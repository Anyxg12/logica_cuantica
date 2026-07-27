from __future__ import annotations

import math

import pandas as pd
import streamlit as st

from quantum.engine import ejecutar_motor
from quantum.metrics import calcular_metricas_sistema


ETAPAS_CUANTICAS = {
    "Estado inicial": "inicial",
    "Información distribuida": "distribuido",
    "Estado recuperado": "recuperado",
}


def obtener_probabilidades(estado) -> pd.DataFrame:
    """
    Convierte un Statevector de tres cúbits en una tabla
    de probabilidades por estado de la base computacional.
    """

    amplitudes = estado.data
    numero_cubits = int(math.log2(len(amplitudes)))

    filas = []

    for indice, amplitud in enumerate(amplitudes):
        probabilidad = float(abs(amplitud) ** 2)

        etiqueta_binaria = format(
            indice,
            f"0{numero_cubits}b",
        )

        filas.append(
            {
                "Estado": f"|{etiqueta_binaria}⟩",
                "Probabilidad": probabilidad,
                "Porcentaje": probabilidad * 100,
            }
        )

    return pd.DataFrame(filas)


def obtener_estado_seleccionado(
    resultado,
    etapa: str,
):
    """
    Devuelve el estado cuántico correspondiente
    a la etapa seleccionada.
    """

    if etapa == "Estado inicial":
        return resultado.estado_inicial

    if etapa == "Información distribuida":
        return resultado.estado_distribuido

    return resultado.estado_recuperado


def obtener_descripcion_etapa(
    etapa: str,
) -> tuple[str, str, str]:
    """
    Devuelve título, descripción y color de una etapa.
    """

    if etapa == "Estado inicial":
        return (
            "Información localizada",
            (
                "El estado preparado mediante θ y φ se encuentra "
                "principalmente en el primer cúbit. Los otros dos "
                "cúbits comienzan en el estado |0⟩."
            ),
            "#22d3ee",
        )

    if etapa == "Información distribuida":
        return (
            "Información no localizada",
            (
                "Las puertas H y CNOT distribuyen amplitudes, fases "
                "y correlaciones entre los tres cúbits. Observar un "
                "solo cúbit ya no revela el estado completo."
            ),
            "#a855f7",
        )

    return (
        "Información reconstruida",
        (
            "El bloque inverso revierte la distribución y recupera "
            "el estado preparado originalmente. La fidelidad mide "
            "qué tan exacta fue esa recuperación."
        ),
        "#4ade80",
    )


