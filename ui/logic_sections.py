import pandas as pd
import streamlit as st

from logic.irreversible import (
    agrupar_entradas_por_salida,
    detectar_colisiones,
    generar_tabla_and,
    puerta_and,
)
from logic.reversible import (
    comprobar_recuperacion,
    generar_tabla_cnot,
    puerta_cnot,
    tiene_colisiones,
)


def render_flujo_bits(
    entrada: str,
    operacion: str,
    salida: str,
    color: str,
) -> None:
    """
    Muestra visualmente una transformación lógica.
    """

    st.html(
        f"""
        <section class="logic-flow">
            <style>
                .logic-flow {{
                    display: grid;
                    grid-template-columns:
                        minmax(130px, 1fr)
                        auto
                        minmax(130px, 1fr);
                    align-items: center;
                    gap: 1rem;
                    margin: 1.2rem 0 1.5rem;
                }}

                .logic-state {{
                    padding: 1.2rem;
                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 18px;
                    background:
                        linear-gradient(
                            145deg,
                            rgba(255,255,255,0.065),
                            rgba(255,255,255,0.02)
                        );
                    text-align: center;
                }}

                .logic-label {{
                    display: block;
                    margin-bottom: 0.45rem;
                    color: #8e99b1;
                    font-size: 0.67rem;
                    font-weight: 750;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                }}
                .logic-value {{
                 color: white;
                 font-family: monospace;
                 font-size: 2rem;
                 font-weight: 850;
                 letter-spacing: 0.08em;
                }}

                .logic-operation {{
                    min-width: 110px;
                    padding: 0.8rem 1rem;
                    border: 1px solid {color};
                    border-radius: 999px;
                    color: white;
                    background: color-mix(
                        in srgb,
                        {color} 18%,
                        transparent
                    );
                    box-shadow: 0 0 28px
                        color-mix(
                            in srgb,
                            {color} 22%,
                            transparent
                        );
                    text-align: center;
                    font-weight: 800;
                }}

                .logic-arrow {{
                    margin-top: 0.3rem;
                    color: {color};
                    font-size: 1.45rem;
                }}

                @media (max-width: 650px) {{
                    .logic-flow {{
                        grid-template-columns: 1fr;
                    }}

                    .logic-operation {{
                        justify-self: center;
                    }}
                }}
            </style>

            <div class="logic-state">
                <span class="logic-label">Entrada</span>
                <span class="logic-value">{entrada}</span>
            </div>

            <div class="logic-operation">
                {operacion}
                <div class="logic-arrow">→</div>
            </div>

            <div class="logic-state">
                <span class="logic-label">Salida</span>
                <span class="logic-value">{salida}</span>
            </div>
        </section>
        """
    )


def render_and_section() -> None:
    """
    Laboratorio interactivo de lógica irreversible.
    """

    st.header("Lógica irreversible: puerta AND")

    st.write(
        """
        AND recibe dos bits y produce una sola salida. Como distintas
        entradas pueden generar el mismo resultado, la transformación
        no conserva toda la información necesaria para reconstruir
        la entrada original.
        """
    )

    columna_a, columna_b = st.columns(2)

    with columna_a:
        entrada_a = st.radio(
            "Entrada A",
            options=[0, 1],
            horizontal=True,
            key="and_entrada_a",
        )

    with columna_b:
        entrada_b = st.radio(
            "Entrada B",
            options=[0, 1],
            horizontal=True,
            key="and_entrada_b",
        )

    salida = puerta_and(
        entrada_a,
        entrada_b,
    )

    render_flujo_bits(
        entrada=f"({entrada_a}, {entrada_b})",
        operacion="AND",
        salida=str(salida),
        color="#f97316",
    )

    grupos = agrupar_entradas_por_salida()
    colisiones = detectar_colisiones()
    entradas_compatibles = grupos[salida]

    metrica_1, metrica_2, metrica_3 = st.columns(3)

    with metrica_1:
        st.metric(
            "Salida obtenida",
            salida,
        )

    with metrica_2:
        st.metric(
            "Entradas compatibles",
            len(entradas_compatibles),
        )

    with metrica_3:
        st.metric(
            "¿Es reversible?",
            "No" if salida in colisiones else "Solo en este caso",
        )

    if salida in colisiones:
        st.error(
            f"La salida {salida} también puede provenir de "
            f"{entradas_compatibles}. La entrada original no puede "
            "reconstruirse de forma única."
        )
    else:
        st.success(
            "Para esta salida existe una sola entrada compatible. "
            "Sin embargo, la función AND completa continúa siendo "
            "irreversible porque la salida 0 presenta colisiones."
        )

    st.subheader("Mapa completo de la operación")

    tabla = pd.DataFrame(
        generar_tabla_and()
    )

    tabla.columns = [
        "Entrada A",
        "Entrada B",
        "Salida",
    ]

    tabla["¿Colisión?"] = tabla["Salida"].map(
        lambda valor: (
            "Sí"
            if valor in colisiones
            else "No"
        )
    )

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
    )

    st.html(
        f"""
        <div style="
            padding: 1.2rem;
            border: 1px solid rgba(249,115,22,0.25);
            border-radius: 17px;
            background:
                linear-gradient(
                    135deg,
                    rgba(249,115,22,0.10),
                    rgba(255,255,255,0.025)
                );
        ">
            <strong style="color:#fdba74;">
                Resultado lógico
            </strong>

            <p style="
                margin: 0.55rem 0 0;
                color: #aeb8cf;
                line-height: 1.6;
            ">
                Tres entradas diferentes, 00, 01 y 10, producen la
                misma salida 0. Esa pérdida de distinción convierte
                a AND en una transformación irreversible.
            </p>
        </div>
        """
    )


