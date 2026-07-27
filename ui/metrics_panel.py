import pandas as pd
import plotly.express as px
import streamlit as st

from quantum.engine import ResultadoMotor
from quantum.metrics import calcular_metricas_sistema


ORDEN_ETAPAS = [
    "Inicial",
    "Distribuido",
    "Recuperado",
]

ORDEN_QUBITS = [
    "Cúbit 0",
    "Cúbit 1",
    "Cúbit 2",
]


def crear_dataframe_metricas(
    resultado: ResultadoMotor,
) -> pd.DataFrame:
    """
    Reúne la entropía y pureza de cada cúbit
    durante las tres etapas del proceso.
    """

    etapas = {
        "Inicial": resultado.estado_inicial,
        "Distribuido": resultado.estado_distribuido,
        "Recuperado": resultado.estado_recuperado,
    }

    filas = []

    for nombre_etapa, estado in etapas.items():
        metricas_etapa = calcular_metricas_sistema(estado)

        for metrica in metricas_etapa:
            filas.append(
                {
                    "Etapa": nombre_etapa,
                    "Cúbit": f"Cúbit {metrica.qubit}",
                    "Entropía": metrica.entropia,
                    "Pureza": metrica.pureza,
                }
            )

    dataframe = pd.DataFrame(filas)

    dataframe["Etapa"] = pd.Categorical(
        dataframe["Etapa"],
        categories=ORDEN_ETAPAS,
        ordered=True,
    )

    dataframe["Cúbit"] = pd.Categorical(
        dataframe["Cúbit"],
        categories=ORDEN_QUBITS,
        ordered=True,
    )

    return dataframe.sort_values(
        ["Etapa", "Cúbit"]
    ).reset_index(drop=True)


def crear_grafico_barras(
    dataframe: pd.DataFrame,
    variable: str,
    titulo: str,
):
    """
    Construye un gráfico de barras agrupadas.

    Cada etapa aparece como una barra separada,
    evitando que los valores se sumen visualmente.
    """

    figura = px.bar(
        dataframe,
        x="Cúbit",
        y=variable,
        color="Etapa",
        barmode="group",
        text_auto=".3f",
        category_orders={
            "Etapa": ORDEN_ETAPAS,
            "Cúbit": ORDEN_QUBITS,
        },
        title=titulo,
    )

    figura.update_layout(
        height=430,
        yaxis_range=[0, 1.08],
        yaxis_title=variable,
        xaxis_title=None,
        legend_title_text="Etapa",
        margin={
            "l": 20,
            "r": 20,
            "t": 65,
            "b": 20,
        },
    )

    figura.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{x}</b><br>"
            + variable
            + ": %{y:.6f}<extra></extra>"
        ),
    )

    return figura


def crear_grafico_evolucion(
    dataframe: pd.DataFrame,
):
    """
    Muestra la evolución promedio de las métricas
    a través de las tres etapas.
    """

    promedios = (
        dataframe.groupby(
            "Etapa",
            observed=True,
            sort=False,
        )[["Entropía", "Pureza"]]
        .mean()
        .reset_index()
    )

    datos_largos = promedios.melt(
        id_vars="Etapa",
        value_vars=["Entropía", "Pureza"],
        var_name="Métrica",
        value_name="Valor",
    )

    figura = px.line(
        datos_largos,
        x="Etapa",
        y="Valor",
        color="Métrica",
        markers=True,
        category_orders={
            "Etapa": ORDEN_ETAPAS,
        },
        title="Evolución promedio del sistema local",
    )

    figura.update_layout(
        height=420,
        yaxis_range=[0, 1.08],
        xaxis_title=None,
        yaxis_title="Valor promedio",
        legend_title_text="Métrica",
        margin={
            "l": 20,
            "r": 20,
            "t": 65,
            "b": 20,
        },
    )

    figura.update_traces(
        line={
            "width": 3,
        },
        marker={
            "size": 10,
        },
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Valor: %{y:.6f}<extra></extra>"
        ),
    )

    return figura


def render_panel_metricas(
    resultado: ResultadoMotor,
) -> None:
    """
    Muestra cómo cambia el estado local de cada
    cúbit durante la simulación.
    """

    st.subheader("Distribución local de la información")

    st.write(
        """
        Estas métricas permiten observar si cada cúbit conserva
        individualmente un estado definido o si la información
        quedó distribuida en las correlaciones del sistema.
        """
    )

    dataframe = crear_dataframe_metricas(resultado)

    tabla_visible = dataframe.copy()

    tabla_visible["Etapa"] = (
        tabla_visible["Etapa"].astype(str)
    )

    tabla_visible["Cúbit"] = (
        tabla_visible["Cúbit"].astype(str)
    )

    tabla_visible["Entropía"] = (
        tabla_visible["Entropía"].map(
            lambda valor: f"{valor:.6f}"
        )
    )

    tabla_visible["Pureza"] = (
        tabla_visible["Pureza"].map(
            lambda valor: f"{valor:.6f}"
        )
    )

    st.dataframe(
        tabla_visible,
        use_container_width=True,
        hide_index=True,
    )

    columna_entropia, columna_pureza = st.columns(2)

    with columna_entropia:
        figura_entropia = crear_grafico_barras(
            dataframe=dataframe,
            variable="Entropía",
            titulo="Entropía local por cúbit",
        )

        st.plotly_chart(
            figura_entropia,
            use_container_width=True,
            key="grafico_entropia",
        )

        st.caption(
            "Una entropía cercana a 1 indica que el cúbit "
            "observado aisladamente aparece muy mezclado."
        )

    with columna_pureza:
        figura_pureza = crear_grafico_barras(
            dataframe=dataframe,
            variable="Pureza",
            titulo="Pureza local por cúbit",
        )

        st.plotly_chart(
            figura_pureza,
            use_container_width=True,
            key="grafico_pureza",
        )

        st.caption(
            "Una pureza igual a 1 representa un estado "
            "local puro y completamente definido."
        )

    figura_evolucion = crear_grafico_evolucion(
        dataframe
    )

    st.plotly_chart(
        figura_evolucion,
        use_container_width=True,
        key="grafico_evolucion",
    )

    st.caption(
        "La evolución ideal esperada es: estado local puro, "
        "información distribuida y recuperación del estado puro."
    )

    etapa_seleccionada = st.selectbox(
        "Analizar una etapa:",
        options=ORDEN_ETAPAS,
        key="etapa_metricas",
    )

    datos_etapa = dataframe[
        dataframe["Etapa"].astype(str)
        == etapa_seleccionada
    ]

    entropia_promedio = datos_etapa[
        "Entropía"
    ].mean()

    pureza_promedio = datos_etapa[
        "Pureza"
    ].mean()

    metrica_entropia, metrica_pureza = st.columns(2)

    with metrica_entropia:
        st.metric(
            "Entropía local promedio",
            f"{entropia_promedio:.6f}",
        )

    with metrica_pureza:
        st.metric(
            "Pureza local promedio",
            f"{pureza_promedio:.6f}",
        )

    if entropia_promedio < 0.05:
        st.success(
            "Los cúbits presentan estados locales "
            "prácticamente puros."
        )

    elif entropia_promedio > 0.80:
        st.warning(
            "La información está fuertemente distribuida "
            "entre las correlaciones del sistema."
        )

    else:
        st.info(
            "Existe una distribución parcial de información "
            "entre los cúbits."
        )

    st.info(
        """
        El sistema global conserva la información y continúa siendo
        reversible, aunque cada cúbit observado por separado parezca
        mezclado. La información deja de estar localizada, pero no
        necesariamente se destruye.
        """
    )