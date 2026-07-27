from matplotlib.figure import Figure
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector


def crear_esferas_bloch(
    estado: Statevector,
    titulo: str,
) -> Figure:
    """
    Genera una esfera de Bloch para cada cúbit del sistema.

    La esfera representa el estado observable local de cada cúbit.
    En sistemas entrelazados, los vectores pueden aparecer reducidos,
    porque la información está distribuida en correlaciones globales.
    """

    figura = plot_bloch_multivector(
        estado,
        title=titulo,
        figsize=(10, 3.5),
        reverse_bits=False,
    )

    return figura