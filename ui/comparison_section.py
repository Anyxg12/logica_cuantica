from __future__ import annotations

import pandas as pd
import streamlit as st

from logic.irreversible import (
    agrupar_entradas_por_salida,
    detectar_colisiones,
)
from logic.reversible import comprobar_recuperacion
from quantum.engine import ejecutar_motor


def calcular_resultados_comparacion() -> dict:
    """
    Calcula los indicadores reales utilizados
    en la comparación final.
    """

    grupos_and = agrupar_entradas_por_salida()
    colisiones_and = detectar_colisiones()

    total_entradas_and = sum(
        len(entradas)
        for entradas in grupos_and.values()
    )

    entradas_unicas_and = sum(
        len(entradas)
        for entradas in grupos_and.values()
        if len(entradas) == 1
    )

    porcentaje_unicidad_and = (
        entradas_unicas_and
        / total_entradas_and
        * 100
    )

    recuperacion_cnot = comprobar_recuperacion()

    porcentaje_recuperacion_cnot = (
        sum(recuperacion_cnot.values())
        / len(recuperacion_cnot)
        * 100
    )

    resultado_cuantico = ejecutar_motor(
        theta_grados=120,
        phi_grados=95,
    )

    return {
        "colisiones_and": len(colisiones_and),
        "entradas_colisionadas_and": sum(
            len(entradas)
            for entradas in colisiones_and.values()
        ),
        "unicidad_and": porcentaje_unicidad_and,
        "recuperacion_cnot": porcentaje_recuperacion_cnot,
        "fidelidad_cuantica": (
            resultado_cuantico.fidelidad * 100
        ),
    }


