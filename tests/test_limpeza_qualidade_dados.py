from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from limpeza_qualidade_dados import (  # noqa: E402
    harmonizar_data_utc_para_br,
    limpar_valor_monetario,
)


def test_harmonizar_data_preserva_brasilia_e_converte_utc() -> None:
    values = pd.Series(["2026-09-01T02:30:00Z", "2026-09-01 02:30:00"])

    result = harmonizar_data_utc_para_br(values)

    assert result.iloc[0] == pd.Timestamp("2026-08-31 23:30:00")
    assert result.iloc[1] == pd.Timestamp("2026-09-01 02:30:00")


def test_limpar_valor_monetario() -> None:
    values = pd.Series(["R$ 39,90", "299.90"])

    result = limpar_valor_monetario(values)

    assert result.tolist() == [39.9, 299.9]
