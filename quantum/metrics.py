from dataclasses import dataclass

from qiskit.quantum_info import (
    DensityMatrix,
    Statevector,
    entropy,
    partial_trace,
    purity,
)


@dataclass(frozen=True)
class MetricasQubit:
    """
    Métricas del estado local de un cúbit.

    entropia:
        Mide qué tan mezclado aparece el cúbit al observarlo
        separado del resto del sistema.

    pureza:
        Vale 1 para un estado puro y disminuye cuando el estado
        local es una mezcla.
    """

    qubit: int
    entropia: float
    pureza: float
    estado_reducido: DensityMatrix


def obtener_estado_reducido(
    estado: Statevector,
    qubit: int,
) -> DensityMatrix:
    """
    Obtiene la matriz de densidad de un solo cúbit.

    Para conservar el cúbit seleccionado, se eliminan
    matemáticamente los demás mediante la traza parcial.
    """

    numero_qubits = estado.num_qubits

    if qubit < 0 or qubit >= numero_qubits:
        raise ValueError(
            f"El cúbit debe estar entre 0 y {numero_qubits - 1}."
        )

    qubits_a_eliminar = [
        indice
        for indice in range(numero_qubits)
        if indice != qubit
    ]

    return partial_trace(
        estado,
        qubits_a_eliminar,
    )


def calcular_metricas_qubit(
    estado: Statevector,
    qubit: int,
) -> MetricasQubit:
    """
    Calcula entropía y pureza para un cúbit individual.
    """

    estado_reducido = obtener_estado_reducido(
        estado,
        qubit,
    )

    entropia_local = float(
        entropy(
            estado_reducido,
            base=2,
        )
    )

    pureza_local = float(
        purity(estado_reducido).real
    )

    # Limpiamos pequeños errores numéricos.
    if abs(entropia_local) < 1e-12:
        entropia_local = 0.0

    if abs(pureza_local - 1.0) < 1e-12:
        pureza_local = 1.0

    return MetricasQubit(
        qubit=qubit,
        entropia=entropia_local,
        pureza=pureza_local,
        estado_reducido=estado_reducido,
    )


def calcular_metricas_sistema(
    estado: Statevector,
) -> list[MetricasQubit]:
    """
    Calcula las métricas locales de todos los cúbits.
    """

    return [
        calcular_metricas_qubit(
            estado,
            qubit,
        )
        for qubit in range(estado.num_qubits)
    ]


if __name__ == "__main__":
    from quantum.engine import ejecutar_motor

    resultado = ejecutar_motor(
        theta_grados=120,
        phi_grados=95,
    )

    etapas = {
        "Inicial": resultado.estado_inicial,
        "Distribuido": resultado.estado_distribuido,
        "Recuperado": resultado.estado_recuperado,
    }

    for nombre, estado in etapas.items():
        print("\n" + "=" * 50)
        print(nombre)

        for metricas in calcular_metricas_sistema(estado):
            print(
                f"Qubit {metricas.qubit}: "
                f"entropía={metricas.entropia:.6f}, "
                f"pureza={metricas.pureza:.6f}"
            )