def render_circuito_visual(
    theta: float,
    phi: float,
    etapa: str,
) -> None:
    """
    Representa visualmente la arquitectura del circuito
    cuántico utilizado por el motor.
    """

    etapa_clase = ETAPAS_CUANTICAS[etapa]

    st.html(
        f"""
        <section class="quantum-circuit-panel">
            <style>
                .quantum-circuit-panel {{
                    position: relative;
                    overflow: hidden;

                    padding: 1.8rem;
                    margin: 1rem 0 1.5rem;

                    border: 1px solid rgba(255,255,255,0.12);
                    border-radius: 23px;

                    background:
                        radial-gradient(
                            circle at 75% 20%,
                            rgba(168,85,247,0.14),
                            transparent 28%
                        ),
                        linear-gradient(
                            145deg,
                            rgba(16,21,40,0.94),
                            rgba(6,9,22,0.97)
                        );

                    box-shadow:
                        0 22px 65px rgba(0,0,0,0.30);
                }}

                .circuit-header {{
                    display: flex;
                    align-items: flex-start;
                    justify-content: space-between;
                    gap: 1rem;
                    margin-bottom: 1.8rem;
                }}

                .circuit-kicker {{
                    color: #c084fc;
                    font-size: 0.68rem;
                    font-weight: 800;
                    letter-spacing: 0.13em;
                    text-transform: uppercase;
                }}

                .circuit-title {{
                    margin-top: 0.3rem;

                    color: white;
                    font-size: 1.35rem;
                    font-weight: 800;
                }}

                .circuit-parameters {{
                    display: flex;
                    gap: 0.55rem;
                    flex-wrap: wrap;
                    justify-content: flex-end;
                }}

                .parameter-chip {{
                    padding: 0.46rem 0.65rem;

                    border: 1px solid rgba(255,255,255,0.11);
                    border-radius: 999px;

                    color: #cbd5e1;
                    background: rgba(255,255,255,0.04);

                    font-size: 0.72rem;
                    font-weight: 650;
                }}

                .circuit-scroll {{
                    overflow-x: auto;
                    padding-bottom: 0.4rem;
                }}

                .circuit-grid {{
                    position: relative;

                    display: grid;
                    grid-template-columns:
                        62px
                        76px
                        76px
                        92px
                        92px
                        58px
                        92px
                        92px
                        76px
                        76px;

                    grid-template-rows:
                        repeat(3, 72px);

                    align-items: center;

                    min-width: 850px;
                }}

                .wire {{
                    position: absolute;
                    left: 55px;
                    right: 18px;

                    height: 2px;

                    background:
                        linear-gradient(
                            90deg,
                            rgba(148,163,184,0.32),
                            rgba(103,232,249,0.72),
                            rgba(192,132,252,0.68),
                            rgba(74,222,128,0.65)
                        );
                }}

                .wire-0 {{
                    top: 36px;
                }}

                .wire-1 {{
                    top: 108px;
                }}

                .wire-2 {{
                    top: 180px;
                }}

                .qubit-label {{
                    position: relative;
                    z-index: 3;

                    color: #94a3b8;
                    font-family: monospace;
                    font-size: 0.83rem;
                    font-weight: 700;
                }}

                .gate {{
                    position: relative;
                    z-index: 4;

                    display: grid;
                    place-items: center;

                    width: 48px;
                    height: 48px;
                    justify-self: center;

                    border-radius: 13px;

                    color: white;
                    font-size: 0.76rem;
                    font-weight: 820;

                    backdrop-filter: blur(8px);
                }}

                .gate-preparation {{
                    border: 1px solid rgba(34,211,238,0.42);
                    background: rgba(8,145,178,0.18);

                    box-shadow:
                        0 0 24px rgba(34,211,238,0.10);
                }}

                .gate-distribution {{
                    border: 1px solid rgba(168,85,247,0.46);
                    background: rgba(126,34,206,0.20);

                    box-shadow:
                        0 0 24px rgba(168,85,247,0.12);
                }}

                .gate-recovery {{
                    border: 1px solid rgba(74,222,128,0.40);
                    background: rgba(22,163,74,0.16);

                    box-shadow:
                        0 0 24px rgba(74,222,128,0.09);
                }}

                .control-dot {{
                    position: relative;
                    z-index: 5;

                    width: 13px;
                    height: 13px;
                    justify-self: center;

                    border-radius: 50%;
                    background: #d8b4fe;

                    box-shadow:
                        0 0 12px rgba(192,132,252,0.7);
                }}

                .target-gate {{
                    position: relative;
                    z-index: 5;

                    display: grid;
                    place-items: center;

                    width: 31px;
                    height: 31px;
                    justify-self: center;

                    border: 2px solid #d8b4fe;
                    border-radius: 50%;

                    color: #d8b4fe;
                    font-size: 1.3rem;
                    line-height: 1;
                }}

                .connection {{
                    position: absolute;
                    z-index: 2;

                    width: 2px;
                    height: 72px;

                    background:
                        linear-gradient(
                            180deg,
                            #d8b4fe,
                            #a855f7
                        );
                }}

                .connection-cnot-1 {{
                    left: 293px;
                    top: 36px;
                }}

                .connection-cnot-2 {{
                    left: 385px;
                    top: 108px;
                }}

                .connection-inverse-2 {{
                    left: 535px;
                    top: 108px;

                    background:
                        linear-gradient(
                            180deg,
                            #86efac,
                            #22c55e
                        );
                }}

                .connection-inverse-1 {{
                    left: 627px;
                    top: 36px;

                    background:
                        linear-gradient(
                            180deg,
                            #86efac,
                            #22c55e
                        );
                }}

                .circuit-block-label {{
                    position: absolute;
                    top: -4px;

                    padding: 0.3rem 0.55rem;

                    border-radius: 999px;

                    font-size: 0.61rem;
                    font-weight: 750;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                }}

                .label-preparation {{
                    left: 72px;
                    color: #67e8f9;
                    background: rgba(8,145,178,0.13);
                }}

                .label-distribution {{
                    left: 245px;
                    color: #d8b4fe;
                    background: rgba(126,34,206,0.14);
                }}

                .label-recovery {{
                    left: 506px;
                    color: #86efac;
                    background: rgba(22,163,74,0.12);
                }}

                .stage-indicator {{
                    display: flex;
                    align-items: center;
                    gap: 0.6rem;

                    margin-top: 1.2rem;
                    padding: 0.85rem 1rem;

                    border: 1px solid rgba(255,255,255,0.09);
                    border-radius: 14px;

                    background: rgba(255,255,255,0.025);
                }}

                .stage-light {{
                    width: 10px;
                    height: 10px;

                    border-radius: 50%;
                }}

                .stage-light.inicial {{
                    background: #22d3ee;
                    box-shadow: 0 0 15px #22d3ee;
                }}

                .stage-light.distribuido {{
                    background: #a855f7;
                    box-shadow: 0 0 15px #a855f7;
                }}

                .stage-light.recuperado {{
                    background: #4ade80;
                    box-shadow: 0 0 15px #4ade80;
                }}

                .stage-indicator strong {{
                    color: white;
                    font-size: 0.82rem;
                }}

                .stage-indicator span {{
                    color: #8994ac;
                    font-size: 0.73rem;
                }}

                @media (max-width: 700px) {{
                    .quantum-circuit-panel {{
                        padding: 1.25rem;
                    }}

                    .circuit-header {{
                        flex-direction: column;
                    }}

                    .circuit-parameters {{
                        justify-content: flex-start;
                    }}
                }}
            </style>

            <div class="circuit-header">
                <div>
                    <div class="circuit-kicker">
                        Arquitectura unitaria
                    </div>

                    <div class="circuit-title">
                        Preparación, distribución y recuperación
                    </div>
                </div>

                <div class="circuit-parameters">
                    <span class="parameter-chip">
                        θ = {theta:.0f}°
                    </span>

                    <span class="parameter-chip">
                        φ = {phi:.0f}°
                    </span>

                    <span class="parameter-chip">
                        3 cúbits
                    </span>
                </div>
            </div>

            <div class="circuit-scroll">
                <div class="circuit-grid">
                    <div class="wire wire-0"></div>
                    <div class="wire wire-1"></div>
                    <div class="wire wire-2"></div>

                    <span class="circuit-block-label label-preparation">
                        Preparación
                    </span>

                    <span class="circuit-block-label label-distribution">
                        Distribución
                    </span>

                    <span class="circuit-block-label label-recovery">
                        Transformación inversa
                    </span>

                    <div class="connection connection-cnot-1"></div>
                    <div class="connection connection-cnot-2"></div>
                    <div class="connection connection-inverse-2"></div>
                    <div class="connection connection-inverse-1"></div>

                    <div class="qubit-label" style="grid-column:1; grid-row:1;">
                        q₀
                    </div>

                    <div class="qubit-label" style="grid-column:1; grid-row:2;">
                        q₁
                    </div>

                    <div class="qubit-label" style="grid-column:1; grid-row:3;">
                        q₂
                    </div>

                    <div class="gate gate-preparation"
                         style="grid-column:2; grid-row:1;">
                        RY
                    </div>

                    <div class="gate gate-preparation"
                         style="grid-column:3; grid-row:1;">
                        RZ
                    </div>

                    <div class="gate gate-distribution"
                         style="grid-column:4; grid-row:1;">
                        H
                    </div>

                    <div class="control-dot"
                         style="grid-column:5; grid-row:1;">
                    </div>

                    <div class="target-gate"
                         style="grid-column:5; grid-row:2;">
                        +
                    </div>

                    <div class="control-dot"
                         style="grid-column:6; grid-row:2;">
                    </div>

                    <div class="target-gate"
                         style="grid-column:6; grid-row:3;">
                        +
                    </div>

                    <div class="control-dot"
                         style="grid-column:7; grid-row:2;
                                background:#86efac;
                                box-shadow:0 0 12px rgba(74,222,128,0.7);">
                    </div>

                    <div class="target-gate"
                         style="grid-column:7; grid-row:3;
                                border-color:#86efac;
                                color:#86efac;">
                        +
                    </div>

                    <div class="control-dot"
                         style="grid-column:8; grid-row:1;
                                background:#86efac;
                                box-shadow:0 0 12px rgba(74,222,128,0.7);">
                    </div>

                    <div class="target-gate"
                         style="grid-column:8; grid-row:2;
                                border-color:#86efac;
                                color:#86efac;">
                        +
                    </div>

                    <div class="gate gate-recovery"
                         style="grid-column:9; grid-row:1;">
                        H
                    </div>

                    <div class="gate gate-recovery"
                         style="grid-column:10; grid-row:1;">
                        FIN
                    </div>
                </div>
            </div>

            <div class="stage-indicator">
                <span class="stage-light {etapa_clase}"></span>

                <div>
                    <strong>{etapa}</strong>
                    <span>
                        · Estado seleccionado para el análisis
                    </span>
                </div>
            </div>
        </section>
        """
    )


