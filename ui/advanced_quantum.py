from typing import Dict

import pandas as pd
import streamlit as st

from quantum.engine import ejecutar_motor, mostrar_amplitudes
from quantum.visualizations import crear_esferas_bloch
from ui.black_hole_visual import render_modelo_agujero_negro
from ui.export_panel import render_panel_exportacion
from ui.metrics_panel import render_panel_metricas
from ui.noise_panel import render_panel_ruido


SECCIONES_MOTOR = [
    "Resumen",
    "Evolución",
    "Métricas",
    "Ruido",
    "Analogía visual",
    "Datos técnicos",
]


def formatear_complejo(valor: complex) -> str:
    """
    Convierte una amplitud compleja en un texto legible.
    """
    real = float(valor.real)
    imaginaria = float(valor.imag)

    if abs(real) < 1e-10:
        real = 0.0

    if abs(imaginaria) < 1e-10:
        imaginaria = 0.0

    return f"{real:.4f} {imaginaria:+.4f}i"


def amplitudes_a_dataframe(
    amplitudes: Dict[str, complex],
) -> pd.DataFrame:
    """
    Convierte las amplitudes de un estado cuántico
    en una tabla legible.
    """
    filas = []

    for estado_base, amplitud in amplitudes.items():
        amplitud_compleja = complex(amplitud)
        probabilidad = abs(amplitud_compleja) ** 2

        filas.append(
            {
                "Estado base": str(estado_base),
                "Amplitud": formatear_complejo(
                    amplitud_compleja
                ),
                "Probabilidad": (
                    f"{probabilidad * 100:.2f} %"
                ),
            }
        )

    return pd.DataFrame(filas)


def mostrar_figura_bloch(
    estado,
    titulo: str,
    explicacion: str,
) -> None:
    """
    Genera y muestra las esferas de Bloch del sistema.
    """
    figura = crear_esferas_bloch(
        estado=estado,
        titulo=titulo,
    )

    st.pyplot(
    figura,
    use_container_width=True,
    clear_figure=True,
    )

    st.caption(explicacion)


