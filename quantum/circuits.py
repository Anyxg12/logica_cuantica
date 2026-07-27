from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from matplotlib.figure import Figure

def crear_circuito_entrelazado(estado_inicial: int) -> QuantumCircuit:
    """
    Crea un circuito de 3 cúbits.

    El primer cúbit contiene la información inicial.
    Los otros dos ayudan a distribuir esa información
    mediante entrelazamiento.
    """
    if estado_inicial not in (0, 1):
        raise ValueError("El estado inicial debe ser 0 o 1.")

    circuito = QuantumCircuit(3, 3)

    # Si queremos iniciar en |1>, aplicamos X al primer cúbit.
    if estado_inicial == 1:
        circuito.x(0)

    # Creamos superposición en el primer cúbit.
    circuito.h(0)

    # Distribuimos la información entre los tres cúbits.
    circuito.cx(0, 1)
    circuito.cx(1, 2)

    return circuito


def crear_circuito_medicion(estado_inicial: int) -> QuantumCircuit:
    """
    Crea el circuito y mide los tres cúbits.
    """
    circuito = crear_circuito_entrelazado(estado_inicial)
    circuito.measure([0, 1, 2], [0, 1, 2])

    return circuito


def simular_circuito(circuito: QuantumCircuit, shots: int = 1000) -> dict:
    """
    Ejecuta el circuito con AerSimulator.
    """
    simulador = AerSimulator()
    resultado = simulador.run(circuito, shots=shots).result()

    return resultado.get_counts()

def dibujar_circuito(circuito: QuantumCircuit) -> Figure:
    """
    Genera una representación gráfica del circuito cuántico.
    """
    figura = circuito.draw(
        output="mpl",
        fold=-1,
        idle_wires=False,
    )

    return figura
def crear_circuito_recuperacion(estado_inicial: int) -> QuantumCircuit:
    """
    Distribuye la información y después revierte la transformación.

    Si todo funciona correctamente:
    - |0> debe recuperarse como 000.
    - |1> debe recuperarse como 001.

    Qiskit muestra los bits en orden c2 c1 c0.
    """
    circuito = crear_circuito_entrelazado(estado_inicial)

    circuito.barrier()

    # Invertimos las operaciones en orden contrario.
    circuito.cx(1, 2)
    circuito.cx(0, 1)
    circuito.h(0)

    circuito.barrier()
    circuito.measure([0, 1, 2], [0, 1, 2])

    return circuito


def comprobar_recuperacion(estado_inicial: int, shots: int = 1000) -> dict:
    """Ejecuta el circuito de recuperación y devuelve sus mediciones."""
    circuito = crear_circuito_recuperacion(estado_inicial)
    return simular_circuito(circuito, shots)


if __name__ == "__main__":
    for estado in (0, 1):
        print(f"\n{'=' * 45}")
        print(f"Estado inicial: |{estado}>")

        print("\nMedición después de distribuir la información:")
        circuito_medicion = crear_circuito_medicion(estado)
        print(circuito_medicion)
        print(simular_circuito(circuito_medicion))

        print("\nMedición después de aplicar el circuito inverso:")
        circuito_recuperacion = crear_circuito_recuperacion(estado)
        print(circuito_recuperacion)
        print(simular_circuito(circuito_recuperacion))
