from dataclasses import dataclass
from math import radians

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity


@dataclass(frozen=True)
class ResultadoMotor:
    """
    Agrupa todos los resultados importantes de una simulación.

    frozen=True impide modificar accidentalmente los valores
    después de crear el resultado.
    """

    theta_grados: float
    phi_grados: float
    estado_inicial: Statevector
    estado_distribuido: Statevector
    estado_recuperado: Statevector
    fidelidad: float
    circuito_preparacion: QuantumCircuit
    circuito_distribucion: QuantumCircuit
    circuito_recuperacion: QuantumCircuit


def validar_angulos(
    theta_grados: float,
    phi_grados: float,
) -> None:
    """
    Comprueba que los ángulos estén dentro del rango utilizado
    por la representación de la esfera de Bloch.
    """

    if not 0 <= theta_grados <= 180:
        raise ValueError(
            "Theta debe encontrarse entre 0 y 180 grados."
        )

    if not 0 <= phi_grados <= 360:
        raise ValueError(
            "Phi debe encontrarse entre 0 y 360 grados."
        )


def crear_circuito_preparacion(
    theta_grados: float,
    phi_grados: float,
) -> QuantumCircuit:
    """
    Prepara un estado cuántico general en el primer cúbit.

    Los cúbits 1 y 2 permanecen en |0>.
    """

    validar_angulos(theta_grados, phi_grados)

    theta = radians(theta_grados)
    phi = radians(phi_grados)

    circuito = QuantumCircuit(3, name="Preparación")

    # RY controla la proporción entre |0> y |1>.
    circuito.ry(theta, 0)

    # RZ añade una fase relativa.
    circuito.rz(phi, 0)

    return circuito


def crear_bloque_distribucion() -> QuantumCircuit:
    """
    Construye la transformación unitaria que distribuye
    la información entre los tres cúbits.
    """

    bloque = QuantumCircuit(3, name="U_mezcla")

    bloque.h(0)
    bloque.cx(0, 1)
    bloque.cx(1, 2)

    return bloque


def crear_circuito_distribucion(
    theta_grados: float,
    phi_grados: float,
) -> QuantumCircuit:
    """
    Prepara el estado y después distribuye su información
    entre los tres cúbits.
    """

    circuito = crear_circuito_preparacion(
        theta_grados,
        phi_grados,
    )

    bloque_distribucion = crear_bloque_distribucion()

    circuito.barrier()
    circuito.compose(
        bloque_distribucion,
        inplace=True,
    )

    return circuito


def crear_circuito_recuperacion(
    theta_grados: float,
    phi_grados: float,
) -> QuantumCircuit:
    """
    Prepara, distribuye y recupera el estado aplicando
    la transformación inversa.
    """

    circuito = crear_circuito_preparacion(
        theta_grados,
        phi_grados,
    )

    bloque_distribucion = crear_bloque_distribucion()

    circuito.barrier()

    # Aplicamos la transformación de distribución.
    circuito.compose(
        bloque_distribucion,
        inplace=True,
    )

    circuito.barrier()

    # Qiskit genera automáticamente la transformación inversa.
    circuito.compose(
        bloque_distribucion.inverse(),
        inplace=True,
    )

    return circuito


def ejecutar_motor(
    theta_grados: float,
    phi_grados: float,
) -> ResultadoMotor:
    """
    Ejecuta la simulación exacta mediante vectores de estado
    y calcula la fidelidad de recuperación.
    """

    circuito_preparacion = crear_circuito_preparacion(
        theta_grados,
        phi_grados,
    )

    circuito_distribucion = crear_circuito_distribucion(
        theta_grados,
        phi_grados,
    )

    circuito_recuperacion = crear_circuito_recuperacion(
        theta_grados,
        phi_grados,
    )

    # Statevector calcula el estado exacto, sin shots ni muestreo.
    estado_inicial = Statevector.from_instruction(
        circuito_preparacion
    )

    estado_distribuido = Statevector.from_instruction(
        circuito_distribucion
    )

    estado_recuperado = Statevector.from_instruction(
        circuito_recuperacion
    )

   
    fidelidad_calculada = float(
       state_fidelity(
        estado_inicial,
        estado_recuperado,
       )
    )

    fidelidad = max(
    0.0,
    min(1.0, fidelidad_calculada),
    )
    return ResultadoMotor(
        theta_grados=theta_grados,
        phi_grados=phi_grados,
        estado_inicial=estado_inicial,
        estado_distribuido=estado_distribuido,
        estado_recuperado=estado_recuperado,
        fidelidad=fidelidad,
        circuito_preparacion=circuito_preparacion,
        circuito_distribucion=circuito_distribucion,
        circuito_recuperacion=circuito_recuperacion,
    )


def mostrar_amplitudes(
    estado: Statevector,
    decimales: int = 4,
) -> dict[str, complex]:
    """
    Convierte un vector de estado en un diccionario legible.

    Solo incluye amplitudes distintas de cero.
    """

    amplitudes = estado.to_dict(decimals=decimales)

    return {
        base: amplitud
        for base, amplitud in amplitudes.items()
        if abs(amplitud) > 10 ** (-decimales)
    }


if __name__ == "__main__":
    ejemplos = [
        (0, 0),
        (180, 0),
        (90, 0),
        (90, 90),
        (60, 210),
    ]

    for theta, phi in ejemplos:
        resultado = ejecutar_motor(theta, phi)

        print("\n" + "=" * 55)
        print(f"Theta: {theta}° | Phi: {phi}°")

        print("\nEstado inicial:")
        print(mostrar_amplitudes(resultado.estado_inicial))

        print("\nEstado distribuido:")
        print(mostrar_amplitudes(resultado.estado_distribuido))

        print("\nEstado recuperado:")
        print(mostrar_amplitudes(resultado.estado_recuperado))

        print(
            "\nFidelidad:",
            f"{resultado.fidelidad:.12f}",
        )