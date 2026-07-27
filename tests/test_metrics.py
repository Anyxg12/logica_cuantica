import pytest

from quantum.engine import ejecutar_motor
from quantum.metrics import (
    calcular_metricas_qubit,
    calcular_metricas_sistema,
)


def test_estado_inicial_tiene_qubits_puros() -> None:
    resultado = ejecutar_motor(
        theta_grados=120,
        phi_grados=95,
    )

    metricas = calcular_metricas_sistema(
        resultado.estado_inicial
    )

    for qubit in metricas:
        assert qubit.entropia == pytest.approx(
            0.0,
            abs=1e-12,
        )
        assert qubit.pureza == pytest.approx(
            1.0,
            abs=1e-12,
        )


def test_distribucion_genera_estados_locales_mezclados() -> None:
    resultado = ejecutar_motor(
        theta_grados=120,
        phi_grados=95,
    )

    metricas = calcular_metricas_sistema(
        resultado.estado_distribuido
    )

    for qubit in metricas:
        assert qubit.entropia > 0.9
        assert qubit.pureza < 0.6


def test_recuperacion_devuelve_qubits_puros() -> None:
    resultado = ejecutar_motor(
        theta_grados=120,
        phi_grados=95,
    )

    metricas = calcular_metricas_sistema(
        resultado.estado_recuperado
    )

    for qubit in metricas:
        assert qubit.entropia == pytest.approx(
            0.0,
            abs=1e-12,
        )
        assert qubit.pureza == pytest.approx(
            1.0,
            abs=1e-12,
        )


def test_rechaza_indice_de_qubit_invalido() -> None:
    resultado = ejecutar_motor(
        theta_grados=90,
        phi_grados=0,
    )

    with pytest.raises(ValueError):
        calcular_metricas_qubit(
            resultado.estado_inicial,
            qubit=3,
        )
        