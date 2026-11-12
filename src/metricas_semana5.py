"""Definições testáveis: estados no tempo, proporções, exposição e coortes."""
from statistics import NormalDist
import numpy as np
import pandas as pd

ESTADOS = {"assinatura_iniciada": True, "renovacao": True, "periodo_carencia": True,
           "assinatura_expirada": False, "reembolso": False}
RENOVACAO = {"renovacao_automatica_desligada": False,
             "renovacao_automatica_religada": True}


def estado_no_corte(assinaturas, eventos, corte):
    """Sem consultar status_atual/data_fim. Início é a primeira cobrança.

    Renovações não religam automaticamente opt-out; somente evento explícito.
    Ausência de evento de toggle implica renovação ligada; hipótese auditável.
    Chargeback isolado é financeiro: não implica perda de acesso sem expiração.
    """
    a = assinaturas.set_index("user_id").copy()
    inicio = pd.to_datetime(a["inicio"])
    ev = eventos.loc[pd.to_datetime(eventos["data_hora_br"]) <= corte].sort_values("data_hora_br")
    status = ev[ev.evento.isin(ESTADOS)].groupby("user_id").evento.last().map(ESTADOS)
    ligada = ev[ev.evento.isin(RENOVACAO)].groupby("user_id").evento.last().map(RENOVACAO)
    out = pd.DataFrame(index=a.index)
    out["ativa"] = (inicio <= corte) & status.reindex(a.index).astype('boolean').fillna(True).astype(bool)
    out["renovacao_ligada"] = ligada.reindex(a.index).astype('boolean').fillna(True).astype(bool)
    for col in ["plano", "canal_cobranca"]:
        last = ev.dropna(subset=[col]).groupby("user_id")[col].last()
        fallback = a["plano_atual" if col == "plano" else col]
        out[col] = last.reindex(a.index).fillna(fallback)
    return out


def wilson(eventos, n):
    if not n:
        return np.nan, np.nan
    z = NormalDist().inv_cdf(.975)
    p = eventos / n
    den = 1 + z*z/n
    centro = (p + z*z/(2*n)) / den
    erro = z * np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
    return centro-erro, centro+erro


def diferenca_proporcoes(e1, n1, e0, n0):
    if not n1 or not n0:
        return (np.nan,)*4
    p1, p0 = e1/n1, e0/n0
    d = p1-p0
    se = np.sqrt(p1*(1-p1)/n1+p0*(1-p0)/n0)
    pool = (e1+e0)/(n1+n0)
    se0 = np.sqrt(pool*(1-pool)*(1/n1+1/n0))
    pv = 2*(1-NormalDist().cdf(abs(d/se0))) if se0 else 1.
    return d*100, (d-1.96*se)*100, (d+1.96*se)*100, pv


def exposicao_meses(dias):
    """Tempo observado real, sem arredondar um cliente-dia a um cliente-mês."""
    return pd.Series(dias).clip(lower=1)/30.4375


def fase_evento(dias):
    return np.select([dias.isna(), dias.gt(60), dias.ge(-60)],
                     ["sem data validada", "mais de 60 dias à frente", "evento ±60 dias"],
                     "evento há mais de 60 dias")


def proporcao_saida_90d(a, corte):
    """Coorte incidente com 90 dias completos; não condicionar à sobrevivência."""
    inicio, fim = pd.to_datetime(a.inicio), pd.to_datetime(a.data_fim)
    elig = (inicio >= pd.Timestamp("2025-01-01")) & (inicio + pd.Timedelta(days=90) <= corte)
    saiu = fim.notna() & (fim <= inicio + pd.Timedelta(days=90))
    rows = []
    for plano in ["mensal", "anual"]:
        mask = elig & a.plano_atual.eq(plano)
        n, e = int(mask.sum()), int((mask&saiu).sum())
        lo, hi = wilson(e,n)
        rows.append(dict(plano=plano,n=n,saidas_90d=e,taxa=e/n if n else np.nan,ic95_inf=lo,ic95_sup=hi))
    return pd.DataFrame(rows)
