from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from analisar_eda_marcos import (  # noqa: E402
    construir_churn_mensal,
    harmonizar_data_utc_para_br,
    two_proportion_p_value,
)


def test_harmonizar_timestamp_misto() -> None:
    result = harmonizar_data_utc_para_br(
        pd.Series(["2026-09-01T02:00:00Z", "2026-09-01 02:00:00"])
    )
    assert result.tolist() == [pd.Timestamp("2026-08-31 23:00:00"), pd.Timestamp("2026-09-01 02:00:00")]


def test_churn_usa_ativos_no_inicio_do_mes() -> None:
    subscriptions = pd.DataFrame(
        {
            "user_id": ["a", "b", "c"],
            "inicio_dt": pd.to_datetime(["2024-01-01", "2024-01-01", "2025-01-15"]),
            "expiracao_br": pd.to_datetime(["2025-01-20", None, None]),
            "plano_atual": ["mensal", "anual", "mensal"],
        }
    )
    churn, _ = construir_churn_mensal(subscriptions)
    january = churn.loc[churn["mes"] == pd.Timestamp("2025-01-01")].iloc[0]
    assert january["ativos_inicio"] == 2
    assert january["perdas"] == 1
    assert january["churn"] == 0.5


def test_two_proportion_identical_rates() -> None:
    assert two_proportion_p_value(10, 100, 20, 200) == 1.0