def render_cnot_section() -> None:
    """
    Laboratorio interactivo de lógica reversible.
    """

    st.header("Lógica reversible: puerta CNOT")

    st.write(
        """
        CNOT conserva el bit de control y modifica el bit objetivo
        mediante XOR. Cada entrada produce una salida diferente y la
        misma operación permite recuperar el estado original.
        """
    )

    columna_control, columna_objetivo = st.columns(2)

    with columna_control:
        control = st.radio(
            "Bit de control",
            options=[0, 1],
            horizontal=True,
            key="cnot_control",
        )

    with columna_objetivo:
        objetivo = st.radio(
            "Bit objetivo",
            options=[0, 1],
            horizontal=True,
            key="cnot_objetivo",
        )

    entrada = (
        control,
        objetivo,
    )

    salida = puerta_cnot(
        control,
        objetivo,
    )

    recuperada = puerta_cnot(
        *salida
    )

    render_flujo_bits(
        entrada=f"({entrada[0]}, {entrada[1]})",
        operacion="CNOT",
        salida=f"({salida[0]}, {salida[1]})",
        color="#a855f7",
    )

    st.subheader("Aplicación inversa")

    render_flujo_bits(
        entrada=f"({salida[0]}, {salida[1]})",
        operacion="CNOT otra vez",
        salida=f"({recuperada[0]}, {recuperada[1]})",
        color="#22d3ee",
    )

    resultados = comprobar_recuperacion()

    metrica_1, metrica_2, metrica_3 = st.columns(3)

    with metrica_1:
        st.metric(
            "¿Presenta colisiones?",
            "Sí" if tiene_colisiones() else "No",
        )

    with metrica_2:
        st.metric(
            "Entrada recuperada",
            (
                "Sí"
                if recuperada == entrada
                else "No"
            ),
        )

    with metrica_3:
        porcentaje = (
            sum(resultados.values())
            / len(resultados)
            * 100
        )

        st.metric(
            "Recuperación total",
            f"{porcentaje:.0f} %",
        )

    if recuperada == entrada:
        st.success(
            "La segunda aplicación de CNOT recuperó exactamente "
            "la entrada original."
        )
    else:
        st.error(
            "La entrada no pudo recuperarse."
        )

    st.subheader("Correspondencia completa")

    tabla = pd.DataFrame(
        generar_tabla_cnot()
    )

    tabla["Entrada recuperada"] = tabla[
        "salida"
    ].map(
        lambda valor: puerta_cnot(
            *valor
        )
    )

    tabla["¿Coincide?"] = tabla.apply(
        lambda fila: (
            "Sí"
            if fila["entrada"]
            == fila["Entrada recuperada"]
            else "No"
        ),
        axis=1,
    )

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
    )

    st.html(
        """
        <div style="
            padding: 1.2rem;
            border: 1px solid rgba(168,85,247,0.28);
            border-radius: 17px;
            background:
                linear-gradient(
                    135deg,
                    rgba(168,85,247,0.11),
                    rgba(34,211,238,0.04)
                );
        ">
            <strong style="color:#d8b4fe;">
                Resultado lógico
            </strong>

            <p style="
                margin: 0.55rem 0 0;
                color: #aeb8cf;
                line-height: 1.6;
            ">
                CNOT establece una correspondencia uno a uno entre
                entradas y salidas. Como la transformación posee una
                inversa, la información original permanece recuperable.
            </p>
        </div>
        """
    )