import pytest

from quantum.noise import (
    ejecutar_con_ruido,
    generar_curva_ruido,
)


def test_ruido_cero_conserva_fidelidad() -> None:
    """
    Sin ruido, la recuperación debe coincidir
    prácticamente con el estado ideal.
    """
    resultado = ejecutar_con_ruido(
        theta_grados=120,
        phi_grados=95,
        nivel_ruido=0.0,
    )

    assert resultado.fidelidad == pytest.approx(
        1.0,
        abs=1e-12,
    )


def test_ruido_alto_reduce_fidelidad() -> None:
    """
    Un nivel significativo de ruido debe producir
    menor fidelidad que el modelo ideal.
    """
    resultado_ideal = ejecutar_con_ruido(
        theta_grados=120,
        phi_grados=95,
        nivel_ruido=0.0,
    )

    resultado_ruidoso = ejecutar_con_ruido(
        theta_grados=120,
        phi_grados=95,
        nivel_ruido=0.20,
    )

    assert (
        resultado_ruidoso.fidelidad
        < resultado_ideal.fidelidad
    )


@pytest.mark.parametrize(
    "nivel_invalido",
    [
        -0.01,
        -1.0,
        0.31,
        1.0,
    ],
)
def test_rechaza_niveles_invalidos(
    nivel_invalido: float,
) -> None:
    """
    El modelo solo acepta niveles entre 0 y 0.30.
    """
    with pytest.raises(ValueError):
        ejecutar_con_ruido(
            theta_grados=90,
            phi_grados=0,
            nivel_ruido=nivel_invalido,
        )


def test_curva_contiene_todos_los_niveles() -> None:
    niveles = [
        0.0,
        0.05,
        0.10,
        0.20,
    ]

    resultados = generar_curva_ruido(
        theta_grados=120,
        phi_grados=95,
        niveles=niveles,
    )

    niveles_obtenidos = [
        resultado.nivel_ruido
        for resultado in resultados
    ]

    assert niveles_obtenidos == niveles
    assert len(resultados) == len(niveles)


def test_fidelidades_estan_en_rango_valido() -> None:
    resultados = generar_curva_ruido(
        theta_grados=120,
        phi_grados=95,
        niveles=[
            0.0,
            0.05,
            0.10,
            0.20,
            0.30,
        ],
    )

    for resultado in resultados:
        assert 0.0 <= resultado.fidelidad <= 1.0