def render_cabecera_motor(
    theta: int,
    phi: int,
    fidelidad_porcentaje: float,
    estados_equivalentes: bool,
) -> None:
    """
    Renderiza la cabecera visual del motor avanzado.
    """

    if estados_equivalentes:
        estado_texto = "Recuperación verificada"
        estado_color = "#4ade80"
        estado_fondo = "rgba(74, 222, 128, 0.10)"
    else:
        estado_texto = "Revisión necesaria"
        estado_color = "#fb7185"
        estado_fondo = "rgba(251, 113, 133, 0.10)"

    st.html(
        f"""
        <section class="advanced-engine-hero">
            <style>
                .advanced-engine-hero {{
                    position: relative;
                    overflow: hidden;

                    display: grid;
                    grid-template-columns:
                        minmax(0, 1.35fr)
                        minmax(310px, 0.75fr);

                    gap: 1.5rem;
                    align-items: center;

                    min-height: 330px;
                    padding: 2.2rem;
                    margin-bottom: 1.3rem;

                    border:
                        1px solid rgba(255, 255, 255, 0.12);

                    border-radius: 26px;

                    background:
                        radial-gradient(
                            circle at 82% 23%,
                            rgba(168, 85, 247, 0.22),
                            transparent 30%
                        ),
                        radial-gradient(
                            circle at 18% 80%,
                            rgba(34, 211, 238, 0.10),
                            transparent 32%
                        ),
                        linear-gradient(
                            145deg,
                            rgba(17, 21, 42, 0.96),
                            rgba(5, 8, 21, 0.98)
                        );

                    box-shadow:
                        0 28px 80px rgba(0, 0, 0, 0.34);
                }}

                .advanced-engine-hero::before {{
                    content: "";
                    position: absolute;
                    inset: 0;
                    pointer-events: none;

                    background-image:
                        radial-gradient(
                            circle,
                            rgba(255, 255, 255, 0.36)
                            0 0.7px,
                            transparent 0.9px
                        );

                    background-size: 59px 59px;
                    opacity: 0.17;
                }}

                .engine-content,
                .engine-dashboard {{
                    position: relative;
                    z-index: 2;
                }}

                .engine-kicker {{
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;

                    margin-bottom: 0.85rem;
                    padding: 0.4rem 0.7rem;

                    border:
                        1px solid rgba(192, 132, 252, 0.30);

                    border-radius: 999px;

                    color: #d8b4fe;
                    background: rgba(168, 85, 247, 0.09);

                    font-size: 0.68rem;
                    font-weight: 800;
                    letter-spacing: 0.11em;
                    text-transform: uppercase;
                }}

                .engine-light {{
                    width: 7px;
                    height: 7px;
                    border-radius: 50%;

                    background: {estado_color};

                    box-shadow:
                        0 0 8px {estado_color},
                        0 0 17px {estado_color};

                    animation:
                        engine-pulse 2.2s ease-in-out infinite;
                }}

                .engine-title {{
                    max-width: 690px;
                    margin: 0;

                    color: white;
                    font-size: clamp(2rem, 4vw, 3.6rem);
                    font-weight: 870;
                    line-height: 1.02;
                    letter-spacing: -0.05em;
                }}

                .engine-title span {{
                    background:
                        linear-gradient(
                            90deg,
                            #c084fc,
                            #67e8f9
                        );

                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                }}

                .engine-description {{
                    max-width: 690px;
                    margin: 1rem 0 1.35rem;

                    color: #adb7ce;
                    font-size: 0.96rem;
                    line-height: 1.7;
                }}

                .engine-process {{
                    display: flex;
                    flex-wrap: wrap;
                    align-items: center;
                    gap: 0.45rem;
                }}

                .process-chip {{
                    padding: 0.52rem 0.72rem;

                    border:
                        1px solid rgba(255, 255, 255, 0.10);

                    border-radius: 11px;

                    color: #dbe4f5;
                    background: rgba(255, 255, 255, 0.035);

                    font-size: 0.72rem;
                    font-weight: 680;
                }}

                .process-arrow {{
                    color: #7d88a0;
                    font-size: 0.85rem;
                }}

                .engine-dashboard {{
                    display: grid;
                    gap: 0.75rem;
                }}

                .engine-status {{
                    padding: 0.85rem 1rem;

                    border: 1px solid {estado_color}55;
                    border-radius: 14px;

                    color: {estado_color};
                    background: {estado_fondo};

                    font-size: 0.78rem;
                    font-weight: 750;
                    text-align: center;
                }}

                .engine-value-card {{
                    position: relative;
                    overflow: hidden;

                    padding: 1rem;

                    border:
                        1px solid rgba(255, 255, 255, 0.11);

                    border-radius: 16px;

                    background:
                        linear-gradient(
                            145deg,
                            rgba(255, 255, 255, 0.065),
                            rgba(255, 255, 255, 0.018)
                        );

                    backdrop-filter: blur(12px);
                }}

                .engine-value-card::before {{
                    content: "";
                    position: absolute;
                    top: 0;
                    left: 0;

                    width: 100%;
                    height: 2px;

                    background:
                        linear-gradient(
                            90deg,
                            #a855f7,
                            #22d3ee
                        );
                }}

                .engine-value-label {{
                    display: block;
                    margin-bottom: 0.3rem;

                    color: #818ca4;
                    font-size: 0.63rem;
                    font-weight: 750;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                }}

                .engine-value {{
                    color: white;
                    font-size: 1.15rem;
                    font-weight: 820;
                }}

                .engine-value-highlight {{
                    color: #67e8f9;
                }}

                @keyframes engine-pulse {{
                    0%, 100% {{
                        opacity: 0.55;
                        transform: scale(0.85);
                    }}

                    50% {{
                        opacity: 1;
                        transform: scale(1.12);
                    }}
                }}

                @media (max-width: 850px) {{
                    .advanced-engine-hero {{
                        grid-template-columns: 1fr;
                        min-height: auto;
                        padding: 1.6rem;
                    }}

                    .engine-dashboard {{
                        grid-template-columns:
                            repeat(3, minmax(0, 1fr));
                    }}

                    .engine-status {{
                        grid-column: 1 / -1;
                    }}
                }}

                @media (max-width: 560px) {{
                    .engine-dashboard {{
                        grid-template-columns: 1fr;
                    }}

                    .engine-status {{
                        grid-column: auto;
                    }}
                }}
            </style>

            <div class="engine-content">
                <div class="engine-kicker">
                    <span class="engine-light"></span>
                    Laboratorio cuántico interactivo
                </div>

                <h2 class="engine-title">
                    Motor cuántico
                    <span>avanzado</span>
                </h2>

                <p class="engine-description">
                    Prepara un estado mediante los ángulos θ y φ,
                    distribuye su información entre tres cúbits y
                    comprueba si una transformación inversa puede
                    reconstruirlo con precisión.
                </p>

                <div class="engine-process">
                    <span class="process-chip">
                        Preparación
                    </span>

                    <span class="process-arrow">→</span>

                    <span class="process-chip">
                        Distribución
                    </span>

                    <span class="process-arrow">→</span>

                    <span class="process-chip">
                        Recuperación
                    </span>

                    <span class="process-arrow">→</span>

                    <span class="process-chip">
                        Verificación
                    </span>
                </div>
            </div>

            <div class="engine-dashboard">
                <div class="engine-status">
                    {estado_texto}
                </div>

                <div class="engine-value-card">
                    <span class="engine-value-label">
                        Ángulo polar
                    </span>

                    <span class="engine-value">
                        θ = {theta}°
                    </span>
                </div>

                <div class="engine-value-card">
                    <span class="engine-value-label">
                        Fase relativa
                    </span>

                    <span class="engine-value">
                        φ = {phi}°
                    </span>
                </div>

                <div class="engine-value-card">
                    <span class="engine-value-label">
                        Fidelidad final
                    </span>

                    <span class="
                        engine-value
                        engine-value-highlight
                    ">
                        {fidelidad_porcentaje:.2f} %
                    </span>
                </div>
            </div>
        </section>
        """
    )


