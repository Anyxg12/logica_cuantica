import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from quantum.noise import (
    ejecutar_con_ruido,
    generar_curva_ruido,
)


NIVELES_CURVA = [
    0.00,
    0.01,
    0.02,
    0.04,
    0.06,
    0.08,
    0.10,
    0.12,
    0.15,
    0.18,
    0.20,
    0.23,
    0.26,
    0.30,
]


@st.cache_data(show_spinner=False)
def calcular_curva_cacheada(
    theta_grados: float,
    phi_grados: float,
) -> pd.DataFrame:
    """
    Calcula y almacena temporalmente la curva de fidelidad.

    El caché evita repetir todas las simulaciones cuando
    Streamlit recarga la página sin cambiar los ángulos.
    """

    resultados = generar_curva_ruido(
        theta_grados=theta_grados,
        phi_grados=phi_grados,
        niveles=NIVELES_CURVA,
    )

    return pd.DataFrame(
        [
            {
                "Nivel de ruido": resultado.nivel_ruido,
                "Ruido (%)": resultado.nivel_ruido * 100,
                "Fidelidad": resultado.fidelidad,
                "Fidelidad (%)": resultado.fidelidad * 100,
            }
            for resultado in resultados
        ]
    )


def crear_grafico_fidelidad(
    dataframe: pd.DataFrame,
    nivel_seleccionado: float,
    fidelidad_seleccionada: float,
) -> go.Figure:
    """
    Construye una curva interactiva de fidelidad frente al ruido.
    """

    figura = px.line(
        dataframe,
        x="Ruido (%)",
        y="Fidelidad (%)",
        markers=True,
        title="Degradación de la recuperación por ruido",
    )

    figura.update_traces(
        line={
            "width": 3,
        },
        marker={
            "size": 8,
        },
        hovertemplate=(
            "<b>Ruido:</b> %{x:.1f} %<br>"
            "<b>Fidelidad:</b> %{y:.4f} %"
            "<extra></extra>"
        ),
    )

    # Marcador del nivel seleccionado por el usuario.
    figura.add_trace(
        go.Scatter(
            x=[nivel_seleccionado * 100],
            y=[fidelidad_seleccionada * 100],
            mode="markers",
            name="Nivel seleccionado",
            marker={
                "size": 15,
                "symbol": "diamond",
            },
            hovertemplate=(
                "<b>Nivel seleccionado</b><br>"
                "Ruido: %{x:.1f} %<br>"
                "Fidelidad: %{y:.4f} %"
                "<extra></extra>"
            ),
        )
    )

    figura.update_layout(
        height=460,
        xaxis_title="Nivel de ruido despolarizante",
        yaxis_title="Fidelidad de recuperación",
        yaxis_range=[0, 102],
        legend_title_text="Resultado",
        margin={
            "l": 20,
            "r": 20,
            "t": 70,
            "b": 20,
        },
    )

    return figura


def crear_indicador_fidelidad(
    fidelidad: float,
) -> go.Figure:
    """
    Crea un indicador visual de la fidelidad obtenida.
    """

    porcentaje = fidelidad * 100

    figura = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=porcentaje,
            number={
                "suffix": " %",
                "valueformat": ".3f",
            },
            title={
                "text": "Información recuperada",
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                },
                "bar": {
                    "thickness": 0.75,
                },
                "steps": [
                    {
                        "range": [0, 60],
                        "color": "rgba(239, 68, 68, 0.18)",
                    },
                    {
                        "range": [60, 85],
                        "color": "rgba(245, 158, 11, 0.18)",
                    },
                    {
                        "range": [85, 100],
                        "color": "rgba(52, 211, 153, 0.18)",
                    },
                ],
                "threshold": {
                    "line": {
                        "width": 4,
                    },
                    "thickness": 0.8,
                    "value": porcentaje,
                },
            },
        )
    )

    figura.update_layout(
        height=300,
        margin={
            "l": 25,
            "r": 25,
            "t": 60,
            "b": 20,
        },
    )

    return figura


