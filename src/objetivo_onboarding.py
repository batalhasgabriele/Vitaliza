"""Extrai motivação e data-alvo do objetivo declarado no onboarding (texto livre).

Regras por expressão regular, sem validação manual: tratar como aproximação.
"""
from __future__ import annotations

import re

import pandas as pd

MESES = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6,
         "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}
MOTIVACOES = {
    "saude_fisica": r"colesterol|dor nas costas|sedent|médico|medico|pressão|pressao|disposi|dormir",
    "saude_mental": r"momento só meu|momento so meu|celular|ansiedade|saúde mental|saude mental|desligar a cabe",
    "social": r"galera|namorad|grupo|pessoal do trabalho|companhia|amiga me chamou|treinar junto",
    "estetica": r"perder|peso|barriga|em forma|espelho|definir|defniir|emagrec|get fit",
    "performance": r"pedal|corrida|crorida|pace|planilha|10k|mais rápido|mais rapido|evoluir",
}
EVENTO_RE = (r"formatura|casamento|prova|viagem|maratona|\b5k\b|verão|verao|mochil|convenç|convenc|"
             r"apresentaç|apresentac|festa|aniversári|aniversari")
PRAZO_RE = r"daqui|\d{1,2}/\d{1,2}|\bdia \d|m[eê]s que vem"


def _motivacao(txt: str) -> str:
    for k, pat in MOTIVACOES.items():
        if re.search(pat, txt):
            return k
    return "nao_informado"


def _proxima(dia: int, mes: int, ref: pd.Timestamp):
    for ano in (ref.year, ref.year + 1):
        try:
            d = pd.Timestamp(year=ano, month=mes, day=min(dia, 28 if mes == 2 else dia))
        except ValueError:
            return None
        if d >= ref:
            return d
    return None


def data_evento(txt: str, ref: pd.Timestamp):
    t = txt.lower()
    meses_re = "|".join(MESES)
    if m := re.search(r"daqui\s+(?:uns\s+)?(\d{1,3})\s*(d|s|m)\w*", t):
        return ref + pd.Timedelta(days=int(m.group(1)) * {"d": 1, "s": 7, "m": 30}[m.group(2)])
    if re.search(r"m[eê]s que vem", t):
        return ref + pd.Timedelta(days=30)
    if (m := re.search(r"\b(\d{1,2})/(\d{1,2})\b", t)) and 1 <= int(m.group(2)) <= 12:
        return _proxima(int(m.group(1)), int(m.group(2)), ref)
    if m := re.search(rf"\b(\d{{1,2}})\s+(?:de\s+)?({meses_re})", t):
        return _proxima(int(m.group(1)), MESES[m.group(2)], ref)
    if m := re.search(rf"(começo|comeco|início|inicio|meio|fim|final)\s+de\s+({meses_re})", t):
        return _proxima({"começo": 5, "comeco": 5, "início": 5, "inicio": 5, "meio": 15}.get(m.group(1), 25), MESES[m.group(2)], ref)
    if m := re.search(rf"\b(?:em|de)\s+({meses_re})", t):
        return _proxima(15, MESES[m.group(1)], ref)
    if m := re.search(r"\bdia\s+(\d{1,2})\b", t):
        d = int(m.group(1)); prox = ref.replace(day=1) + pd.DateOffset(months=0 if d >= ref.day else 1)
        return _proxima(d, prox.month, ref)
    if re.search(r"verão|verao", t):
        return _proxima(21, 12, ref)
    return None


def tratar(onb: pd.DataFrame) -> pd.DataFrame:
    """Recebe onboarding_limpo e devolve user_id, motivacao, tem_prazo e data_evento."""
    o = onb[["user_id", "objetivo_texto", "respondido_em"]].copy()
    ref = pd.to_datetime(o["respondido_em"])
    txt = o["objetivo_texto"].fillna("").str.lower()
    o["motivacao"] = txt.map(_motivacao)
    o["tem_prazo"] = txt.str.contains(EVENTO_RE) | txt.str.contains(PRAZO_RE)
    o.loc[o["tem_prazo"] & o["motivacao"].eq("nao_informado"), "motivacao"] = "so_evento"
    o["data_evento"] = pd.to_datetime([data_evento(t, r) if p else None for t, r, p in zip(txt, ref, o["tem_prazo"])])
    return o[["user_id", "motivacao", "tem_prazo", "data_evento"]]