def render_resumen_motor(
    resultado,
    theta: int,
    phi: int,
    estados_equivalentes: bool,
) -> None:
    """
    Muestra el resumen principal del experimento.
    """

    st.subheader("Resumen del experimento")

    columna_1, columna_2, columna_3, columna_4 = (
        st.columns(4)
    )

    with columna_1:
        st.metric(
            "Cúbits simulados",
            "3",
        )

    with columna_2:
        st.metric(
            "Ángulo θ",
            f"{theta}°",
        )

    with columna_3:
        st.metric(
            "Fase φ",
            f"{phi}°",
        )

    with columna_4:
        st.metric(
            "Fidelidad",
            f"{resultado.fidelidad * 100:.2f} %",
        )

    st.html(
        """
        <section class="advanced-summary">
            <style>
                .advanced-summary {
                    display: grid;
                    grid-template-columns:
                        repeat(3, minmax(0, 1fr));

                    gap: 0.85rem;
                    margin: 1.2rem 0;
                }

                .advanced-summary-card {
                    position: relative;
                    overflow: hidden;

                    padding: 1.25rem;

                    border:
                        1px solid rgba(255, 255, 255, 0.10);

                    border-radius: 18px;

                    background:
                        linear-gradient(
                            145deg,
                            rgba(255, 255, 255, 0.055),
                            rgba(255, 255, 255, 0.018)
                        );
                }

                .advanced-summary-number {
                    display: grid;
                    place-items: center;

                    width: 34px;
                    height: 34px;
                    margin-bottom: 0.8rem;

                    border-radius: 11px;

                    color: #d8b4fe;
                    background: rgba(168, 85, 247, 0.13);

                    font-weight: 820;
                }

                .advanced-summary-card h4 {
                    margin: 0 0 0.45rem;
                    color: white;
                    font-size: 1rem;
                }

                .advanced-summary-card p {
                    margin: 0;
                    color: #98a4bc;
                    font-size: 0.8rem;
                    line-height: 1.55;
                }

                @media (max-width: 750px) {
                    .advanced-summary {
                        grid-template-columns: 1fr;
                    }
                }
            </style>

            <article class="advanced-summary-card">
                <div class="advanced-summary-number">
                    1
                </div>

                <h4>Preparación</h4>

                <p>
                    Las puertas RY y RZ construyen el estado inicial
                    a partir de los ángulos seleccionados.
                </p>
            </article>

            <article class="advanced-summary-card">
                <div class="advanced-summary-number">
                    2
                </div>

                <h4>Distribución</h4>

                <p>
                    Las puertas H y CNOT desplazan la información
                    hacia correlaciones globales entre los cúbits.
                </p>
            </article>

            <article class="advanced-summary-card">
                <div class="advanced-summary-number">
                    3
                </div>

                <h4>Recuperación</h4>

                <p>
                    El circuito inverso reconstruye el estado y la
                    fidelidad comprueba matemáticamente el resultado.
                </p>
            </article>
        </section>
        """
    )

    if estados_equivalentes:
        st.success(
            """
            El estado recuperado es equivalente al estado inicial,
            incluyendo amplitudes y fase relativa.
            """
        )
    else:
        st.error(
            """
            El estado recuperado no coincide con el estado inicial.
            Revisa las operaciones aplicadas por el circuito.
            """
        )

    st.info(
        """
        La fidelidad se calcula internamente con toda la precisión
        disponible. El porcentaje mostrado se redondea a dos decimales
        únicamente para mejorar la presentación visual.
        """
    )


