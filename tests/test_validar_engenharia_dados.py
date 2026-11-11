import sys
from pathlib import Path
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from validar_engenharia_dados import comparar


def test_comparacao_independe_da_ordem_e_preserva_nulos():
    a = pd.DataFrame({'user_id': [1, 2], 'valor': [None, 4.0]})
    assert comparar(a, a.iloc[::-1])['colunas_alteradas'] == []


def test_nao_confunde_ausencia_com_zero():
    a = pd.DataFrame({'user_id': [1, 2], 'valor': [None, 4.0]})
    assert comparar(a, a.fillna(0))['colunas_alteradas'] == ['valor']


def test_detecta_populacao_diferente_e_chave_duplicada():
    a = pd.DataFrame({'user_id': [1, 2], 'valor': [2, 4]})
    assert not comparar(a, a.iloc[:1])['populacao_igual']
    with pytest.raises(ValueError):
        comparar(a, pd.concat([a, a]))
