from itertools import product
from typing import Dict, List, Tuple

Entrada = Tuple[int, int]


def puerta_and(a: int, b: int) -> int:
    """Devuelve el resultado de la operación lógica AND."""
    if a not in (0, 1) or b not in (0, 1):
        raise ValueError("Las entradas deben ser 0 o 1.")

    return a & b


def generar_tabla_and() -> List[Dict[str, int]]:
    """Genera la tabla de verdad completa de la puerta AND."""
    tabla = []

    for a, b in product((0, 1), repeat=2):
        tabla.append(
            {
                "a": a,
                "b": b,
                "salida": puerta_and(a, b),
            }
        )

    return tabla


def agrupar_entradas_por_salida() -> Dict[int, List[Entrada]]:
    """
    Agrupa las entradas según su salida.

    Esto permite ver si varias entradas producen el mismo resultado.
    """
    grupos: Dict[int, List[Entrada]] = {0: [], 1: []}

    for fila in generar_tabla_and():
        entrada = (fila["a"], fila["b"])
        grupos[fila["salida"]].append(entrada)

    return grupos


def detectar_colisiones() -> Dict[int, List[Entrada]]:
    """
    Devuelve únicamente las salidas asociadas a más de una entrada.

    Una colisión muestra que la operación no permite reconstruir
    de manera única la entrada original.
    """
    grupos = agrupar_entradas_por_salida()

    return {
        salida: entradas
        for salida, entradas in grupos.items()
        if len(entradas) > 1
    }


if __name__ == "__main__":
    print("Tabla de verdad de AND:")

    for fila in generar_tabla_and():
        print(f"{fila['a']} AND {fila['b']} = {fila['salida']}")

    print("\nEntradas agrupadas por salida:")
    print(agrupar_entradas_por_salida())

    print("\nColisiones detectadas:")
    print(detectar_colisiones())