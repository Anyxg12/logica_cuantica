import pytest

from quantum.engine import ejecutar_motor


@pytest.mark.parametrize(
    "theta, phi",
    [
        (0, 0),
        (180, 0),
        (90, 0),
        (90, 90),
        (60, 210),
        (35, 320),
    ],
)
def test_motor_recupera_estados_generales(
    theta: float,
    phi: float,
) -> None:
    """
    Comprueba que el circuito inverso recupera estados
    con diferentes amplitudes y fases.
    """
    resultado = ejecutar_motor(theta, phi)

    assert resultado.fidelidad == pytest.approx(
        1.0,
        abs=1e-12,
    )

    assert resultado.estado_inicial.equiv(
        resultado.estado_recuperado
    )


@pytest.mark.parametrize(
    "theta, phi",
    [
        (-1, 0),
        (181, 0),
        (90, -1),
        (90, 361),
    ],
)
def test_motor_rechaza_angulos_invalidos(
    theta: float,
    phi: float,
) -> None:
    """Comprueba la validación de los parámetros."""
    with pytest.raises(ValueError):
        ejecutar_motor(theta, phi)


@pytest.mark.parametrize(
    "theta, phi",
    [
        (0, 0),
        (90, 45),
        (180, 360),
    ],
)
def test_estado_inicial_esta_normalizado(
    theta: float,
    phi: float,
) -> None:
    """Comprueba que la suma de probabilidades sea uno."""
    resultado = ejecutar_motor(theta, phi)

    probabilidad_total = sum(
        abs(amplitud) ** 2
        for amplitud in resultado.estado_inicial.data
    )

    assert probabilidad_total == pytest.approx(
        1.0,
        abs=1e-12,
    )