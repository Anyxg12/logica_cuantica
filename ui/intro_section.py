import streamlit as st

from logic.irreversible import detectar_colisiones
from logic.reversible import (
    comprobar_recuperacion,
    tiene_colisiones,
)
from quantum.engine import ejecutar_motor


def render_intro() -> None:
    """
    Renderiza una introducción visual al recorrido lógico
    de la aplicación.
    """

    colisiones_and = detectar_colisiones()
    entradas_colisionadas = len(colisiones_and.get(0, []))

    recuperacion_cnot = comprobar_recuperacion()
    porcentaje_cnot = (
        sum(recuperacion_cnot.values())
        / len(recuperacion_cnot)
        * 100
    )

    resultado_cuantico = ejecutar_motor(
        theta_grados=120,
        phi_grados=95,
    )

    fidelidad_cuantica = (
        resultado_cuantico.fidelidad * 100
    )

    st.html(
        f"""
        <section class="intro-journey">
            <style>
                .intro-journey {{
                    position: relative;
                    overflow: hidden;

                    padding: 2.2rem;
                    margin-top: 1rem;

                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: 26px;

                    background:
                        radial-gradient(
                            circle at 85% 15%,
                            rgba(168, 85, 247, 0.15),
                            transparent 30%
                        ),
                        radial-gradient(
                            circle at 10% 80%,
                            rgba(34, 211, 238, 0.08),
                            transparent 28%
                        ),
                        linear-gradient(
                            145deg,
                            rgba(15, 19, 36, 0.91),
                            rgba(7, 10, 23, 0.94)
                        );

                    box-shadow:
                        0 25px 70px rgba(0, 0, 0, 0.30);
                }}

                .intro-heading {{
                    max-width: 790px;
                    margin-bottom: 2.2rem;
                }}

                .intro-kicker {{
                    color: #c084fc;
                    font-size: 0.72rem;
                    font-weight: 800;
                    letter-spacing: 0.14em;
                    text-transform: uppercase;
                }}

                .intro-title {{
                    margin: 0.45rem 0 0.7rem;

                    color: white;
                    font-size: clamp(1.8rem, 4vw, 3rem);
                    font-weight: 830;
                    line-height: 1.06;
                    letter-spacing: -0.045em;
                }}

                .intro-text {{
                    color: #aeb8cf;
                    font-size: 1rem;
                    line-height: 1.7;
                }}

                .journey-grid {{
                    position: relative;

                    display: grid;
                    grid-template-columns:
                        repeat(3, minmax(0, 1fr));

                    gap: 1rem;
                }}

                .journey-grid::before {{
                    content: "";

                    position: absolute;
                    top: 46px;
                    left: 15%;
                    right: 15%;

                    height: 2px;

                    background:
                        linear-gradient(
                            90deg,
                            #f97316,
                            #a855f7,
                            #22d3ee
                        );

                    opacity: 0.42;
                }}

                .journey-card {{
                    position: relative;
                    z-index: 2;
                    overflow: hidden;

                    min-height: 320px;
                    padding: 1.35rem;

                    border: 1px solid rgba(255, 255, 255, 0.11);
                    border-radius: 20px;

                    background:
                        linear-gradient(
                            150deg,
                            rgba(255, 255, 255, 0.065),
                            rgba(255, 255, 255, 0.018)
                        );

                    backdrop-filter: blur(12px);

                    transition:
                        transform 0.25s ease,
                        border-color 0.25s ease,
                        box-shadow 0.25s ease;
                }}

                .journey-card:hover {{
                    transform: translateY(-6px);

                    border-color:
                        rgba(192, 132, 252, 0.38);

                    box-shadow:
                        0 22px 55px rgba(0, 0, 0, 0.28),
                        0 0 35px rgba(168, 85, 247, 0.07);
                }}

                .journey-icon {{
                    position: relative;

                    display: grid;
                    place-items: center;

                    width: 58px;
                    height: 58px;
                    margin-bottom: 1rem;

                    border-radius: 18px;

                    font-size: 1.55rem;
                    font-weight: 850;
                }}

                .icon-and {{
                    color: #fdba74;
                    background: rgba(249, 115, 22, 0.13);
                    border: 1px solid rgba(249, 115, 22, 0.28);
                }}

                .icon-cnot {{
                    color: #d8b4fe;
                    background: rgba(168, 85, 247, 0.13);
                    border: 1px solid rgba(168, 85, 247, 0.28);
                }}

                .icon-quantum {{
                    color: #67e8f9;
                    background: rgba(34, 211, 238, 0.12);
                    border: 1px solid rgba(34, 211, 238, 0.27);
                }}

                .journey-number {{
                    position: absolute;
                    top: -7px;
                    right: -7px;

                    display: grid;
                    place-items: center;

                    width: 24px;
                    height: 24px;

                    border-radius: 50%;
                    background: #0a0e1d;
                    border: 1px solid rgba(255, 255, 255, 0.15);

                    color: white;
                    font-size: 0.67rem;
                }}

                .journey-card h3 {{
                    margin: 0 0 0.6rem;
                    color: white;
                    font-size: 1.25rem;
                }}

                .journey-card p {{
                    min-height: 102px;
                    margin: 0;

                    color: #aeb8cf;
                    font-size: 0.88rem;
                    line-height: 1.6;
                }}

                .journey-status {{
                    margin-top: 1.15rem;
                    padding: 0.85rem;

                    border-radius: 13px;
                    background: rgba(7, 10, 22, 0.70);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                }}

                .status-label {{
                    display: block;
                    margin-bottom: 0.28rem;

                    color: #7f8aa2;
                    font-size: 0.63rem;
                    font-weight: 750;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                }}

                .status-value {{
                    display: block;

                    color: white;
                    font-size: 0.94rem;
                    font-weight: 760;
                }}

                .status-orange {{
                    color: #fb923c;
                }}

                .status-purple {{
                    color: #c084fc;
                }}

                .status-cyan {{
                    color: #67e8f9;
                }}

                .intro-conclusion {{
                    display: grid;
                    grid-template-columns:
                        repeat(3, minmax(0, 1fr));

                    gap: 0.75rem;
                    margin-top: 1.3rem;
                }}

                .conclusion-item {{
                    padding: 0.9rem;

                    border-radius: 14px;
                    border: 1px solid rgba(255, 255, 255, 0.09);

                    background: rgba(255, 255, 255, 0.028);
                    text-align: center;
                }}

                .conclusion-item strong {{
                    display: block;
                    color: white;
                    font-size: 0.82rem;
                }}

                .conclusion-item span {{
                    display: block;
                    margin-top: 0.28rem;

                    color: #8792aa;
                    font-size: 0.69rem;
                }}

                @media (max-width: 850px) {{
                    .journey-grid,
                    .intro-conclusion {{
                        grid-template-columns: 1fr;
                    }}

                    .journey-grid::before {{
                        display: none;
                    }}

                    .journey-card {{
                        min-height: auto;
                    }}

                    .journey-card p {{
                        min-height: auto;
                    }}
                }}
            </style>

            <div class="intro-heading">
                <div class="intro-kicker">
                    Recorrido conceptual
                </div>

                <div class="intro-title">
                    Tres maneras de transformar información
                </div>

                <div class="intro-text">
                    La aplicación avanza desde una operación clásica
                    que pierde información, pasa por una transformación
                    reversible y culmina en un circuito cuántico donde
                    la información se distribuye entre correlaciones.
                </div>
            </div>

            <div class="journey-grid">
                <article class="journey-card">
                    <div class="journey-icon icon-and">
                        AND
                        <span class="journey-number">1</span>
                    </div>

                    <h3>Lógica irreversible</h3>

                    <p>
                        Varias entradas diferentes producen una misma
                        salida. Una vez ejecutada la operación, no siempre
                        puede reconstruirse el estado original.
                    </p>

                    <div class="journey-status">
                        <span class="status-label">
                            Resultado observado
                        </span>

                        <span class="status-value status-orange">
                            {entradas_colisionadas} entradas → salida 0
                        </span>
                    </div>
                </article>

                <article class="journey-card">
                    <div class="journey-icon icon-cnot">
                        ↺
                        <span class="journey-number">2</span>
                    </div>

                    <h3>Lógica reversible</h3>

                    <p>
                        CNOT conserva una correspondencia única entre
                        entradas y salidas. Aplicar la transformación
                        nuevamente recupera la información inicial.
                    </p>

                    <div class="journey-status">
                        <span class="status-label">
                            Recuperación clásica
                        </span>

                        <span class="status-value status-purple">
                            {porcentaje_cnot:.0f} % de las entradas
                        </span>
                    </div>
                </article>

                <article class="journey-card">
                    <div class="journey-icon icon-quantum">
                        ⚛
                        <span class="journey-number">3</span>
                    </div>

                    <h3>Información cuántica</h3>

                    <p>
                        Las puertas unitarias distribuyen amplitudes y
                        fases entre varios cúbits. La información deja
                        de estar localizada, pero permanece en el sistema.
                    </p>

                    <div class="journey-status">
                        <span class="status-label">
                            Fidelidad ideal
                        </span>

                        <span class="status-value status-cyan">
                            {fidelidad_cuantica:.6f} %
                        </span>
                    </div>
                </article>
            </div>

            <div class="intro-conclusion">
                <div class="conclusion-item">
                    <strong>AND</strong>
                    <span>Pérdida lógica</span>
                </div>

                <div class="conclusion-item">
                    <strong>CNOT</strong>
                    <span>Recuperación reversible</span>
                </div>

                <div class="conclusion-item">
                    <strong>Circuito cuántico</strong>
                    <span>Información distribuida globalmente</span>
                </div>
            </div>
        </section>
        """
    )

    st.info(
        """
        La paradoja de la información de los agujeros negros se utiliza
        como contexto conceptual. El programa no reproduce un agujero
        negro físico ni fenómenos de relatividad general.
        """
    )