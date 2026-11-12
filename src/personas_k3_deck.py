"""Personas k=3 e números do deck executivo (Customer Segmentation Report, Semana 5).

Reproduz todos os números do deck "Vitaliza — Diagnóstico de Churn" (7 slides) a partir da camada
Prata, reaproveitando a montagem da base inteira de `segmentacao_base_inteira.construir()`
(regras POP-002, ATV-001..010, EVT-003, PAG-003..005, SOC-001, ANA-001..004).

Diferença em relação à proposta k=4 (ADR 018): o K-Means usa só 5 variáveis de comportamento,
sem posts e conexões, e k=3 (ver ADR 019). Churn, plano, renovação, receita, pesquisa e campanha
continuam fora do modelo e só descrevem os grupos.

Saída: apenas tabelas agregadas em `saidas/deck_executivo/tabelas/` (GOV-004: nada por cliente).

Uso:
    python src/personas_k3_deck.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
import segmentacao_base_inteira as base  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PRATA = ROOT / "dados" / "processados" / "prata"
OURO = ROOT / "dados" / "processados" / "ouro"
TAB = ROOT / "saidas" / "deck_executivo" / "tabelas"
CORTE = pd.Timestamp("2026-09-30 23:59:59")
SEED = 42
K = 3
VARS = ["dias_semana_pretendidos", "treinos_mes", "regularidade", "n_modalidades", "pct_ar_livre"]
ORD = ["Atleta ao Ar Livre", "Treino em Casa Guiado", "Hábito Fraco"]
CAC = 118.0


def taxa(g: pd.DataFrame) -> float:
    """Churn por mês observado: saídas na janela ÷ meses de assinatura observados (%)."""
    return g["saiu_na_janela"].sum() / g["exposicao_meses"].sum() * 100


def segmentar(b: pd.DataFrame) -> tuple[pd.DataFrame, dict, np.ndarray]:
    fit = b[~b["provisorio"]].copy()
    par = base.parametros(fit, VARS)
    xr = base.matriz(fit, VARS, par)
    esc = StandardScaler().fit(xr)
    x = esc.transform(xr)
    km = KMeans(K, n_init=50, random_state=SEED).fit(x)
    lab = km.labels_
    z = pd.DataFrame(km.cluster_centers_, columns=VARS)
    nomes = {int(z["treinos_mes"].idxmin()): "Hábito Fraco"}
    resto = [i for i in range(K) if i not in nomes]
    nomes[max(resto, key=lambda i: z.loc[i, "pct_ar_livre"])] = "Atleta ao Ar Livre"
    nomes[min(resto, key=lambda i: z.loc[i, "pct_ar_livre"])] = "Treino em Casa Guiado"
    b["persona"] = pd.Series(km.predict(esc.transform(base.matriz(b, VARS, par))), index=b.index).map(nomes)

    rng = np.random.default_rng(SEED)
    boot = [adjusted_rand_score(lab, KMeans(K, n_init=10, random_state=s).fit(x[i]).predict(x))
            for s, i in enumerate(rng.choice(len(x), (10, len(x))))]
    perm = np.column_stack([rng.permutation(x[:, j]) for j in range(x.shape[1])])
    xh = base.matriz(fit.assign(n_modalidades=fit["n_modalidades_hiit_funcional"]), VARS, par)
    q = {
        "clientes": len(b), "ajuste": len(fit), "provisorios": int(b["provisorio"].sum()),
        "silhueta": silhouette_score(x, lab, sample_size=8000, random_state=0),
        "silhueta_embaralhada": silhouette_score(perm, KMeans(K, n_init=10, random_state=SEED).fit_predict(perm), sample_size=8000, random_state=0),
        "davies_bouldin": davies_bouldin_score(x, lab),
        "ari_outra_semente": adjusted_rand_score(lab, KMeans(K, n_init=50, random_state=7).fit_predict(x)),
        "ari_bootstrap_medio": float(np.mean(boot)), "ari_bootstrap_min": float(np.min(boot)),
        "ari_minmax": adjusted_rand_score(lab, KMeans(K, n_init=20, random_state=SEED).fit_predict(MinMaxScaler().fit_transform(xr))),
        "ari_robust": adjusted_rand_score(lab, KMeans(K, n_init=20, random_state=SEED).fit_predict(RobustScaler().fit_transform(xr))),
        "ari_sem_log1p": adjusted_rand_score(lab, KMeans(K, n_init=20, random_state=SEED).fit_predict(StandardScaler().fit_transform(base.matriz(fit, VARS, par, log=False)))),
        "ari_so_ativos": adjusted_rand_score(lab, KMeans(K, n_init=20, random_state=SEED).fit(x[fit["fim"].isna().values]).predict(x)),
        "ari_so_saidos": adjusted_rand_score(lab, KMeans(K, n_init=20, random_state=SEED).fit(x[fit["fim"].notna().values]).predict(x)),
        "ari_hiit_funcional": adjusted_rand_score(lab, KMeans(K, n_init=20, random_state=SEED).fit_predict(StandardScaler().fit_transform(xh))),
    }
    z.rename(index=nomes).loc[ORD].round(3).to_csv(TAB / "centroides_z.csv")
    return b, q, lab


def perfil(b: pd.DataFrame) -> pd.DataFrame:
    s, a = b[~b["provisorio"]], b[b["fim"].isna()]
    saidas = b[b["saiu_na_janela"]]
    linhas = {}
    for p in ORD + ["Base"]:
        g = s if p == "Base" else s[s["persona"] == p]
        ga = a if p == "Base" else a[a["persona"] == p]
        men, anu = g["plano_atual"].eq("mensal"), g["plano_atual"].eq("anual")
        linhas[p] = {
            "ativos": len(ga), "pct_ativos": len(ga) / len(a) * 100,
            "receita_mensal_liquida": ga["receita_liquida_mensal_equiv"].sum(),
            "pct_receita": ga["receita_liquida_mensal_equiv"].sum() / a["receita_liquida_mensal_equiv"].sum() * 100,
            "receita_media_por_ativo": ga["receita_liquida_mensal_equiv"].mean(),
            "custo_saida_ano": ga["receita_liquida_mensal_equiv"].mean() * 12,
            "pct_saidas_2026": (saidas["persona"].eq(p).mean() * 100) if p != "Base" else 100.0,
            "churn_mes": taxa(g), "churn_mes_mensal": taxa(g[men]), "churn_mes_anual": taxa(g[anu]),
            "pct_anual_ativos": ga["plano_atual"].eq("anual").mean() * 100,
            "treinos_mes_mediana": g["treinos_mes"].median(), "regularidade_mediana": g["regularidade"].median(),
            "pct_ar_livre_mediana": g["pct_ar_livre"].median(), "min_por_treino_mediana": g["min_por_treino"].median(),
            "pct_sem_treino": g["sem_treino"].mean() * 100,
            "pct_saida_involuntaria": g["tipo_saida"].eq("involuntaria").sum() / max(g["saiu_na_janela"].sum(), 1) * 100,
            "renovacao_desligada_ativos": int(ga["renovacao_desligada_corte"].sum()),
            "saiu_com_evento_recente_pct": g.loc[g["fase_evento"].eq("evento recente (±60 dias)"), "saiu_na_janela"].mean() * 100,
            "pct_provisorios_no_grupo": (b.loc[b["provisorio"], "persona"].eq(p).mean() * 100) if p != "Base" else 100.0,
        }
    return pd.DataFrame(linhas).T


def categorias(b: pd.DataFrame) -> pd.DataFrame:
    s = b[~b["provisorio"]]
    out = []
    for c in ["motivacao", "modalidade_principal", "canal_aquisicao", "nivel", "sexo", "uf", "relogio_conectado"]:
        ct = pd.crosstab(s[c].astype(object).fillna("não informado"), s["persona"], normalize="columns")[ORD] * 100
        ct["Base"] = s[c].astype(object).fillna("não informado").value_counts(normalize=True) * 100
        out.append(ct.assign(variavel=c).reset_index().rename(columns={c: "categoria"}))
    return pd.concat(out)[["variavel", "categoria", *ORD, "Base"]]


def fatores(b: pd.DataFrame) -> pd.DataFrame:
    s = b[~b["provisorio"]].copy()
    s["constancia_quintil"] = pd.qcut(s["regularidade"].rank(method="first"), 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
    s["conexoes_faixa"] = pd.cut(s["conexoes"], [-1, 0, 2, 5, 1e9], labels=["0", "1-2", "3-5", "6+"])
    s["pagamento_recusado"] = s["pagamentos_recusados"] > 0
    s["idade_faixa"] = pd.cut(s["idade"], [0, 25, 35, 45, 55, 65, 120]).astype(str)
    cols = ["fase_evento", "constancia_quintil", "plano_atual", "motivacao", "conexoes_faixa", "pagamento_recusado",
            "canal_aquisicao", "canal_cobranca", "relogio_conectado", "sexo", "idade_faixa", "uf", "nivel", "persona"]
    out = []
    for c in cols:
        g = s.groupby(s[c].astype(object).fillna("não informado"))
        t = pd.DataFrame({"clientes": g.size(), "saidas": g["saiu_na_janela"].sum(), "meses": g["exposicao_meses"].sum()})
        t = t[t["clientes"] >= 100]
        t["churn_mes"] = t["saidas"] / t["meses"] * 100
        t["razao_max_min"] = t["churn_mes"].max() / t["churn_mes"].min()
        out.append(t.reset_index().rename(columns={c: "categoria"}).assign(fator=c))
    return pd.concat(out)[["fator", "categoria", "clientes", "saidas", "churn_mes", "razao_max_min"]]


def antes_da_saida(b: pd.DataFrame) -> pd.DataFrame:
    s = b[~b["provisorio"] & (b["exposicao_dias"] >= 120)].copy()
    at = pd.read_parquet(PRATA / "atividades_limpas.parquet", columns=["user_id", "inicio_dt_br"])
    at = at[at["user_id"].isin(s["user_id"])]
    at["dias"] = (at["user_id"].map(s.set_index("user_id")["fim_exp"]) - pd.to_datetime(at["inicio_dt_br"])).dt.days
    at = at[at["dias"].between(0, 120)]
    at["janela"] = pd.cut(at["dias"], [-1, 30, 60, 90, 120], labels=["0-30", "31-60", "61-90", "91-120"])
    cnt = at.groupby(["user_id", "janela"], observed=False).size().unstack(fill_value=0)
    s = s.join(cnt, on="user_id")
    jan = ["91-120", "61-90", "31-60", "0-30"]
    s[jan] = s[jan].fillna(0)
    return s.groupby(["saiu_na_janela", "plano_atual"])[jan].mean().round(2).reset_index()


def niveis(b: pd.DataFrame) -> pd.DataFrame:
    a = b[b["fim"].isna()].copy()
    hf, desl = a["persona"].eq("Hábito Fraco"), a["renovacao_desligada_corte"]
    mensal = a["plano_atual"].eq("mensal")
    a["nivel"] = np.select([hf & (desl | mensal), ~hf & desl, ~hf & ~desl], ["1 · Imediata", "2 · Leve", "3 · Monitorar"], "4 · Não perturbe")
    return a.groupby("nivel").agg(clientes=("user_id", "size"), receita_mensal=("receita_liquida_mensal_equiv", "sum")).round(0).reset_index()


def empresa_e_impacto(b: pd.DataFrame) -> dict:
    a = pd.read_parquet(PRATA / "assinaturas_limpas.parquet")
    a["ini"], a["fimd"] = pd.to_datetime(a["inicio"]), pd.to_datetime(a["data_fim"])
    p = pd.read_parquet(PRATA / "pagamentos_limpos.parquet")
    p["d"] = pd.to_datetime(p["data_hora_br"])
    ok = p[p["status"].eq("aprovado") & ~p["flag_duplicata_aprovada_dia"]]
    liq = ok.groupby(ok["d"].dt.to_period("M"))["valor_liquido"].sum()
    sai26 = a[a["fimd"].between("2026-01-01", CORTE)]
    sai26 = sai26.assign(dias=(sai26["fimd"] - sai26["ini"]).dt.days)
    ativos = b[b["fim"].isna()]
    m = a[a["plano_atual"].eq("mensal") & (a["ini"] >= "2025-01-01")].copy()
    elig = m[m["ini"] <= CORTE - pd.Timedelta(days=int(30.44 * 3))]
    dur = (elig["fimd"].fillna(CORTE) - elig["ini"]).dt.days / 30.44
    imp = {"habito_90d": 0.20 * ((sai26["plano_atual"].eq("mensal") & (sai26["dias"] <= 92)).sum() / 9),
           "proximo_objetivo": 0.30 * 58, "renovacao_anual": 0.20 * 758 / 12,
           "pagamento": 0.30 * sai26["motivo_fim"].isin(["falha_pagamento", "chargeback"]).sum() / 9}
    total = sum(imp.values())
    return {
        "novas_2025": int(a["ini"].between("2025-01-01", "2025-12-31 23:59").sum()),
        "saidas_2025": int(a["fimd"].between("2025-01-01", "2025-12-31 23:59").sum()),
        "novas_2026_jan_set": int(a["ini"].between("2026-01-01", CORTE).sum()),
        "saidas_2026_jan_set": len(sai26),
        "receita_liquida_jan_set_2025": float(liq[(liq.index >= "2025-01") & (liq.index <= "2025-09")].sum()),
        "receita_liquida_jan_set_2026": float(liq[(liq.index >= "2026-01") & (liq.index <= "2026-09")].sum()),
        "pct_saidas_voluntarias_2026": float(sai26["motivo_fim"].eq("renovacao_desligada").mean() * 100),
        "saidas_involuntarias_2026": int(sai26["motivo_fim"].isin(["falha_pagamento", "chargeback"]).sum()),
        "saidas_mensal_ate_90d_2026": int((sai26["plano_atual"].eq("mensal") & (sai26["dias"] <= 92)).sum()),
        "pct_mensal_sai_ate_3_meses": float(((elig["fimd"].notna()) & (dur <= 3.05)).mean() * 100),
        "renovacao_desligada_ativos": int(ativos["renovacao_desligada_corte"].sum()),
        "receita_renovacao_desligada": float(ativos.loc[ativos["renovacao_desligada_corte"], "receita_liquida_mensal_equiv"].sum()),
        "ativos_evento_proximos_60d": int(ativos["dias_ate_evento"].between(0, 60).sum()),
        "impacto_saidas_evitadas_mes": {k: round(v, 1) for k, v in imp.items()},
        "impacto_total_mes": round(total, 1), "impacto_pp": round(total / len(ativos) * 100, 2),
        "impacto_receita_ano": round(total * 12 * ativos["receita_liquida_mensal_equiv"].mean() * 12, 0),
        "impacto_cac_evitado": round(total * 12 * CAC, 0),
        "premissas_impacto": "eficácia de 20–30% por ação; excesso de saídas perto do evento de ~58/mês (731 saídas com evento recente, ~81/mês, menos a taxa base); 758 anuais do Hábito Fraco com renovação desligada distribuídos em 12 meses",
    }


def main() -> None:
    TAB.mkdir(parents=True, exist_ok=True)
    b = base.construir()
    b, qualidade, _ = segmentar(b)
    perfil(b).round(2).to_csv(TAB / "perfil_personas.csv")
    categorias(b).round(2).to_csv(TAB / "categorias_personas.csv", index=False)
    fatores(b).round(2).to_csv(TAB / "fatores_churn.csv", index=False)
    antes_da_saida(b).to_csv(TAB / "treinos_antes_da_saida.csv", index=False)
    niveis(b).to_csv(TAB / "niveis_prioridade.csv", index=False)
    seg = pd.read_parquet(OURO / "segmentos_ativos_set2026.parquet").set_index("user_id")["segmento"]
    pd.crosstab(b["persona"], b["user_id"].map(seg)).to_csv(TAB / "personas_vs_segmentos_time.csv")
    resumo = {"qualidade": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in qualidade.items()}, "empresa_e_impacto": empresa_e_impacto(b)}
    (TAB / "resumo_deck.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=1))
    print(pd.read_csv(TAB / "perfil_personas.csv", index_col=0).T.round(1).to_string())
    print(pd.read_csv(TAB / "niveis_prioridade.csv").to_string())


if __name__ == "__main__":
    main()