def render_estado_actual(
    etapa: str,
    titulo: str,
    descripcion: str,
    color: str,
) -> None:
    """
    Renderiza una tarjeta explicativa de la etapa actual.
    """

    st.html(
        f"""
        <div style="
            padding: 1.25rem;
            margin-bottom: 1rem;

            border: 1px solid {color}55;
            border-radius: 18px;

            background:
                linear-gradient(
                    135deg,
                    {color}18,
                    rgba(255,255,255,0.025)
                );

            box-shadow:
                0 16px 42px rgba(0,0,0,0.18);
        ">
            <div style="
                color:{color};
                font-size:0.68rem;
                font-weight:800;
                letter-spacing:0.1em;
                text-transform:uppercase;
            ">
                {etapa}
            </div>

            <div style="
                margin-top:0.35rem;
                color:white;
                font-size:1.2rem;
                font-weight:800;
            ">
                {titulo}
            </div>

            <p style="
                margin:0.55rem 0 0;
                color:#aeb8cf;
                line-height:1.65;
            ">
                {descripcion}
            </p>
        </div>
        """
    )


def render_quantum_section() -> None:
    """
    Renderiza el laboratorio visual del circuito cuántico.
    """

    st.header("Circuito cuántico: información distribuida")

    st.write(
        """
        El estado inicial se prepara en el primer cúbit. Después,
        una secuencia de puertas unitarias distribuye su información
        entre tres cúbits. La operación inversa permite comprobar
        si el estado original continúa siendo recuperable.
        """
    )

    columna_theta, columna_phi = st.columns(2)

    with columna_theta:
        theta = st.slider(
            "Ángulo θ de preparación",
            min_value=0,
            max_value=180,
            value=120,
            step=5,
            key="quantum_section_theta",
        )

    with columna_phi:
        phi = st.slider(
            "Fase φ de preparación",
            min_value=0,
            max_value=360,
            value=95,
            step=5,
            key="quantum_section_phi",
        )

    resultado = ejecutar_motor(
        theta_grados=theta,
        phi_grados=phi,
    )

    etapa = st.radio(
        "Etapa del proceso",
        options=list(ETAPAS_CUANTICAS.keys()),
        horizontal=True,
        key="quantum_section_stage",
    )

    estado = obtener_estado_seleccionado(
        resultado,
        etapa,
    )

    titulo, descripcion, color = (
        obtener_descripcion_etapa(etapa)
    )

    render_circuito_visual(
        theta=theta,
        phi=phi,
        etapa=etapa,
    )

    metricas = calcular_metricas_sistema(estado)

    entropia_promedio = sum(
        metrica.entropia
        for metrica in metricas
    ) / len(metricas)

    pureza_promedio = sum(
        metrica.pureza
        for metrica in metricas
    ) / len(metricas)

    probabilidades = obtener_probabilidades(estado)

    estados_activos = int(
        (
            probabilidades["Probabilidad"]
            > 1e-10
        ).sum()
    )

    metrica_1, metrica_2, metrica_3, metrica_4 = (
        st.columns(4)
    )

    with metrica_1:
        st.metric(
            "Fidelidad final",
            f"{resultado.fidelidad * 100:.2f} %",
        )

    with metrica_2:
        st.metric(
            "Entropía local media",
            f"{entropia_promedio:.6f}",
        )

    with metrica_3:
        st.metric(
            "Pureza local media",
            f"{pureza_promedio:.6f}",
        )

    with metrica_4:
        st.metric(
            "Estados con amplitud",
            estados_activos,
        )

    render_estado_actual(
        etapa=etapa,
        titulo=titulo,
        descripcion=descripcion,
        color=color,
    )

    columna_grafico, columna_tabla = st.columns(
        [1.35, 1]
    )

    with columna_grafico:
        st.subheader("Distribución de probabilidades")

        datos_grafico = probabilidades.set_index(
            "Estado"
        )[["Probabilidad"]]

        st.bar_chart(
            datos_grafico,
            use_container_width=True,
            height=380,
        )

    with columna_tabla:
        st.subheader("Estados de la base")

        tabla_visible = probabilidades.copy()

        tabla_visible["Probabilidad"] = (
            tabla_visible["Probabilidad"]
            .map(lambda valor: f"{valor:.8f}")
        )

        tabla_visible["Porcentaje"] = (
            tabla_visible["Porcentaje"]
            .map(lambda valor: f"{valor:.4f} %")
        )

        st.dataframe(
            tabla_visible,
            use_container_width=True,
            hide_index=True,
            height=380,
        )

    if etapa == "Información distribuida":
        st.info(
            """
            Una entropía local elevada no significa que la información
            haya sido destruida. Significa que ya no está contenida
            completamente en un cúbit individual, sino en las
            correlaciones del estado conjunto.
            """
        )

    elif etapa == "Estado recuperado":
        if resultado.fidelidad >= 0.999999:
            st.success(
                """
                La transformación inversa recuperó el estado inicial
                con fidelidad prácticamente perfecta.
                """
            )
        else:
            st.warning(
                """
                La recuperación no fue perfecta. Revisa las operaciones
                aplicadas o el modelo de simulación.
                """
            )

    else:
        st.info(
            """
            Modifica θ y φ para preparar estados distintos. El circuito
            debe conservar también la fase, no solamente las
            probabilidades de medición.
            """
        )

    st.caption(
        """
        La fidelidad compara el estado preparado originalmente con el
        estado obtenido después de aplicar la distribución y su
        transformación inversa.
        """
    )