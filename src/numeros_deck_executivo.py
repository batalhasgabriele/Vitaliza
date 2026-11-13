"""Números complementares e auditoria do deck executivo (Semana 5).

Complementa a consolidação da ADR 020 (`src/consolidar_semana5.py`) com os números do deck que não
estão nas tabelas consolidadas. Lê só a camada Prata e grava apenas agregados (GOV-004).

Saídas em `saidas/deck_executivo/auditoria/`:
- `numeros_deck.json`: receita dos últimos 12 meses, qualidade de contas, poder do piloto, público
  ampliado de formação de hábito, taxa de não renovação por canal corrigida para censura;
- `entropia_fatores.csv`: quanto da incerteza sobre a perda de acesso em 60 dias cada fator explica,
  em cortes fixos (31/05 e 31/07), com atributos medidos só até o corte;
- `evento_corte_fixo.csv`: saída em 60 dias por fase do objetivo com data, em corte fixo;
- `treinos_antes_da_saida.csv`: trajetória retrospectiva de treinos antes da saída.

Uso:
    python src/numeros_deck_executivo.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import segmentacao_base_inteira as base  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
PRATA = ROOT / "dados" / "processados" / "prata"
OUT = ROOT / "saidas" / "deck_executivo" / "auditoria"
CORTE = pd.Timestamp("2026-09-30 23:59:59")
CORTES = [pd.Timestamp("2026-05-31 23:59:59"), pd.Timestamp("2026-07-31 23:59:59")]
HORIZONTE = pd.Timedelta(days=60)
OUTDOOR = {"corrida", "caminhada", "pedal"}


def entropia(p: np.ndarray) -> float:
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def info_mutua(x: pd.Series, y: pd.Series) -> float:
    ct = pd.crosstab(x, y).to_numpy(dtype=float)
    pxy = ct / ct.sum()
    esperado = pxy.sum(1, keepdims=True) @ pxy.sum(0, keepdims=True)
    nz = pxy > 0
    return float((pxy[nz] * np.log2(pxy[nz] / esperado[nz])).sum())


def ultimo_toggle(ev: pd.DataFrame, ate: pd.Timestamp) -> pd.Series:
    t = ev[ev["evento"].isin(["renovacao_automatica_desligada", "renovacao_automatica_religada"]) & (ev["d"] <= ate)]
    return t.sort_values("d").groupby("user_id")["evento"].last()


def mde(p: float, n_por_braco: int) -> float:
    """Menor diferença detectável (p.p.), bicaudal 5%, poder 80%, dois braços iguais."""
    return 2.8016 * np.sqrt(2 * p * (1 - p) / n_por_braco) * 100


def coorte(b, at, ev, am, pg, t):
    c = b[(b["ini"] <= t) & (b["fim"].isna() | (b["fim"] > t))].copy()
    c["y"] = c["fim"].notna() & (c["fim"] <= t + HORIZONTE)
    w = at[(at["d"] > t - pd.Timedelta(days=84)) & (at["d"] <= t) & at["user_id"].isin(c["user_id"])]
    w = w.assign(semana=(t - w["d"]).dt.days // 7, fora=w["tipo_canonico"].isin(OUTDOOR))
    g = w.groupby("user_id").agg(treinos=("d", "size"), semanas=("semana", "nunique"), fora=("fora", "mean"))
    c = c.join(g, on="user_id")
    c[["treinos", "semanas"]] = c[["treinos", "semanas"]].fillna(0)
    expo = ((t - c["ini"]).dt.days.clip(upper=84) / 7).clip(lower=1)
    c["constancia"] = pd.cut((c["semanas"] / expo).clip(upper=1), [-.01, .25, .5, .75, 1.01], labels=["<25%", "25-50%", "50-75%", "75%+"])
    c["treinos_84d"] = pd.cut(c["treinos"], [-1, 0, 5, 15, 30, 1e9], labels=["0", "1-5", "6-15", "16-30", "31+"])
    c["modo"] = np.where(c["treinos"] == 0, "sem treino", np.where(c["fora"] >= .5, "ar livre", "casa"))
    c["renovacao_desligada"] = c["user_id"].map(ultimo_toggle(ev, t)).eq("renovacao_automatica_desligada")
    d = (c["data_evento"] - t).dt.days
    c["evento"] = np.select([~c["tem_prazo"], c["data_evento"].isna(), d.between(0, 60), d.between(-60, -1), d > 60],
                            ["sem prazo", "prazo sem data", "nos próximos 60 dias", "nos últimos 60 dias", "depois de 60 dias"], "passou há 60+ dias")
    c["recusa_previa"] = c["user_id"].isin(pg.loc[(pg["status"] == "recusado") & (pg["d"] <= t), "user_id"])
    c["tempo_de_casa"] = pd.cut((t - c["ini"]).dt.days / 30.44, [-1, 1, 3, 6, 12, 1e9], labels=["<1m", "1-3m", "3-6m", "6-12m", "12m+"])
    a = am[am["desde_dt"] <= t]
    con = a.groupby("seguido_id").size().add(a.groupby("seguidor_id").size(), fill_value=0)
    c["conexoes_no_corte"] = pd.cut(c["user_id"].map(con).fillna(0), [-1, 0, 2, 5, 1e9], labels=["0", "1-2", "3-5", "6+"])
    c["idade_faixa"] = pd.cut(c["idade"], [0, 35, 45, 55, 65, 120]).astype(str)
    return c


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    b = base.construir()
    at = pd.read_parquet(PRATA / "atividades_limpas.parquet", columns=["user_id", "inicio_dt_br", "tipo_canonico"])
    at["d"] = pd.to_datetime(at["inicio_dt_br"])
    ev = pd.read_parquet(PRATA / "eventos_assinatura_limpos.parquet")
    ev["d"] = pd.to_datetime(ev["data_hora_br"])
    am = pd.read_parquet(PRATA / "amizades_limpas.parquet")
    am = am[~am["flag_apos_corte"]].assign(desde_dt=lambda x: pd.to_datetime(x["desde_dt"]))
    pg = pd.read_parquet(PRATA / "pagamentos_limpos.parquet")
    pg["d"] = pd.to_datetime(pg["data_hora_br"])
    a = pd.read_parquet(PRATA / "assinaturas_limpas.parquet")
    a["ini"], a["fimd"] = pd.to_datetime(a["inicio"]), pd.to_datetime(a["data_fim"])
    u = pd.read_parquet(PRATA / "usuarios_limpo.parquet")

    # 1) entropia dos fatores em cortes fixos
    fatores = ["renovacao_desligada", "plano_atual", "constancia", "treinos_84d", "tempo_de_casa", "evento", "modo",
               "recusa_previa", "conexoes_no_corte", "motivacao", "canal_aquisicao", "canal_cobranca", "nivel",
               "sexo", "idade_faixa", "uf", "relogio_conectado", "sistema"]
    linhas, evento = [], []
    for t in CORTES:
        c = coorte(b, at, ev, am, pg, t)
        hy = entropia(c["y"].value_counts(normalize=True).to_numpy())
        for f in fatores:
            x = c[f].astype(str)
            r = c.groupby(x)["y"].agg(["mean", "size"])
            r = r[r["size"] >= 100]
            mi = info_mutua(x, c["y"])
            linhas.append({"corte": t.date().isoformat(), "fator": f, "n": len(c), "taxa_base_pct": c["y"].mean() * 100,
                           "entropia_desfecho_bits": hy, "info_mutua_bits": mi, "incerteza_explicada_pct": mi / hy * 100,
                           "taxa_min_pct": r["mean"].min() * 100, "taxa_max_pct": r["mean"].max() * 100})
        e = c.groupby("evento")["y"].agg(clientes="size", saida_60d_pct="mean").reset_index()
        evento.append(e.assign(corte=t.date().isoformat(), saida_60d_pct=e["saida_60d_pct"] * 100))
    pd.DataFrame(linhas).round(4).to_csv(OUT / "entropia_fatores.csv", index=False)
    pd.concat(evento).round(2).to_csv(OUT / "evento_corte_fixo.csv", index=False)

    # 2) trajetória de treinos antes da saída (retrospectiva, todas as assinaturas em vigor em 2026)
    s = b[~b["provisorio"] & (b["exposicao_dias"] >= 120)].copy()
    w = at[at["user_id"].isin(s["user_id"])].copy()
    w["dias"] = (w["user_id"].map(s.set_index("user_id")["fim_exp"]) - w["d"]).dt.days
    w = w[w["dias"].between(0, 120)]
    w["janela"] = pd.cut(w["dias"], [-1, 30, 60, 90, 120], labels=["0-30", "31-60", "61-90", "91-120"])
    cnt = w.groupby(["user_id", "janela"], observed=False).size().unstack(fill_value=0)
    s = s.join(cnt, on="user_id")
    jan = ["91-120", "61-90", "31-60", "0-30"]
    s[jan] = s[jan].fillna(0)
    s.groupby(["saiu_na_janela", "plano_atual"])[jan].mean().round(2).reset_index().to_csv(OUT / "treinos_antes_da_saida.csv", index=False)

    # 3) números avulsos do deck
    ok = pg[pg["status"].eq("aprovado") & ~pg["flag_duplicata_aprovada_dia"]]
    rec = ok.groupby(ok["d"].dt.to_period("M"))["valor_liquido"].sum()
    ativos_ids = set(a.loc[a["status_atual"].eq("ativa"), "user_id"])
    f = pd.read_parquet(PRATA / "feed_posts_limpos.parquet", columns=["user_id"])
    email = u["email"].str.lower().str.strip()

    t = CORTES[1]
    c = coorte(b, at, ev, am, pg, t)
    desl = c[c["renovacao_desligada"]]
    tg60 = ultimo_toggle(ev, t + HORIZONTE)
    ativo60 = desl["fim"].isna() | (desl["fim"] > t + HORIZONTE)
    religou = desl["user_id"].map(tg60).eq("renovacao_automatica_religada")
    p0 = float((ativo60 & religou).mean())

    ativos = b[b["fim"].isna()].copy()
    novos_mensal = ativos[ativos["plano_atual"].eq("mensal") & (ativos["ini"] > CORTE - pd.Timedelta(days=90)) & ~ativos["renovacao_desligada_corte"]]

    an = a[a["plano_atual"].eq("anual") & a["ini"].between("2024-01-01", "2025-08-31")].merge(u[["user_id", "canal_aquisicao"]], on="user_id")
    an["nao_renovou"] = an["fimd"].notna() & (an["fimd"] <= an["ini"] + pd.Timedelta(days=380))
    infl = an.groupby(an["canal_aquisicao"].eq("influenciador"))["nao_renovou"].agg(["mean", "size"])

    numeros = {
        "receita_liquida_set26": round(float(rec[pd.Period("2026-09")]), 2),
        "receita_liquida_set26_x12": round(float(rec[pd.Period("2026-09")] * 12), 2),
        "receita_liquida_ultimos_12m": round(float(rec[pd.Period("2025-10"):pd.Period("2026-09")].sum()), 2),
        "receita_liquida_jan_set_2025": round(float(rec[pd.Period("2025-01"):pd.Period("2025-09")].sum()), 2),
        "receita_liquida_jan_set_2026": round(float(rec[pd.Period("2026-01"):pd.Period("2026-09")].sum()), 2),
        "contas": len(u), "contas_internas": int(u["flag_conta_interna"].astype(bool).sum()),
        "contas_com_email_repetido": int(email.duplicated(keep=False).sum()),
        "pct_treinos_de_nao_pagantes_ativos": round(float((~at["user_id"].isin(ativos_ids)).mean() * 100), 1),
        "pct_posts_de_nao_pagantes_ativos": round(float((~f["user_id"].isin(ativos_ids)).mean() * 100), 1),
        "piloto_renovacao_desligada": {
            "corte_referencia": t.date().isoformat(), "elegiveis_no_corte_ref": int(len(desl)),
            "taxa_base_ativa_e_religada_60d_pct": round(p0 * 100, 1),
            "mde_pp_200_por_braco": round(mde(p0, 200), 1), "mde_pp_1127_por_braco": round(mde(p0, 1127), 1),
        },
        "mensal_ate_90_dias_renovacao_ligada": {"clientes": int(len(novos_mensal)),
                                                "receita_equivalente": round(float(novos_mensal["receita_liquida_mensal_equiv"].sum()), 2)},
        "anual_nao_renova_1o_ano_pct": {"influenciador": round(float(infl.loc[True, "mean"] * 100), 1),
                                        "demais_canais": round(float(infl.loc[False, "mean"] * 100), 1),
                                        "n_influenciador": int(infl.loc[True, "size"]), "n_demais": int(infl.loc[False, "size"]),
                                        "entradas": "anuais iniciados de 01/2024 a 08/2025 (aniversário observável até o corte)"},
    }
    (OUT / "numeros_deck.json").write_text(json.dumps(numeros, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(numeros, ensure_ascii=False, indent=1))
    e = pd.read_csv(OUT / "entropia_fatores.csv")
    print(e.pivot(index="fator", columns="corte", values="incerteza_explicada_pct").round(2).sort_values("2026-07-31", ascending=False))
    print(pd.read_csv(OUT / "evento_corte_fixo.csv").to_string())
    print(pd.read_csv(OUT / "treinos_antes_da_saida.csv").to_string())


if __name__ == "__main__":
    main()
