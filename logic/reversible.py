from itertools import product
from typing import Dict, List, Tuple

Entrada = Tuple[int, int]


def puerta_cnot(control: int, objetivo: int) -> Entrada:
    """
    Aplica una puerta CNOT clásica.

    El primer bit se conserva.
    El segundo cambia si el primer bit es 1.
    """
    if control not in (0, 1) or objetivo not in (0, 1):
        raise ValueError("Las entradas deben ser 0 o 1.")

    nuevo_objetivo = control ^ objetivo
    return control, nuevo_objetivo


def generar_tabla_cnot() -> List[Dict[str, object]]:
    """Genera todas las combinaciones posibles de entrada y salida."""
    tabla = []

    for control, objetivo in product((0, 1), repeat=2):
        salida = puerta_cnot(control, objetivo)

        tabla.append(
            {
                "entrada": (control, objetivo),
                "salida": salida,
            }
        )

    return tabla


def tiene_colisiones() -> bool:
    """
    Comprueba si dos entradas diferentes producen la misma salida.
    """
    salidas = [fila["salida"] for fila in generar_tabla_cnot()]
    return len(salidas) != len(set(salidas))


def comprobar_recuperacion() -> Dict[Entrada, bool]:
    """
    Aplica CNOT dos veces.

    Como CNOT es su propia inversa, debe recuperar la entrada original.
    """
    resultados = {}

    for control, objetivo in product((0, 1), repeat=2):
        entrada = (control, objetivo)
        transformada = puerta_cnot(*entrada)
        recuperada = puerta_cnot(*transformada)

        resultados[entrada] = recuperada == entrada

    return resultados


if __name__ == "__main__":
    print("Tabla de CNOT:")

    for fila in generar_tabla_cnot():
        print(f"{fila['entrada']} -> {fila['salida']}")

    print("\n¿Tiene colisiones?")
    print(tiene_colisiones())

    print("\n¿Se recupera cada entrada aplicando CNOT dos veces?")
    for entrada, recuperada in comprobar_recuperacion().items():
        print(f"{entrada}: {recuperada}")