def render_evolucion_cuantica(resultado) -> None:
    """
    Muestra la evolución del sistema mediante esferas de Bloch.
    """

    st.subheader("Evolución del estado cuántico")

    etapa_visual = st.radio(
        "Selecciona la etapa que deseas observar:",
        options=[
            "Estado inicial",
            "Información distribuida",
            "Estado recuperado",
        ],
        horizontal=True,
        key="etapa_bloch",
    )

    if etapa_visual == "Estado inicial":
        estado_visual = resultado.estado_inicial
        titulo_visual = "Estado inicial"

        explicacion_visual = (
            "El primer cúbit contiene el estado preparado mediante "
            "los ángulos θ y φ. Los otros dos cúbits permanecen "
            "inicialmente en |0⟩."
        )

        color = "#22d3ee"
        titulo_estado = "Información localizada"

    elif etapa_visual == "Información distribuida":
        estado_visual = resultado.estado_distribuido
        titulo_visual = "Información distribuida"

        explicacion_visual = (
            "Después de aplicar las puertas cuánticas, la información "
            "ya no se encuentra únicamente en el primer cúbit. "
            "También está distribuida en las correlaciones globales "
            "entre los tres cúbits."
        )

        color = "#a855f7"
        titulo_estado = "Información entrelazada"

    else:
        estado_visual = resultado.estado_recuperado
        titulo_visual = "Estado recuperado"

        explicacion_visual = (
            "Después de aplicar la transformación inversa, "
            "el primer cúbit recupera el estado preparado originalmente."
        )

        color = "#4ade80"
        titulo_estado = "Información reconstruida"

    st.html(
        f"""
        <div style="
            padding: 1rem 1.15rem;
            margin: 1rem 0;

            border: 1px solid {color}55;
            border-radius: 16px;

            background:
                linear-gradient(
                    135deg,
                    {color}17,
                    rgba(255,255,255,0.02)
                );
        ">
            <div style="
                color:{color};
                font-size:0.68rem;
                font-weight:800;
                letter-spacing:0.1em;
                text-transform:uppercase;
            ">
                Etapa seleccionada
            </div>

            <div style="
                margin-top:0.35rem;
                color:white;
                font-size:1.12rem;
                font-weight:800;
            ">
                {titulo_estado}
            </div>
        </div>
        """
    )

    mostrar_figura_bloch(
        estado=estado_visual,
        titulo=titulo_visual,
        explicacion=explicacion_visual,
    )

    st.info(
        """
        Cada esfera representa el estado observable local de un cúbit.

        Cuando los cúbits están entrelazados, una flecha puede reducirse
        o acercarse al centro. Esto no implica que la información haya
        desaparecido: puede permanecer codificada en las correlaciones
        del sistema completo.
        """
    )


