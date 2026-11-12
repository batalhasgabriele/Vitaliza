"""Segmentação da base inteira de clientes pagantes (Semana 5), sem usar churn.

População: todo cliente pagante (sem cortesia/interno) com assinatura em vigor em algum momento
de jan–set/2026, esteja ativo ou não no corte. É a maior base com comportamento completo:
treinos de todas as origens só existem a partir de 01/2026.

Comportamento medido por mês de assinatura observado na janela. Churn, status, renovação,
tickets, pesquisa de saída, campanha, plano e receita NÃO entram no K-Means; são usados só
depois, para descrever os segmentos e formular hipóteses.

Uso:
    python src/segmentacao_base_inteira.py --explorar   # compara conjuntos de variáveis e k
    python src/segmentacao_base_inteira.py              # gera a versão final
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import objetivo_onboarding as obj  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PRATA = ROOT / "dados" / "processados" / "prata"
OURO = ROOT / "dados" / "processados" / "ouro"
SAIDA = ROOT / "saidas" / "base_inteira"
TAB = SAIDA / "tabelas"
INI, FIM = pd.Timestamp("2026-01-01"), pd.Timestamp("2026-09-30 23:59:59")
EXPO_MIN = 30
SEED = 42
OUTDOOR = {"corrida", "caminhada", "pedal"}

# min_por_treino fica fora do modelo: é indefinida para quem não treinou e a regra ANA-002
# proíbe preenchê-la com zero (o zero criava um grupo artificial). Fica só como descritiva.
CONJUNTOS = {
    "A_completo": ["idade", "nivel_ord", "dias_semana_pretendidos", "treinos_mes", "sessoes_app_mes", "n_modalidades",
                   "pct_ar_livre", "pct_relogio", "pct_acompanhado", "posts_mes", "conexoes"],
    "B_comportamento": ["dias_semana_pretendidos", "treinos_mes", "regularidade", "sessoes_app_mes", "n_modalidades",
                        "pct_ar_livre", "pct_relogio", "pct_acompanhado", "posts_mes", "conexoes"],
    "C_sem_dispositivo": ["dias_semana_pretendidos", "treinos_mes", "regularidade", "n_modalidades",
                          "pct_ar_livre", "pct_acompanhado", "posts_mes", "conexoes"],
}
LOG = {"treinos_mes", "min_por_treino", "sessoes_app_mes", "pct_acompanhado", "posts_mes", "conexoes"}


def construir() -> pd.DataFrame:
    a = pd.read_parquet(PRATA / "assinaturas_limpas.parquet")
    a["ini"] = pd.to_datetime(a["inicio"]); a["fim"] = pd.to_datetime(a["data_fim"])
    u = pd.read_parquet(PRATA / "usuarios_limpo.parquet")
    # POP-002: a Prata já exclui contas internas/cortesia (32.583 linhas); nenhum filtro adicional
    b = a[(a["ini"] <= FIM) & (a["fim"].isna() | (a["fim"] >= INI))].copy()
    b["ini_exp"] = b["ini"].clip(lower=INI)
    b["fim_exp"] = b["fim"].fillna(FIM).clip(upper=FIM)
    b["exposicao_dias"] = ((b["fim_exp"] - b["ini_exp"]).dt.days + 1).clip(lower=1)
    b["exposicao_meses"] = (b["exposicao_dias"] / 30.44).clip(lower=1)  # ANA-001: mínimo de um mês
    b["semanas_expostas"] = (b["exposicao_dias"] / 7).clip(lower=1)
    jan = b.set_index("user_id")[["ini_exp", "fim_exp"]]
    lim_fim = jan["fim_exp"].dt.normalize() + pd.Timedelta(days=1)

    def dentro(df, col):
        x = df[df["user_id"].isin(jan.index)].copy()
        x[col] = pd.to_datetime(x[col])
        return x[(x[col] >= x["user_id"].map(jan["ini_exp"])) & (x[col] < x["user_id"].map(lim_fim))]

    # perfil e onboarding
    u["email_norm"] = u["email"].str.lower().str.strip()
    u["conta_duplicada"] = u["email_norm"].duplicated(keep=False)
    b = b.merge(u[["user_id", "idade", "sexo", "uf", "canal_aquisicao", "sistema", "relogio_conectado", "conta_duplicada"]], on="user_id", how="left")
    onb = pd.read_parquet(PRATA / "onboarding_limpo.parquet")
    b = b.merge(onb[["user_id", "nivel", "dias_semana_pretendidos"]], on="user_id", how="left")
    b = b.merge(obj.tratar(onb), on="user_id", how="left")
    b["nivel_ord"] = b["nivel"].map({"iniciante": 1, "intermediario": 2, "avancado": 3})
    b["motivacao"] = b["motivacao"].fillna("nao_informado")
    b["tem_prazo"] = b["tem_prazo"].astype("boolean").fillna(False).astype(bool)

    # treinos: Prata já válida e deduplicada (ATV-003/004/007); distância >200 km já anulada com o treino
    # preservado (ATV-005); outliers não são removidos (ATV-010); modalidades canônicas (ATV-001)
    at = pd.read_parquet(PRATA / "atividades_limpas.parquet")
    at = dentro(at, "inicio_dt_br")
    at["tipo_seg"] = at["tipo_canonico"]
    at["ar_livre"] = at["tipo_seg"].isin(OUTDOOR)
    at["relogio"] = at["origem"].ne("app")
    at["acomp"] = at["treino_com"].fillna("").astype(str).str.strip().ne("")
    at["semana"] = at["inicio_dt_br"].dt.to_period("W")
    g = at.groupby("user_id").agg(n_treinos=("atividade_id", "size"), min_por_treino=("duracao_min", "mean"),
                                  n_modalidades=("tipo_seg", "nunique"), pct_ar_livre=("ar_livre", "mean"),
                                  pct_relogio=("relogio", "mean"), pct_acompanhado=("acomp", "mean"),
                                  minutos=("duracao_min", "sum"), semanas_com_treino=("semana", "nunique"),
                                  ultimo_treino=("inicio_dt_br", "max"))
    g["modalidade_principal"] = at.groupby("user_id")["tipo_seg"].agg(lambda s: s.mode().iat[0])
    # só para sensibilidade (ponto de atenção 5, não é regra do registro): hiit unido a funcional
    g["n_modalidades_hiit_funcional"] = at.assign(t=at["tipo_seg"].replace({"hiit": "funcional"})).groupby("user_id")["t"].nunique()
    b = b.merge(g, on="user_id", how="left")

    # sessões de app nos meses com assinatura
    m = pd.read_parquet(PRATA / "uso_mensal_limpo.parquet")
    m = m[m["user_id"].isin(jan.index) & m["mes"].between("2026-01", "2026-09")].copy()
    m["ts"] = pd.to_datetime(m["mes"] + "-01")
    m = m[(m["ts"] + pd.offsets.MonthEnd(0) >= m["user_id"].map(jan["ini_exp"])) & (m["ts"] <= m["user_id"].map(jan["fim_exp"]))]
    b["sessoes"] = b["user_id"].map(m.groupby("user_id")["sessoes_app"].sum())

    # social
    f = pd.read_parquet(PRATA / "feed_posts_limpos.parquet")
    f = dentro(f[~f["flag_apos_corte"]], "data_hora_dt")
    b["posts"] = b["user_id"].map(f.groupby("user_id").size())
    # SOC-001: relações até o corte e, para quem saiu, até a data de saída
    am = pd.read_parquet(PRATA / "amizades_limpas.parquet")
    am = am[~am["flag_apos_corte"]].copy(); am["desde_dt"] = pd.to_datetime(am["desde_dt"])
    seguidos = am[am["desde_dt"] < am["seguido_id"].map(lim_fim)]
    seguidores = am[am["desde_dt"] < am["seguidor_id"].map(lim_fim)]
    b["conexoes"] = b["user_id"].map(seguidos.groupby("seguido_id").size()).fillna(0) + b["user_id"].map(seguidores.groupby("seguidor_id").size()).fillna(0)

    # descritivas (não entram no modelo)
    t = pd.read_parquet(PRATA / "tickets_suporte_limpos.parquet")
    t = dentro(t, "aberto_em_dt")
    b["tickets"] = b["user_id"].map(t.groupby("user_id").size())
    b["tickets_cobranca"] = b["user_id"].map(t[t["categoria_atendente"].eq("cobranca")].groupby("user_id").size())
    # CLU-006 / PAG-003/004/005: último pagamento aprovado, deduplicado e líquido de taxas até o desfecho;
    # anual dividido por 12; tabela de preço como fallback
    pr = pd.read_parquet(PRATA / "pagamentos_limpos.parquet")
    p = pr[pr["status"].eq("aprovado") & pr["valor_num"].gt(0) & ~pr["flag_duplicata_aprovada_dia"] & pr["user_id"].isin(jan.index)].copy()
    p["data_hora_br"] = pd.to_datetime(p["data_hora_br"])
    p = p[p["data_hora_br"] < p["user_id"].map(lim_fim)]
    ult = p.sort_values(["user_id", "data_hora_br"]).drop_duplicates("user_id", keep="last").set_index("user_id")
    anual = b["plano_atual"].eq("anual")
    taxa = b["canal_cobranca"].map({"app_store": 0.15, "google_play": 0.15, "web_cartao": 0.035, "web_pix": 0.0099}).fillna(0.0)
    bruto = b["user_id"].map(ult["valor_num"]).fillna(pd.Series(np.where(anual, 299.90, 39.90), index=b.index))
    liquido = b["user_id"].map(ult["valor_liquido"]).fillna(bruto * (1 - taxa))
    b["receita_liquida_mensal_equiv"] = np.where(anual, liquido / 12, liquido)
    b["flag_pagamento_ausente"] = b["user_id"].map(ult["valor_num"]).isna()
    b["pagamentos_recusados"] = b["user_id"].map(dentro(pr[pr["status"].eq("recusado")], "data_hora_br").groupby("user_id").size())
    ev = pd.read_parquet(PRATA / "eventos_assinatura_limpos.parquet")
    ev["d"] = pd.to_datetime(ev["data_hora_br"])
    ev = ev[ev["d"] <= FIM]
    ult = ev[ev["evento"].isin(["renovacao_automatica_desligada", "renovacao_automatica_religada"])].sort_values("d").groupby("user_id")["evento"].last()
    b["renovacao_desligada_corte"] = b["user_id"].map(ult.eq("renovacao_automatica_desligada")).fillna(False).astype(bool) & b["fim"].isna()
    # PES-002: resposta mais recente por pessoa
    q = pd.read_parquet(PRATA / "pesquisa_saida_limpa.parquet").sort_values("respondido_em_dt").drop_duplicates("user_id", keep="last")
    b["motivo_pesquisa"] = b["user_id"].map(q.set_index("user_id")["motivo_principal"])

    # ANA-002: zero só para contagens; descritivas e demográficas ficam nulas
    zero = ["n_treinos", "minutos", "semanas_com_treino", "sessoes", "posts", "tickets", "tickets_cobranca", "pagamentos_recusados"]
    b[zero] = b[zero].fillna(0)
    em = b["exposicao_meses"]
    b["treinos_mes"] = b["n_treinos"] / em
    b["minutos_mes"] = b["minutos"] / em
    b["sessoes_app_mes"] = b["sessoes"] / em
    b["posts_mes"] = b["posts"] / em
    b["regularidade"] = (b["semanas_com_treino"] / b["semanas_expostas"]).clip(upper=1)
    b["sem_treino"] = b["n_treinos"].eq(0)
    b["dias_sem_treinar_no_fim"] = (b["fim_exp"] - b["ultimo_treino"]).dt.days
    b["provisorio"] = b["exposicao_dias"] < EXPO_MIN

    # desfecho (só descritivo, depois do cluster)
    b["saiu_na_janela"] = b["fim"].notna()
    b["tipo_saida"] = b["motivo_fim"].map({"renovacao_desligada": "voluntaria", "falha_pagamento": "involuntaria", "chargeback": "involuntaria", "reembolso": "reembolso"})
    ref = b["fim"].fillna(FIM)
    b["dias_ate_evento"] = (b["data_evento"] - ref).dt.days
    b["fase_evento"] = np.select([~b["tem_prazo"], b["data_evento"].isna(), b["dias_ate_evento"] > 30, b["dias_ate_evento"] >= -60],
                                 ["sem prazo", "prazo sem data", "evento à frente", "evento recente (±60 dias)"], "evento passou há 60+ dias")
    seg = pd.read_parquet(OURO / "segmentos_ativos_set2026.parquet")
    b["segmento_time"] = b["user_id"].map(seg.set_index("user_id")["segmento"])
    return b


PROPORCOES = {"regularidade", "pct_ar_livre", "pct_acompanhado", "pct_relogio"}


def parametros(fit: pd.DataFrame, cols: list[str]) -> dict:
    """CLU-003 (mesma regra de preparar_matriz do time): mediana só para dias pretendidos,
    zero nas demais ausências, teto no P99 fora das proporções, depois log1p."""
    x = fit[cols].copy()
    med = float(x["dias_semana_pretendidos"].median()) if "dias_semana_pretendidos" in cols else None
    if med is not None:
        x["dias_semana_pretendidos"] = x["dias_semana_pretendidos"].fillna(med)
    x = x.fillna(0.0)
    return {"med_dias": med, "p99": {c: float(x[c].quantile(.99)) for c in cols if c not in PROPORCOES}}


def matriz(b: pd.DataFrame, cols: list[str], par: dict, log: bool = True) -> pd.DataFrame:
    x = b[cols].copy()
    if par["med_dias"] is not None:
        x["dias_semana_pretendidos"] = x["dias_semana_pretendidos"].fillna(par["med_dias"])
    x = x.fillna(0.0).astype(float)
    for c in cols:
        if c in par["p99"]:
            x[c] = x[c].clip(upper=par["p99"][c])
        if log and c in LOG:
            x[c] = np.log1p(x[c].clip(lower=0))
    return x


def avaliar(X, k, reps=10):
    km = KMeans(k, n_init=30, random_state=SEED).fit(X)
    rng = np.random.default_rng(SEED); aris = []
    for s in range(reps):
        i = rng.choice(len(X), len(X))
        aris.append(adjusted_rand_score(km.labels_, KMeans(k, n_init=20, random_state=s).fit(X[i]).predict(X)))
    tam = np.bincount(km.labels_) / len(X)
    return km, {"k": k, "silhueta": silhouette_score(X, km.labels_, sample_size=8000, random_state=0), "davies_bouldin": davies_bouldin_score(X, km.labels_),
                "calinski_harabasz": calinski_harabasz_score(X, km.labels_), "ari_bootstrap": float(np.mean(aris)), "ari_min": float(np.min(aris)),
                "menor_cluster_pct": tam.min() * 100, "inercia": km.inertia_}


def explorar(b: pd.DataFrame) -> None:
    fit = b[~b["provisorio"]]
    linhas = []
    for nome, cols in CONJUNTOS.items():
        X = StandardScaler().fit_transform(matriz(fit, cols, parametros(fit, cols)))
        for k in range(3, 7):
            km, r = avaliar(X, k, reps=6)
            at = fit["segmento_time"].notna().values
            r.update({"conjunto": nome, "ari_vs_time_nos_ativos": adjusted_rand_score(fit.loc[at, "segmento_time"], km.labels_[at])})
            linhas.append(r); print({kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in r.items()}, flush=True)
            if k in (4, 5):
                z = pd.DataFrame(km.cluster_centers_, columns=cols).round(2); z.insert(0, "pct", (np.bincount(km.labels_) / len(X) * 100).round(1))
                print(z.T.to_string())
    pd.DataFrame(linhas).to_csv(TAB / "exploracao_conjuntos_k.csv", index=False)


# ---------------------------------------------------------------------------
# Versão final: conjunto C (sem variáveis que medem o dispositivo), k = 4
# ---------------------------------------------------------------------------
FINAL = CONJUNTOS["C_sem_dispositivo"]
K = 4
ORD = ["Ativo ao Ar Livre", "Treino Indoor Guiado", "Hábito Fraco", "Treina em Companhia"]


def jaccard_melhor(lab, outro, c):
    A = lab == c
    return max((A & (outro == q)).sum() / (A | (outro == q)).sum() for q in np.unique(outro))


def final(b: pd.DataFrame) -> None:
    from scipy import stats
    from sklearn.preprocessing import MinMaxScaler, RobustScaler
    fit = b[~b["provisorio"]].copy()
    par = parametros(fit, FINAL)
    Xr = matriz(fit, FINAL, par); esc = StandardScaler().fit(Xr); X = esc.transform(Xr)
    km = KMeans(K, n_init=50, random_state=SEED).fit(X); lab = km.labels_
    Z = pd.DataFrame(km.cluster_centers_, columns=FINAL)
    nomes = {Z.pct_acompanhado.idxmax(): "Treina em Companhia", Z.treinos_mes.idxmin(): "Hábito Fraco"}
    resto = [i for i in range(K) if i not in nomes]
    nomes[max(resto, key=lambda i: Z.loc[i, "pct_ar_livre"])] = "Ativo ao Ar Livre"
    nomes[min(resto, key=lambda i: Z.loc[i, "pct_ar_livre"])] = "Treino Indoor Guiado"
    b["persona"] = pd.Series(km.predict(esc.transform(matriz(b, FINAL, par))), index=b.index).map(nomes)
    fit["persona"] = pd.Series(lab, index=fit.index).map(nomes)

    # robustez
    rob = []

    def comp(nome, outro):
        r = {"cenario": nome, "ari": adjusted_rand_score(lab, outro)}
        r.update({nomes[c]: jaccard_melhor(lab, outro, c) for c in range(K)})
        rob.append(r)
    comp("MinMaxScaler", KMeans(K, n_init=20, random_state=SEED).fit_predict(MinMaxScaler().fit_transform(Xr)))
    comp("RobustScaler", KMeans(K, n_init=20, random_state=SEED).fit_predict(RobustScaler().fit_transform(Xr)))
    comp("Sem log1p", KMeans(K, n_init=20, random_state=SEED).fit_predict(StandardScaler().fit_transform(matriz(fit, FINAL, par, log=False))))
    Xh = matriz(fit.assign(n_modalidades=fit["n_modalidades_hiit_funcional"]), FINAL, parametros(fit.assign(n_modalidades=fit["n_modalidades_hiit_funcional"]), FINAL))
    comp("hiit unido a funcional (sensibilidade)", KMeans(K, n_init=30, random_state=SEED).fit_predict(StandardScaler().fit_transform(Xh)))
    comp("Outra semente", KMeans(K, n_init=50, random_state=7).fit_predict(X))
    comp("Sem contas duplicadas", KMeans(K, n_init=30, random_state=SEED).fit(X[~fit.conta_duplicada.values]).predict(X))
    cc = fit[FINAL].notna().all(axis=1).values
    comp("Só casos completos", KMeans(K, n_init=30, random_state=SEED).fit(X[cc]).predict(X))
    comp("Ajuste só com ativos no corte", KMeans(K, n_init=30, random_state=SEED).fit(X[fit.fim.isna().values]).predict(X))
    comp("Ajuste só com quem saiu na janela", KMeans(K, n_init=30, random_state=SEED).fit(X[fit.fim.notna().values]).predict(X))
    rng = np.random.default_rng(SEED); jac = {c: [] for c in range(K)}
    for s in range(20):
        i = rng.choice(len(X), len(X)); o = KMeans(K, n_init=20, random_state=s).fit(X[i]).predict(X)
        for c in range(K):
            jac[c].append(jaccard_melhor(lab, o, c))
    rob.append({"cenario": "Bootstrap 20x, Jaccard médio", "ari": np.nan, **{nomes[c]: np.mean(jac[c]) for c in range(K)}})
    rob.append({"cenario": "Bootstrap 20x, Jaccard mínimo", "ari": np.nan, **{nomes[c]: np.min(jac[c]) for c in range(K)}})
    perm = np.column_stack([rng.permutation(X[:, j]) for j in range(X.shape[1])])
    sil_real = silhouette_score(X, lab, sample_size=8000, random_state=0)
    sil_perm = silhouette_score(perm, KMeans(K, n_init=10, random_state=SEED).fit_predict(perm), sample_size=8000, random_state=0)
    pd.DataFrame(rob).round(3).to_csv(TAB / "robustez.csv", index=False)

    # centróides e importância
    zc = Z.rename(index=nomes).loc[ORD]; zc.round(3).to_csv(TAB / "centroides_z.csv")
    eta = {}
    for j, c in enumerate(FINAL):
        gm = X[:, j].mean(); eta[c] = sum((lab == i).sum() * (X[lab == i, j].mean() - gm) ** 2 for i in range(K)) / ((X[:, j] - gm) ** 2).sum()
    pd.Series(eta, name="eta2").sort_values(ascending=False).round(4).to_csv(TAB / "importancia_variaveis.csv")

    # estatísticas por persona (só >= 30 dias observados)
    S = fit
    m = pd.read_parquet(PRATA / "uso_mensal_limpo.parquet", columns=["user_id", "mes", "atividades_video", "atividades_ar_livre"])
    m = m[m.mes.between("2026-01", "2026-09")].groupby("user_id")[["atividades_video", "atividades_ar_livre"]].sum()
    S["pct_video_app"] = (m.atividades_video / (m.atividades_video + m.atividades_ar_livre)).reindex(S.user_id).values
    NUM = ["treinos_mes", "regularidade", "minutos_mes", "min_por_treino", "n_modalidades", "pct_ar_livre", "pct_video_app", "pct_relogio", "pct_acompanhado",
           "sessoes_app_mes", "posts_mes", "conexoes", "dias_semana_pretendidos", "nivel_ord", "idade", "tickets", "receita_liquida_mensal_equiv", "exposicao_meses"]
    rows = []
    for v in NUM:
        for p in ["Base"] + ORD:
            s = (S[v] if p == "Base" else S.loc[S.persona == p, v]).dropna()
            rows.append({"variavel": v, "entrada": v in FINAL, "persona": p, "n": len(s), "media": s.mean(), "dp": s.std(), "p25": s.quantile(.25), "mediana": s.median(), "p75": s.quantile(.75)})
    pd.DataFrame(rows).round(3).to_csv(TAB / "estatisticas_numericas.csv", index=False)

    # desfecho e descritivas pós-cluster
    def resumo(g):
        sai = g.saiu_na_janela
        men, anu = g.plano_atual.eq("mensal"), g.plano_atual.eq("anual")
        return pd.Series({
            "clientes": len(g), "pct_base": len(g) / len(S) * 100,
            "churn_mensal_pct": sai.sum() / g.exposicao_meses.sum() * 100,
            "saiu_na_janela_pct": sai.mean() * 100,
            "saida_voluntaria_pct": g.tipo_saida.eq("voluntaria").sum() / max(sai.sum(), 1) * 100,
            "saida_involuntaria_pct": g.tipo_saida.eq("involuntaria").sum() / max(sai.sum(), 1) * 100,
            "renov_desligada_ativos_pct": g.loc[g.fim.isna(), "renovacao_desligada_corte"].mean() * 100,
            "sem_treino_30d_antes_saida_pct": (g.loc[sai, "dias_sem_treinar_no_fim"].fillna(999) > 30).mean() * 100,
            "anual_pct": anu.mean() * 100,
            "churn_mensal_mensalistas_pct": g.loc[men, "saiu_na_janela"].sum() / g.loc[men, "exposicao_meses"].sum() * 100,
            "churn_mensal_anuais_pct": g.loc[anu, "saiu_na_janela"].sum() / g.loc[anu, "exposicao_meses"].sum() * 100,
            "com_prazo_pct": g.tem_prazo.mean() * 100,
            "saiu_evento_recente_pct": g.loc[g.fase_evento.eq("evento recente (±60 dias)"), "saiu_na_janela"].mean() * 100,
            "relogio_pct": g.relogio_conectado.ne("nenhum").mean() * 100,
            "indicacao_pct": g.canal_aquisicao.eq("indicacao").mean() * 100,
            "pag_recusado_pct": (g.pagamentos_recusados > 0).mean() * 100,
            "tickets_cobranca_pct": (g.tickets_cobranca > 0).mean() * 100,
            "receita_mensal_equiv_media": g.receita_liquida_mensal_equiv.mean(),
            "receita_mensal_ativos": g.loc[g.fim.isna(), "receita_liquida_mensal_equiv"].sum(),
            "ativos_no_corte": int(g.fim.isna().sum()),
        })
    R = pd.concat({**{p: resumo(S[S.persona == p]) for p in ORD}, "Base": resumo(S)}, axis=1).T
    R["pct_receita"] = R.receita_mensal_ativos / R.loc[ORD, "receita_mensal_ativos"].sum() * 100
    R["provisorios"] = b[b.provisorio].persona.value_counts().reindex(ORD)
    R.loc["Base", "provisorios"] = int(b.provisorio.sum())
    R.round(2).to_csv(TAB / "resumo_personas.csv")

    cats = {"plano_atual": "Plano", "canal_cobranca": "Canal de cobrança", "canal_aquisicao": "Canal de aquisição", "relogio_conectado": "Relógio",
            "motivacao": "Motivação declarada", "modalidade_principal": "Modalidade principal", "nivel": "Nível", "sexo": "Sexo", "uf": "UF",
            "sistema": "Sistema", "fase_evento": "Objetivo com prazo", "tipo_saida": "Tipo de saída (só quem saiu)",
            "motivo_pesquisa": "Motivo na pesquisa de saída", "segmento_time": "Segmento do time (só ativos)"}
    linhas, efe = [], []
    for c, rot in cats.items():
        x = S[c].dropna() if c in ("tipo_saida", "motivo_pesquisa", "segmento_time") else S[c].astype("object").fillna("não informado")
        ct = pd.crosstab(x, S.loc[x.index, "persona"]).reindex(columns=ORD, fill_value=0)
        chi, pv, gl, _ = stats.chi2_contingency(ct)
        efe.append({"variavel": rot, "cramer_v": np.sqrt(chi / (ct.values.sum() * (min(ct.shape) - 1))), "p": pv, "n": int(ct.values.sum())})
        pc = ct / ct.sum() * 100; base = x.value_counts(normalize=True) * 100
        for cat in ct.index:
            linhas.append({"variavel": rot, "categoria": cat, "base_pct": base[cat], **{p: pc.loc[cat, p] for p in ORD}})
    pd.DataFrame(linhas).round(2).to_csv(TAB / "estatisticas_categoricas.csv", index=False)
    pd.DataFrame(efe).sort_values("cramer_v", ascending=False).round(4).to_csv(TAB / "estatisticas_categoricas_efeito.csv", index=False)
    cf = S.groupby(["persona", "fase_evento"]).agg(n=("user_id", "size"), saiu_pct=("saiu_na_janela", "mean")).reset_index()
    cf["saiu_pct"] *= 100; cf.round(2).to_csv(TAB / "churn_por_fase_evento.csv", index=False)

    b[["user_id", "persona", "provisorio", "saiu_na_janela"]].to_csv(TAB / "personas_clientes.csv", index=False)
    S.to_pickle(SAIDA / "_fit.pkl"); np.save(SAIDA / "_X.npy", X)
    (SAIDA / "_meta.json").write_text(json.dumps({"variaveis": FINAL, "k": K, "silhueta": float(sil_real), "silhueta_embaralhada": float(sil_perm),
                                                 "clientes": len(b), "ajuste": len(S), "provisorios": int(b.provisorio.sum())}, ensure_ascii=False, indent=1), encoding="utf-8")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print("silhueta", sil_real, "embaralhada", sil_perm)
    print(pd.read_csv(TAB / "robustez.csv").to_string()); print(zc.round(2).T.to_string()); print(R.round(1).T.to_string())
    print(pd.read_csv(TAB / "estatisticas_categoricas_efeito.csv").to_string())
    sn = pd.read_csv(TAB / "estatisticas_numericas.csv")
    print(sn.pivot(index="variavel", columns="persona", values="media")[["Base"] + ORD].round(2).to_string())
    print(sn.pivot(index="variavel", columns="persona", values="mediana")[["Base"] + ORD].round(2).to_string())
    print(pd.read_csv(TAB / "estatisticas_categoricas.csv").to_string())
    print(cf.round(1).to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--explorar", action="store_true"); args = ap.parse_args()
    TAB.mkdir(parents=True, exist_ok=True)
    base = construir()
    print("clientes:", len(base), "| provisórios:", int(base.provisorio.sum()), "| ativos no corte:", int(base.fim.isna().sum()), "| saíram na janela:", int(base.saiu_na_janela.sum()))
    explorar(base) if args.explorar else final(base)
