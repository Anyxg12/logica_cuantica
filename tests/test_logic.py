from logic.irreversible import detectar_colisiones
from logic.reversible import comprobar_recuperacion, tiene_colisiones


def test_and_tiene_colisiones():
    colisiones = detectar_colisiones()

    assert 0 in colisiones
    assert colisiones[0] == [(0, 0), (0, 1), (1, 0)]


def test_cnot_no_tiene_colisiones():
    assert tiene_colisiones() is False


def test_cnot_recupera_todas_las_entradas():
    resultados = comprobar_recuperacion()

    assert all(resultados.values())