def render_panel_ruido(
    theta_grados: float,
    phi_grados: float,
) -> None:
    """
    Muestra la comparación entre simulación ideal
    y simulación afectada por ruido.
    """

    st.subheader("Modelo ideal frente a ruido cuántico")

    st.write(
        """
        Las puertas cuánticas ideales son reversibles, pero un sistema
        físico puede sufrir errores durante su ejecución. Este módulo
        añade ruido despolarizante para observar cómo disminuye la
        capacidad de recuperar el estado original.
        """
    )

    nivel_porcentaje = st.slider(
        "Intensidad del ruido:",
        min_value=0,
        max_value=30,
        value=5,
        step=1,
        format="%d %%",
        key="nivel_ruido",
    )

    nivel_ruido = nivel_porcentaje / 100

    with st.spinner("Ejecutando simulación con ruido..."):
        resultado_ruidoso = ejecutar_con_ruido(
            theta_grados=theta_grados,
            phi_grados=phi_grados,
            nivel_ruido=nivel_ruido,
        )

    fidelidad = resultado_ruidoso.fidelidad
    perdida = 1.0 - fidelidad

    columna_ideal, columna_ruido, columna_perdida = st.columns(3)

    with columna_ideal:
        st.metric(
            "Fidelidad ideal",
            "100.000 %",
        )

    with columna_ruido:
        st.metric(
            "Fidelidad con ruido",
            f"{fidelidad * 100:.3f} %",
        )

    with columna_perdida:
        st.metric(
            "Pérdida respecto al ideal",
            f"{perdida * 100:.3f} %",
        )

    columna_indicador, columna_explicacion = st.columns(
        [1, 1.35]
    )

    with columna_indicador:
        indicador = crear_indicador_fidelidad(
            fidelidad
        )

        st.plotly_chart(
            indicador,
            use_container_width=True,
            key="indicador_fidelidad_ruido",
        )

    with columna_explicacion:
        st.markdown("#### Interpretación")

        if nivel_ruido == 0:
            st.success(
                "Sin ruido, el circuito inverso recupera "
                "completamente el estado inicial."
            )

        elif fidelidad >= 0.90:
            st.success(
                "La recuperación continúa siendo alta, aunque "
                "ya existen pequeñas alteraciones en el estado."
            )

        elif fidelidad >= 0.70:
            st.warning(
                "El ruido produce una degradación visible. "
                "La transformación matemática sigue teniendo inversa, "
                "pero el estado físico ya fue alterado."
            )

        else:
            st.error(
                "El nivel de ruido dificulta significativamente "
                "la recuperación de la información inicial."
            )

        st.info(
            """
            **Ruido no significa irreversibilidad lógica.**

            El circuito ideal todavía posee una inversa. Sin embargo,
            los errores modifican el estado durante la ejecución, por
            lo que aplicar la inversa ya no reconstruye exactamente
            la información original.
            """
        )

    with st.spinner("Calculando curva de degradación..."):
        dataframe_curva = calcular_curva_cacheada(
            theta_grados=theta_grados,
            phi_grados=phi_grados,
        )

    grafico = crear_grafico_fidelidad(
        dataframe=dataframe_curva,
        nivel_seleccionado=nivel_ruido,
        fidelidad_seleccionada=fidelidad,
    )

    st.plotly_chart(
        grafico,
        use_container_width=True,
        key="curva_fidelidad_ruido",
    )

    tabla_visible = dataframe_curva.copy()

    tabla_visible["Ruido"] = tabla_visible[
        "Ruido (%)"
    ].map(
        lambda valor: f"{valor:.0f} %"
    )

    tabla_visible["Fidelidad"] = tabla_visible[
        "Fidelidad (%)"
    ].map(
        lambda valor: f"{valor:.4f} %"
    )

    with st.expander("Ver resultados numéricos"):
        st.dataframe(
            tabla_visible[
                [
                    "Ruido",
                    "Fidelidad",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "El modelo utiliza ruido despolarizante simplificado. "
        "No representa las características exactas de un computador "
        "cuántico físico específico."
    )