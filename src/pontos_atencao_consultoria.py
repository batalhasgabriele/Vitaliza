"""Verificações de consultoria sobre o trabalho da Semana 5 (somente leitura da Prata/Ouro).

Cada verificação vira uma linha em saidas/base_inteira/tabelas/pontos_atencao_evidencias.csv
para ser discutida com o time. Nada da Bronze, Prata ou Ouro oficial é alterado.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PRATA = ROOT / "dados" / "processados" / "prata"
OURO = ROOT / "dados" / "processados" / "ouro"
OUT = ROOT / "saidas" / "base_inteira" / "tabelas"
OUT.mkdir(parents=True, exist_ok=True)
CORTE = pd.Timestamp("2026-09-30 23:59:59")
ENVIO = pd.Timestamp("2026-08-10 10:00:00")


def ic_dif(p1, n1, p0, n0):
    se = np.sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
    d = p1 - p0
    return d * 100, (d - 1.96 * se) * 100, (d + 1.96 * se) * 100


def main() -> None:
    ev = []
    a = pd.read_parquet(PRATA / "assinaturas_limpas.parquet")
    a["ini"] = pd.to_datetime(a["inicio"]); a["fim"] = pd.to_datetime(a["data_fim"])
    u = pd.read_parquet(PRATA / "usuarios_limpo.parquet")
    at = pd.read_parquet(PRATA / "atividades_limpas.parquet", columns=["user_id", "inicio_dt_br", "origem"])
    at["d"] = pd.to_datetime(at["inicio_dt_br"])
    at = at[at["d"] <= CORTE]
    seg = pd.read_parquet(OURO / "features_segmentacao_ativos_set2026.parquet")

    # 1. População de sobreviventes
    pag = a[a["plano_atual"] != "cortesia"]
    ativos = pag[pag["fim"].isna()]
    saiu26 = pag[pag["fim"].between("2026-01-01", CORTE)].copy()
    j = at.merge(saiu26[["user_id", "fim"]], on="user_id")
    j = j[(j["d"] < j["fim"] + pd.Timedelta(days=1)) & (j["d"] >= j["fim"] - pd.Timedelta(days=29))]
    saiu26["treinos_30d_antes_saida"] = saiu26["user_id"].map(j.groupby("user_id").size()).fillna(0)
    dorm = saiu26["treinos_30d_antes_saida"].eq(0)
    ev.append({"ponto": "1. Segmentação só com sobreviventes", "metrica": "pagantes já vistos / ativos usados no cluster", "valor": f"{len(pag):,} / {len(ativos):,}"})
    ev.append({"ponto": "1. Segmentação só com sobreviventes", "metrica": "saídas em jan–set/2026 fora da segmentação", "valor": f"{len(saiu26):,}"})
    ev.append({"ponto": "1. Segmentação só com sobreviventes", "metrica": "das saídas de 2026, % sem treino nos 30 dias antes de sair", "valor": f"{dorm.mean()*100:.1f}% ({dorm.sum():,})"})
    ev.append({"ponto": "1. Segmentação só com sobreviventes", "metrica": "% sem treino antes de sair, mensal vs anual", "valor": f"{dorm[saiu26.plano_atual.eq('mensal')].mean()*100:.1f}% vs {dorm[saiu26.plano_atual.eq('anual')].mean()*100:.1f}%"})
    ev.append({"ponto": "1. Segmentação só com sobreviventes", "metrica": "% anual: ativos vs saídas de 2026", "valor": f"{ativos.plano_atual.eq('anual').mean()*100:.1f}% vs {saiu26.plano_atual.eq('anual').mean()*100:.1f}%"})

    # 2. EDA com cobertura desigual de uso
    f = pd.read_parquet(OURO / "features_eda_corte_set2026.parquet")
    f["ano_fim"] = pd.to_datetime(f["data_fim"]).dt.year
    sem = f["meses_registrados"].eq(0)
    ev.append({"ponto": "2. Variáveis de uso na EDA com cobertura desigual", "metrica": "saídas de 2024 sem nenhum mês de uso (uso_mensal começa em 2025)", "valor": f"{int((sem & f.ano_fim.eq(2024)).sum()):,} de {int(f.ano_fim.eq(2024).sum()):,}"})
    for col in ["media_sessoes_mes", "media_atividades_mes", "media_minutos_mes"]:
        x = f[[col, "churn"]].dropna()
        auc_all = roc_auc_score(x.churn, -x[col])
        y = f.loc[~sem & ~f.ano_fim.eq(2024), [col, "churn"]].dropna()
        auc_ok = roc_auc_score(y.churn, -y[col])
        ev.append({"ponto": "2. Variáveis de uso na EDA com cobertura desigual", "metrica": f"AUC de {col}: todos vs só com cobertura", "valor": f"{auc_all:.3f} vs {auc_ok:.3f}"})
    for mes in ["2025-03", "2025-09", "2026-03", "2026-09"]:
        t = pd.Timestamp(mes + "-01")
        ids = set(pag.user_id[(pag.ini <= t + pd.offsets.MonthEnd(0)) & (pag.fim.isna() | (pag.fim >= t))])
        m = pd.read_parquet(PRATA / "uso_mensal_limpo.parquet", columns=["user_id", "mes"]) if mes == "2025-03" else m
        rows = set(m.user_id[m.mes == mes])
        ev.append({"ponto": "2. Variáveis de uso na EDA com cobertura desigual", "metrica": f"assinantes de {mes} com linha em uso_mensal", "valor": f"{len(ids & rows)/len(ids)*100:.1f}%"})

    # 3. Relógio dentro do grupo adormecido
    s = seg.copy()
    s["garmin"] = s.relogio_conectado.eq("garmin")
    ad = s[s.segmento.eq("Adormecidos sem hábito")]
    ev.append({"ponto": "3. Relógio e o grupo adormecido", "metrica": "% Garmin: adormecidos vs demais", "valor": f"{ad.garmin.mean()*100:.1f}% vs {s[~s.segmento.eq('Adormecidos sem hábito')].garmin.mean()*100:.1f}%"})
    ev.append({"ponto": "3. Relógio e o grupo adormecido", "metrica": "adormecidos com 4+ treinos nos últimos 90 dias", "valor": f"{(ad.treinos_90d >= 4).sum():,} ({(ad.treinos_90d >= 4).mean()*100:.1f}%)"})
    ev.append({"ponto": "3. Relógio e o grupo adormecido", "metrica": "mediana de treinos 90d dos adormecidos: com relógio vs sem", "valor": f"{ad[ad.relogio_conectado.ne('nenhum')].treinos_90d.median():.0f} vs {ad[ad.relogio_conectado.eq('nenhum')].treinos_90d.median():.0f}"})
    ev.append({"ponto": "3. Relógio e o grupo adormecido", "metrica": "regularidade_3m vem de uso_mensal, que não registra treino de relógio", "valor": "verificado: 91,5% dos meses batem com origem app"})

    # 4. hiit só existe no app
    t = pd.read_parquet(PRATA / "atividades_limpas.parquet", columns=["tipo_canonico", "origem"])
    ev.append({"ponto": "4. Taxonomia de modalidade depende da fonte", "metrica": "treinos hiit vindos de relógio", "valor": f"{int(((t.tipo_canonico=='hiit') & (t.origem!='app')).sum())} de {int((t.tipo_canonico=='hiit').sum()):,}"})
    ev.append({"ponto": "4. Taxonomia de modalidade depende da fonte", "metrica": "% de funcional entre treinos de relógio vs app", "valor": f"{(t[t.origem!='app'].tipo_canonico=='funcional').mean()*100:.1f}% vs {(t[t.origem=='app'].tipo_canonico=='funcional').mean()*100:.1f}%"})

    # 5. Campanha: janela e elegibilidade
    c = pd.read_parquet(PRATA / "campanha_ago26_limpa.parquet").merge(pag[["user_id", "fim", "plano_atual", "ini"]], on="user_id", how="left")
    ja_saiu = c.fim.notna() & (c.fim < ENVIO.normalize())
    cc = c[~ja_saiu].copy()

    def renova(ini, plano):
        if plano == "anual":
            k = ENVIO.year - ini.year; p = ini + pd.DateOffset(years=k)
            return p if p >= ENVIO.normalize() else ini + pd.DateOffset(years=k + 1)
        return None
    cc["renov"] = [renova(i, p) for i, p in zip(cc.ini, cc.plano_atual)]
    cc["elegivel"] = cc.plano_atual.eq("mensal") | (cc.renov <= CORTE)
    linhas = []
    # 30 dias para todos = regra CAM-002 do registro (resultado oficial); as outras duas são sensibilidades propostas
    for nome, janela, sub in [("30 dias, todos (regra CAM-002)", pd.Timedelta(days=30), cc), ("até 30/09, todos", CORTE - ENVIO.normalize(), cc), ("até 30/09, só quem renova na janela", CORTE - ENVIO.normalize(), cc[cc.elegivel])]:
        sub = sub.assign(saiu=sub.fim.notna() & (sub.fim >= ENVIO.normalize()) & (sub.fim <= ENVIO.normalize() + janela))
        ctl = sub[sub.grupo == "controle"]
        for g in ["cupom", "desafio", "conteudo"]:
            gg = sub[sub.grupo == g]
            d, lo, hi = ic_dif(gg.saiu.mean(), len(gg), ctl.saiu.mean(), len(ctl))
            linhas.append({"janela": nome, "grupo": g, "n": len(gg), "churn_pct": gg.saiu.mean() * 100, "controle_pct": ctl.saiu.mean() * 100, "dif_pp": d, "ic95_inf": lo, "ic95_sup": hi})
    camp = pd.DataFrame(linhas).round(2)
    camp.to_csv(OUT / "campanha_janelas.csv", index=False)
    for r in camp[camp.grupo == "cupom"].itertuples():
        ev.append({"ponto": "5. Campanha A/B: janela e elegibilidade", "metrica": f"cupom vs controle ({r.janela})", "valor": f"{r.dif_pp:+.2f} p.p. [IC95 {r.ic95_inf:+.2f}; {r.ic95_sup:+.2f}]"})

    # 6. Contas duplicadas
    em = u.email.str.lower().str.strip()
    ev.append({"ponto": "6. Contas duplicadas não tratadas", "metrica": "contas com e-mail repetido após normalizar caixa", "valor": f"{int(em.duplicated(keep=False).sum()):,} contas ({int(em.duplicated().sum())} pares)"})
    dup_ids = set(u.user_id[em.duplicated(keep=False)])
    ev.append({"ponto": "6. Contas duplicadas não tratadas", "metrica": "dessas, contas com assinatura paga", "valor": f"{int(pag.user_id.isin(dup_ids).sum())}"})

    # 7. Objetivo com prazo fora das análises
    sys.path.insert(0, str(ROOT / "src"))
    import objetivo_onboarding as obj
    o = obj.tratar(pd.read_parquet(PRATA / "onboarding_limpo.parquet"))
    ev.append({"ponto": "7. Objetivo com prazo não é usado", "metrica": "onboardings com objetivo datado (evento, prova, viagem)", "valor": f"{o.tem_prazo.mean()*100:.1f}%"})
    # PES-002: resposta mais recente por pessoa
    q = pd.read_parquet(PRATA / "pesquisa_saida_limpa.parquet").sort_values("respondido_em_dt").drop_duplicates("user_id", keep="last")
    cum = q.comentario.fillna("").str.lower().str.contains(r"formatura|casamento|prova|viagem|maratona|consegui|cheguei|objetivo|meta|já foi|ja foi|passou|era só|era so")
    ev.append({"ponto": "7. Objetivo com prazo não é usado", "metrica": "comentários da pesquisa de saída que citam meta cumprida ou evento", "valor": f"{cum[q.comentario.notna()].mean()*100:.1f}% dos comentários"})
    pr = q.motivo_principal.eq("preco") & q.comentario.notna()
    ev.append({"ponto": "7. Objetivo com prazo não é usado", "metrica": "quem marcou preço e comentou meta cumprida ou evento", "valor": f"{cum[pr].mean()*100:.1f}%"})

    E = pd.DataFrame(ev)
    E.to_csv(OUT / "pontos_atencao_evidencias.csv", index=False)
    print(E.to_string()); print(camp.to_string())


if __name__ == "__main__":
    main()