def render_datos_tecnicos(
    resultado,
    theta: int,
    phi: int,
) -> None:
    """
    Renderiza amplitudes, probabilidades y exportación.
    """

    st.subheader("Datos técnicos del experimento")

    st.write(
        """
        Esta sección contiene los valores numéricos utilizados por el
        motor. Se mantiene separada del recorrido visual para evitar
        que las tablas ocupen media galaxia cada vez que se abre la
        pestaña.
        """
    )

    amplitudes_iniciales = mostrar_amplitudes(
        resultado.estado_inicial
    )

    amplitudes_distribuidas = mostrar_amplitudes(
        resultado.estado_distribuido
    )

    amplitudes_recuperadas = mostrar_amplitudes(
        resultado.estado_recuperado
    )

    with st.expander(
        "Amplitudes y probabilidades",
        expanded=True,
    ):
        (
            tab_estado_inicial,
            tab_estado_distribuido,
            tab_estado_recuperado,
        ) = st.tabs(
            [
                "Estado inicial",
                "Información distribuida",
                "Estado recuperado",
            ]
        )

        with tab_estado_inicial:
            st.dataframe(
                amplitudes_a_dataframe(
                    amplitudes_iniciales
                ),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Estado preparado mediante las puertas RY y RZ."
            )

        with tab_estado_distribuido:
            st.dataframe(
                amplitudes_a_dataframe(
                    amplitudes_distribuidas
                ),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Las amplitudes corresponden al sistema global "
                "formado por tres cúbits."
            )

        with tab_estado_recuperado:
            st.dataframe(
                amplitudes_a_dataframe(
                    amplitudes_recuperadas
                ),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Después de aplicar la transformación inversa, "
                "reaparece el estado inicial."
            )

    st.info(
        """
        La fidelidad compara matemáticamente el estado inicial con el
        recuperado. Un valor de 100 % representa una recuperación ideal.
        """
    )

    with st.expander(
        "Exportación y respaldo de resultados",
        expanded=False,
    ):
        render_panel_exportacion(
            resultado=resultado,
            theta=theta,
            phi=phi,
        )


def render_motor_avanzado() -> None:
    """
    Renderiza el motor cuántico avanzado organizado
    como un panel de análisis interactivo.
    """

    columna_theta, columna_phi = st.columns(2)

    with columna_theta:
        theta = st.slider(
            "Ángulo θ: proporción entre |0⟩ y |1⟩",
            min_value=0,
            max_value=180,
            value=90,
            step=5,
            key="theta_motor",
        )

    with columna_phi:
        phi = st.slider(
            "Ángulo φ: fase relativa",
            min_value=0,
            max_value=360,
            value=0,
            step=5,
            key="phi_motor",
        )

    resultado = ejecutar_motor(
        theta_grados=theta,
        phi_grados=phi,
    )

    fidelidad_porcentaje = (
        resultado.fidelidad * 100
    )

    estados_equivalentes = (
        resultado.estado_inicial.equiv(
            resultado.estado_recuperado
        )
    )

    render_cabecera_motor(
        theta=theta,
        phi=phi,
        fidelidad_porcentaje=fidelidad_porcentaje,
        estados_equivalentes=estados_equivalentes,
    )

    st.markdown("### Panel de análisis")

    seccion = st.radio(
        "Selecciona una sección:",
        options=SECCIONES_MOTOR,
        horizontal=True,
        key="seccion_motor_avanzado",
        label_visibility="collapsed",
    )

    st.divider()

    if seccion == "Resumen":
        render_resumen_motor(
            resultado=resultado,
            theta=theta,
            phi=phi,
            estados_equivalentes=estados_equivalentes,
        )

    elif seccion == "Evolución":
        render_evolucion_cuantica(
            resultado
        )

    elif seccion == "Métricas":
        render_panel_metricas(
            resultado
        )

    elif seccion == "Ruido":
        render_panel_ruido(
            theta_grados=theta,
            phi_grados=phi,
        )

    elif seccion == "Analogía visual":
        render_modelo_agujero_negro(
            resultado
        )

    else:
        render_datos_tecnicos(
            resultado=resultado,
            theta=theta,
            phi=phi,
        )