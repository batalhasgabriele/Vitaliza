from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from segmentacao_clientes import divisao_segura, escolher_k  # noqa: E402


def test_divisao_segura_trata_zero_sem_infinito() -> None:
    numerador = pd.Series([2.0, 3.0, 0.0])
    denominador = pd.Series([1.0, 0.0, 0.0])

    resultado = divisao_segura(numerador, denominador)

    assert resultado.tolist() == [2.0, 0.0, 0.0]
    assert np.isfinite(resultado).all()


def test_escolher_k_restringe_a_tres_ou_quatro_e_tamanho_minimo() -> None:
    metricas = pd.DataFrame(
        {
            "k": [3, 4, 5],
            "silhouette_amostra": [0.31, 0.35, 0.50],
            "estabilidade_ari": [0.90, 0.88, 0.95],
            "menor_cluster_pct": [18.0, 7.0, 4.0],
        }
    )

    assert escolher_k(metricas) == 4


def test_escolher_k_descarta_cluster_menor_que_cinco_porcento() -> None:
    metricas = pd.DataFrame(
        {
            "k": [3, 4],
            "silhouette_amostra": [0.30, 0.45],
            "estabilidade_ari": [0.90, 0.92],
            "menor_cluster_pct": [20.0, 3.0],
        }
    )

    assert escolher_k(metricas) == 3
