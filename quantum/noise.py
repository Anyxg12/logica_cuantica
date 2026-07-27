from dataclasses import dataclass

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import (
    DensityMatrix,
    Statevector,
    state_fidelity,
)
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
)

from quantum.engine import (
    crear_circuito_preparacion,
    crear_circuito_recuperacion,
)


@dataclass(frozen=True)
class ResultadoRuido:
    """
    Resultado de ejecutar el circuito de recuperación
    bajo un modelo de ruido despolarizante.
    """

    theta_grados: float
    phi_grados: float
    nivel_ruido: float
    fidelidad: float
    estado_ideal: Statevector
    estado_ruidoso: DensityMatrix
    circuito_original: QuantumCircuit
    circuito_transpilado: QuantumCircuit


def validar_nivel_ruido(
    nivel_ruido: float,
) -> None:
    """
    Restringe el nivel de ruido a un intervalo pedagógico.

    Se utiliza un máximo de 0.30 para evitar valores
    excesivos y conservar una visualización comprensible.
    """

    if not 0.0 <= nivel_ruido <= 0.30:
        raise ValueError(
            "El nivel de ruido debe estar entre 0.0 y 0.30."
        )


def crear_modelo_ruido(
    nivel_ruido: float,
) -> NoiseModel:
    """
    Crea un modelo simplificado de ruido despolarizante.

    El error de dos cúbits se hace ligeramente mayor,
    porque las operaciones de varios cúbits suelen ser
    más sensibles dentro de este modelo pedagógico.
    """

    validar_nivel_ruido(nivel_ruido)

    modelo = NoiseModel()

    if nivel_ruido == 0:
        return modelo

    error_un_qubit = depolarizing_error(
        nivel_ruido,
        1,
    )

    error_dos_qubits = depolarizing_error(
        min(nivel_ruido * 1.5, 0.30),
        2,
    )

    # Puertas posibles después de la transpilación.
    puertas_un_qubit = [
        "x",
        "sx",
        "h",
        "ry",
        "rz",
    ]

    modelo.add_all_qubit_quantum_error(
        error_un_qubit,
        puertas_un_qubit,
    )

    modelo.add_all_qubit_quantum_error(
        error_dos_qubits,
        ["cx"],
    )

    return modelo


def preparar_circuito_ruidoso(
    theta_grados: float,
    phi_grados: float,
) -> QuantumCircuit:
    """
    Construye el circuito de recuperación y añade
    una instrucción para guardar la matriz de densidad.
    """

    circuito = crear_circuito_recuperacion(
        theta_grados,
        phi_grados,
    ).copy()

    circuito.save_density_matrix(
        label="estado_final",
    )

    return circuito


def ejecutar_con_ruido(
    theta_grados: float,
    phi_grados: float,
    nivel_ruido: float,
) -> ResultadoRuido:
    """
    Ejecuta la recuperación bajo ruido despolarizante
    y compara el resultado con el estado ideal.
    """

    validar_nivel_ruido(nivel_ruido)

    modelo_ruido = crear_modelo_ruido(
        nivel_ruido
    )

    simulador = AerSimulator(
        method="density_matrix",
        noise_model=modelo_ruido,
    )

    circuito = preparar_circuito_ruidoso(
        theta_grados,
        phi_grados,
    )

    circuito_transpilado = transpile(
        circuito,
        simulador,
        optimization_level=0,
    )

    resultado_simulacion = simulador.run(
        circuito_transpilado
    ).result()

    datos = resultado_simulacion.data(0)

    estado_ruidoso = DensityMatrix(
        datos["estado_final"]
    )

    # El objetivo ideal es el estado preparado originalmente:
    # primer cúbit con θ y φ; los demás en |0>.
    circuito_ideal = crear_circuito_preparacion(
        theta_grados,
        phi_grados,
    )

    estado_ideal = Statevector.from_instruction(
        circuito_ideal
    )

    fidelidad_calculada = float(
    state_fidelity(
        estado_ideal,
        estado_ruidoso,
    )
)

      # La fidelidad matemática pertenece al intervalo [0, 1].
     # Corregimos únicamente pequeños excesos numéricos
      # producidos por operaciones de coma flotante.
    fidelidad = max(
      0.0,
      min(1.0, fidelidad_calculada),
    )

    return ResultadoRuido(
        theta_grados=theta_grados,
        phi_grados=phi_grados,
        nivel_ruido=nivel_ruido,
        fidelidad=fidelidad,
        estado_ideal=estado_ideal,
        estado_ruidoso=estado_ruidoso,
        circuito_original=circuito,
        circuito_transpilado=circuito_transpilado,
    )


def generar_curva_ruido(
    theta_grados: float,
    phi_grados: float,
    niveles: list[float] | None = None,
) -> list[ResultadoRuido]:
    """
    Ejecuta el circuito con distintos niveles de ruido.

    El resultado permite construir posteriormente una
    gráfica de fidelidad frente a ruido.
    """

    if niveles is None:
        niveles = [
            0.00,
            0.01,
            0.02,
            0.05,
            0.08,
            0.10,
            0.15,
            0.20,
            0.25,
            0.30,
        ]

    return [
        ejecutar_con_ruido(
            theta_grados=theta_grados,
            phi_grados=phi_grados,
            nivel_ruido=nivel,
        )
        for nivel in niveles
    ]


if __name__ == "__main__":
    theta = 120
    phi = 95

    print(
        f"Estado probado: θ={theta}°, φ={phi}°"
    )

    print("\nRuido      Fidelidad")
    print("-" * 28)

    resultados = generar_curva_ruido(
        theta_grados=theta,
        phi_grados=phi,
    )

    for resultado in resultados:
        print(
            f"{resultado.nivel_ruido:0.2f}"
            f"        "
            f"{resultado.fidelidad:0.8f}"
        )