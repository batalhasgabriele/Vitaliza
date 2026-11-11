import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from validar_entrega_semana5 import intervalo_diferenca


def test_intervalo_simetrico_sem_diferenca():
    lo, hi = intervalo_diferenca(50, 1000, 50, 1000)
    assert lo < 0 < hi
    assert np.isclose(-lo, hi)


def test_trocar_bracos_inverte_intervalo():
    lo, hi = intervalo_diferenca(161, 3472, 196, 3579)
    a, b = intervalo_diferenca(196, 3579, 161, 3472)
    assert np.isclose(lo, -b) and np.isclose(hi, -a)