def render_comparison_section() -> None:
    """
    Renderiza la conclusión visual que compara
    los tres modelos computacionales.
    """

    resultados = calcular_resultados_comparacion()

    st.header("Comparación final")

    st.write(
        """
        Los tres modelos transforman información, pero no lo hacen
        de la misma manera. La diferencia esencial está en si la
        entrada original continúa siendo distinguible y recuperable
        después de ejecutar la operación.
        """
    )

    st.html(
        f"""
        <section class="comparison-dashboard">
            <style>
                .comparison-dashboard {{
                    position: relative;
                    overflow: hidden;

                    padding: 2.2rem;
                    margin: 1rem 0 1.5rem;

                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: 27px;

                    background:
                        radial-gradient(
                            circle at 14% 20%,
                            rgba(249, 115, 22, 0.12),
                            transparent 24%
                        ),
                        radial-gradient(
                            circle at 50% 15%,
                            rgba(168, 85, 247, 0.13),
                            transparent 25%
                        ),
                        radial-gradient(
                            circle at 87% 20%,
                            rgba(34, 211, 238, 0.11),
                            transparent 24%
                        ),
                        linear-gradient(
                            145deg,
                            rgba(14, 18, 35, 0.95),
                            rgba(6, 9, 21, 0.98)
                        );

                    box-shadow:
                        0 28px 80px rgba(0, 0, 0, 0.34);
                }}

                .comparison-heading {{
                    max-width: 800px;
                    margin-bottom: 2rem;
                }}

                .comparison-kicker {{
                    color: #c084fc;
                    font-size: 0.7rem;
                    font-weight: 800;
                    letter-spacing: 0.14em;
                    text-transform: uppercase;
                }}

                .comparison-title {{
                    margin: 0.4rem 0 0.65rem;

                    color: white;
                    font-size: clamp(1.9rem, 4vw, 3.15rem);
                    font-weight: 850;
                    line-height: 1.05;
                    letter-spacing: -0.045em;
                }}

                .comparison-description {{
                    color: #aeb8cf;
                    font-size: 0.98rem;
                    line-height: 1.7;
                }}

                .comparison-cards {{
                    position: relative;

                    display: grid;
                    grid-template-columns:
                        repeat(3, minmax(0, 1fr));

                    gap: 1rem;
                }}

                .comparison-cards::before {{
                    content: "";

                    position: absolute;
                    top: 44px;
                    left: 16%;
                    right: 16%;

                    height: 2px;

                    background:
                        linear-gradient(
                            90deg,
                            #f97316,
                            #a855f7,
                            #22d3ee
                        );

                    opacity: 0.35;
                }}

                .comparison-card {{
                    position: relative;
                    z-index: 2;
                    overflow: hidden;

                    min-height: 390px;
                    padding: 1.35rem;

                    border: 1px solid rgba(255, 255, 255, 0.11);
                    border-radius: 21px;

                    background:
                        linear-gradient(
                            150deg,
                            rgba(255, 255, 255, 0.065),
                            rgba(255, 255, 255, 0.018)
                        );

                    backdrop-filter: blur(13px);

                    transition:
                        transform 0.25s ease,
                        border-color 0.25s ease,
                        box-shadow 0.25s ease;
                }}

                .comparison-card:hover {{
                    transform: translateY(-6px);

                    border-color:
                        rgba(192, 132, 252, 0.37);

                    box-shadow:
                        0 24px 58px rgba(0, 0, 0, 0.29),
                        0 0 38px rgba(168, 85, 247, 0.07);
                }}

                .model-symbol {{
                    display: grid;
                    place-items: center;

                    width: 58px;
                    height: 58px;
                    margin-bottom: 1rem;

                    border-radius: 18px;

                    font-size: 1.25rem;
                    font-weight: 850;
                }}

                .symbol-and {{
                    color: #fdba74;
                    background: rgba(249, 115, 22, 0.13);
                    border: 1px solid rgba(249, 115, 22, 0.28);
                }}

                .symbol-cnot {{
                    color: #d8b4fe;
                    background: rgba(168, 85, 247, 0.13);
                    border: 1px solid rgba(168, 85, 247, 0.28);
                }}

                .symbol-quantum {{
                    color: #67e8f9;
                    background: rgba(34, 211, 238, 0.12);
                    border: 1px solid rgba(34, 211, 238, 0.28);
                }}

                .model-type {{
                    margin-bottom: 0.3rem;

                    color: #8792aa;
                    font-size: 0.65rem;
                    font-weight: 760;
                    letter-spacing: 0.09em;
                    text-transform: uppercase;
                }}

                .model-name {{
                    margin: 0 0 0.65rem;

                    color: white;
                    font-size: 1.3rem;
                    font-weight: 820;
                }}

                .model-description {{
                    min-height: 94px;
                    margin: 0;

                    color: #aeb8cf;
                    font-size: 0.86rem;
                    line-height: 1.6;
                }}

                .result-box {{
                    margin-top: 1.15rem;
                    padding: 0.9rem;

                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 14px;

                    background: rgba(5, 8, 19, 0.64);
                }}

                .result-label {{
                    display: block;
                    margin-bottom: 0.3rem;

                    color: #78849c;
                    font-size: 0.62rem;
                    font-weight: 750;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                }}

                .result-value {{
                    display: block;

                    color: white;
                    font-size: 1.05rem;
                    font-weight: 800;
                }}

                .result-orange {{
                    color: #fb923c;
                }}

                .result-purple {{
                    color: #c084fc;
                }}

                .result-cyan {{
                    color: #67e8f9;
                }}

                .model-verdict {{
                    display: flex;
                    align-items: center;
                    gap: 0.55rem;

                    margin-top: 0.8rem;
                    padding: 0.7rem 0.8rem;

                    border-radius: 12px;

                    font-size: 0.75rem;
                    font-weight: 680;
                }}

                .verdict-loss {{
                    color: #fdba74;
                    background: rgba(249, 115, 22, 0.09);
                }}

                .verdict-preserved {{
                    color: #d8b4fe;
                    background: rgba(168, 85, 247, 0.09);
                }}

                .verdict-global {{
                    color: #67e8f9;
                    background: rgba(34, 211, 238, 0.085);
                }}

                .verdict-dot {{
                    flex: 0 0 8px;
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: currentColor;
                    box-shadow: 0 0 10px currentColor;
                }}

                .final-thesis {{
                    position: relative;
                    overflow: hidden;

                    display: grid;
                    grid-template-columns:
                        minmax(0, 1.55fr)
                        minmax(240px, 0.75fr);

                    gap: 1rem;
                    align-items: center;

                    margin-top: 1.25rem;
                    padding: 1.4rem;

                    border: 1px solid rgba(192, 132, 252, 0.22);
                    border-radius: 19px;

                    background:
                        linear-gradient(
                            135deg,
                            rgba(168, 85, 247, 0.115),
                            rgba(34, 211, 238, 0.04)
                        );
                }}

                .thesis-label {{
                    color: #c084fc;
                    font-size: 0.67rem;
                    font-weight: 800;
                    letter-spacing: 0.12em;
                    text-transform: uppercase;
                }}

                .thesis-title {{
                    margin: 0.35rem 0 0.5rem;

                    color: white;
                    font-size: 1.25rem;
                    font-weight: 820;
                }}

                .thesis-text {{
                    margin: 0;

                    color: #aeb8cf;
                    font-size: 0.88rem;
                    line-height: 1.65;
                }}

                .thesis-formula {{
                    padding: 1.1rem;

                    border: 1px solid rgba(255, 255, 255, 0.09);
                    border-radius: 15px;

                    background: rgba(5, 8, 20, 0.58);
                    text-align: center;
                }}

                .thesis-formula strong {{
                    display: block;

                    background:
                        linear-gradient(
                            90deg,
                            #d8b4fe,
                            #67e8f9
                        );

                    background-clip: text;
                    -webkit-background-clip: text;
                    color: transparent;

                    font-size: 1.03rem;
                    font-weight: 820;
                }}

                .thesis-formula span {{
                    display: block;
                    margin-top: 0.35rem;

                    color: #7f8aa2;
                    font-size: 0.68rem;
                }}

                @media (max-width: 850px) {{
                    .comparison-cards,
                    .final-thesis {{
                        grid-template-columns: 1fr;
                    }}

                    .comparison-cards::before {{
                        display: none;
                    }}

                    .comparison-card {{
                        min-height: auto;
                    }}

                    .model-description {{
                        min-height: auto;
                    }}
                }}
            </style>

            <div class="comparison-heading">
                <div class="comparison-kicker">
                    Síntesis del experimento
                </div>

                <div class="comparison-title">
                    Perder acceso no siempre significa destruir
                    información
                </div>

                <div class="comparison-description">
                    AND elimina distinciones entre entradas. CNOT
                    conserva una correspondencia uno a uno. El circuito
                    cuántico mantiene la información en el estado global,
                    aunque temporalmente deje de estar localizada.
                </div>
            </div>

            <div class="comparison-cards">
                <article class="comparison-card">
                    <div class="model-symbol symbol-and">
                        AND
                    </div>

                    <div class="model-type">
                        Lógica irreversible
                    </div>

                    <div class="model-name">
                        Distinciones eliminadas
                    </div>

                    <p class="model-description">
                        Varias entradas distintas producen la misma
                        salida. Conocer el resultado no permite determinar
                        de forma única cuál fue la entrada original.
                    </p>

                    <div class="result-box">
                        <span class="result-label">
                            Entradas identificables
                        </span>

                        <span class="result-value result-orange">
                            {resultados["unicidad_and"]:.0f} %
                        </span>
                    </div>

                    <div class="result-box">
                        <span class="result-label">
                            Entradas en colisión
                        </span>

                        <span class="result-value">
                            {resultados["entradas_colisionadas_and"]} de 4
                        </span>
                    </div>

                    <div class="model-verdict verdict-loss">
                        <span class="verdict-dot"></span>
                        Información lógica perdida
                    </div>
                </article>

                <article class="comparison-card">
                    <div class="model-symbol symbol-cnot">
                        ↺
                    </div>

                    <div class="model-type">
                        Lógica reversible
                    </div>

                    <div class="model-name">
                        Correspondencia conservada
                    </div>

                    <p class="model-description">
                        Cada entrada produce una salida diferente. La
                        misma puerta CNOT puede aplicarse nuevamente
                        para reconstruir exactamente el estado inicial.
                    </p>

                    <div class="result-box">
                        <span class="result-label">
                            Recuperación comprobada
                        </span>

                        <span class="result-value result-purple">
                            {resultados["recuperacion_cnot"]:.0f} %
                        </span>
                    </div>

                    <div class="result-box">
                        <span class="result-label">
                            Colisiones
                        </span>

                        <span class="result-value">
                            0
                        </span>
                    </div>

                    <div class="model-verdict verdict-preserved">
                        <span class="verdict-dot"></span>
                        Información recuperable
                    </div>
                </article>

                <article class="comparison-card">
                    <div class="model-symbol symbol-quantum">
                        ⚛
                    </div>

                    <div class="model-type">
                        Transformación unitaria
                    </div>

                    <div class="model-name">
                        Información distribuida
                    </div>

                    <p class="model-description">
                        El estado deja de estar contenido en un solo
                        cúbit y pasa a depender de amplitudes, fases y
                        correlaciones del sistema completo.
                    </p>

                    <div class="result-box">
                        <span class="result-label">
                            Fidelidad ideal
                        </span>

                        <span class="result-value result-cyan">
                            {resultados["fidelidad_cuantica"]:.2f} %
                        </span>
                    </div>

                    <div class="result-box">
                        <span class="result-label">
                            Recuperación
                        </span>

                        <span class="result-value">
                            Circuito inverso
                        </span>
                    </div>

                    <div class="model-verdict verdict-global">
                        <span class="verdict-dot"></span>
                        Información conservada globalmente
                    </div>
                </article>
            </div>

            <div class="final-thesis">
                <div>
                    <div class="thesis-label">
                        Conclusión central
                    </div>

                    <div class="thesis-title">
                        La accesibilidad local y la conservación global
                        no son lo mismo
                    </div>

                    <p class="thesis-text">
                        El modelo cuántico demuestra que una información
                        puede resultar inaccesible al observar una parte
                        aislada del sistema y, aun así, permanecer
                        codificada en las correlaciones globales.
                    </p>
                </div>

                <div class="thesis-formula">
                    <strong>
                        No localizada ≠ destruida
                    </strong>

                    <span>
                        Idea que conecta el circuito con la paradoja
                        de la información
                    </span>
                </div>
            </div>
        </section>
        """
    )

    st.subheader("Matriz comparativa")

    tabla = pd.DataFrame(
        [
            {
                "Modelo": "Puerta AND",
                "Tipo": "Irreversible",
                "Relación": "Muchos a uno",
                "¿Tiene inversa?": "No",
                "Resultado": "Pierde distinción entre entradas",
            },
            {
                "Modelo": "Puerta CNOT",
                "Tipo": "Reversible",
                "Relación": "Uno a uno",
                "¿Tiene inversa?": "Sí",
                "Resultado": "Recupera exactamente la entrada",
            },
            {
                "Modelo": "Circuito cuántico",
                "Tipo": "Unitario",
                "Relación": "Estado global reversible",
                "¿Tiene inversa?": "Sí",
                "Resultado": "Distribuye y recupera información",
            },
        ]
    )

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
    )

    st.success(
        """
        En la simulación ideal, el circuito inverso recupera el estado
        inicial con fidelidad del 100 %. Esto no resuelve físicamente
        la paradoja de los agujeros negros, pero muestra de forma
        computacional que información no localizada no equivale
        necesariamente a información destruida.
        """
    )

    st.caption(
        """
        La comparación utiliza un modelo lógico y cuántico simplificado.
        No incluye gravedad, geometría del espacio-tiempo ni radiación
        de Hawking física.
        """
    )