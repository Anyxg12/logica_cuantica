import streamlit as st

from ui.black_hole_visual import (
    RUTA_IMAGEN,
    cargar_imagen_base64,
)


def render_hero() -> None:
    """
    Renderiza la cabecera cinematográfica principal
    de la aplicación.
    """

    try:
        imagen_uri = cargar_imagen_base64(
            str(RUTA_IMAGEN)
        )

    except FileNotFoundError:
        imagen_uri = ""

    fondo_imagen = (
        f'url("{imagen_uri}")'
        if imagen_uri
        else "none"
    )

    st.html(
        f"""
        <section class="main-hero">
            <style>
                .main-hero {{
                    position: relative;
                    overflow: hidden;

                    min-height: 485px;
                    margin-bottom: 1.5rem;
                    padding: 3.3rem;

                    border: 1px solid rgba(255, 255, 255, 0.13);
                    border-radius: 28px;

                    background:
                        linear-gradient(
                            90deg,
                            rgba(4, 7, 18, 0.98) 0%,
                            rgba(5, 8, 20, 0.94) 36%,
                            rgba(5, 8, 20, 0.42) 68%,
                            rgba(5, 8, 20, 0.18) 100%
                        ),
                        linear-gradient(
                            180deg,
                            transparent 55%,
                            rgba(3, 5, 14, 0.85) 100%
                        ),
                        {fondo_imagen}
                        66% center / cover no-repeat;

                    box-shadow:
                        0 30px 90px rgba(0, 0, 0, 0.46),
                        inset 0 0 80px rgba(5, 8, 20, 0.24);
                }}

                .main-hero::before {{
                    content: "";
                    position: absolute;
                    inset: 0;
                    pointer-events: none;

                    background:
                        radial-gradient(
                            circle at 77% 45%,
                            rgba(249, 115, 22, 0.18),
                            transparent 22%
                        ),
                        radial-gradient(
                            circle at 52% 42%,
                            rgba(34, 211, 238, 0.09),
                            transparent 22%
                        );
                }}

                .main-hero::after {{
                    content: "";
                    position: absolute;
                    inset: 0;
                    pointer-events: none;

                    background-image:
                        radial-gradient(
                            circle,
                            rgba(255, 255, 255, 0.5) 0 0.7px,
                            transparent 0.9px
                        );

                    background-size: 61px 61px;
                    opacity: 0.18;
                }}

                .hero-content {{
                    position: relative;
                    z-index: 3;

                    max-width: 660px;
                }}

                .hero-kicker {{
                    display: inline-flex;
                    align-items: center;
                    gap: 0.55rem;

                    margin-bottom: 1rem;
                    padding: 0.42rem 0.75rem;

                    border: 1px solid rgba(192, 132, 252, 0.32);
                    border-radius: 999px;

                    color: #d8b4fe;
                    background: rgba(168, 85, 247, 0.10);

                    font-size: 0.73rem;
                    font-weight: 760;
                    letter-spacing: 0.11em;
                    text-transform: uppercase;
                }}

                .hero-dot {{
                    width: 7px;
                    height: 7px;
                    border-radius: 50%;

                    background: #4ade80;

                    box-shadow:
                        0 0 8px #4ade80,
                        0 0 16px rgba(74, 222, 128, 0.5);

                    animation: hero-pulse 2.3s ease-in-out infinite;
                }}

                .hero-title {{
                    margin: 0;
                    max-width: 650px;

                    color: white;
                    font-size: clamp(2.8rem, 6vw, 5rem);
                    font-weight: 880;
                    line-height: 0.98;
                    letter-spacing: -0.055em;

                    text-shadow:
                        0 8px 40px rgba(0, 0, 0, 0.48);
                }}

                .hero-title span {{
                    background:
                        linear-gradient(
                            90deg,
                            #d8b4fe,
                            #a855f7 46%,
                            #67e8f9
                        );

                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                }}

                .hero-description {{
                    max-width: 610px;
                    margin: 1.35rem 0 1.5rem;

                    color: #b9c3d9;
                    font-size: 1.05rem;
                    line-height: 1.7;

                    text-shadow:
                        0 4px 18px rgba(0, 0, 0, 0.7);
                }}

                .hero-tags {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.65rem;
                    margin-bottom: 1.65rem;
                }}

                .hero-tag {{
                    display: inline-flex;
                    align-items: center;
                    gap: 0.45rem;

                    padding: 0.55rem 0.75rem;

                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: 12px;

                    color: #dce4f5;
                    background: rgba(10, 14, 29, 0.63);

                    font-size: 0.77rem;
                    font-weight: 620;

                    backdrop-filter: blur(10px);
                }}

                .hero-tag-icon {{
                    color: #67e8f9;
                    font-size: 0.92rem;
                }}

                .hero-status {{
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 0.7rem;

                    max-width: 620px;
                }}

                .hero-status-card {{
                    position: relative;
                    overflow: hidden;

                    padding: 0.9rem;

                    border: 1px solid rgba(255, 255, 255, 0.11);
                    border-radius: 14px;

                    background:
                        linear-gradient(
                            145deg,
                            rgba(18, 23, 42, 0.82),
                            rgba(9, 13, 28, 0.62)
                        );

                    backdrop-filter: blur(12px);
                }}

                .hero-status-card::before {{
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

                .hero-status-label {{
                    display: block;
                    margin-bottom: 0.3rem;

                    color: #8994ac;
                    font-size: 0.66rem;
                    font-weight: 650;
                    letter-spacing: 0.07em;
                    text-transform: uppercase;
                }}

                .hero-status-value {{
                    color: #f8fafc;
                    font-size: 0.84rem;
                    font-weight: 720;
                }}

                .hero-footnote {{
                    position: absolute;
                    z-index: 4;
                    right: 1.4rem;
                    bottom: 1.15rem;

                    max-width: 365px;
                    padding: 0.65rem 0.85rem;

                    border: 1px solid rgba(255, 255, 255, 0.10);
                    border-radius: 11px;

                    color: #8e99b1;
                    background: rgba(4, 7, 18, 0.66);

                    font-size: 0.66rem;
                    line-height: 1.45;
                    text-align: right;

                    backdrop-filter: blur(10px);
                }}

                @keyframes hero-pulse {{
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
                    .main-hero {{
                        min-height: auto;
                        padding: 2.2rem 1.5rem 6rem;

                        background:
                            linear-gradient(
                                180deg,
                                rgba(4, 7, 18, 0.89),
                                rgba(4, 7, 18, 0.97)
                            ),
                            {fondo_imagen}
                            center center / cover no-repeat;
                    }}

                    .hero-status {{
                        grid-template-columns: 1fr;
                    }}

                    .hero-footnote {{
                        left: 1.5rem;
                        right: 1.5rem;
                        text-align: left;
                    }}
                }}

                @media (max-width: 520px) {{
                    .hero-title {{
                        font-size: 2.55rem;
                    }}

                    .hero-description {{
                        font-size: 0.94rem;
                    }}

                    .hero-tags {{
                        gap: 0.45rem;
                    }}
                }}
            </style>

            <div class="hero-content">
                <div class="hero-kicker">
                    <span class="hero-dot"></span>
                    Proyecto final · Lógica matemática
                </div>

                <h1 class="hero-title">
                    ¿Se destruye la
                    <span>información?</span>
                </h1>

                <p class="hero-description">
                    Una simulación interactiva que compara lógica
                    irreversible, lógica reversible y circuitos cuánticos
                    mediante un modelo inspirado en la paradoja de la
                    información de los agujeros negros.
                </p>

                <div class="hero-tags">
                    <div class="hero-tag">
                        <span class="hero-tag-icon">◇</span>
                        Python + Qiskit
                    </div>

                    <div class="hero-tag">
                        <span class="hero-tag-icon">↺</span>
                        Computación reversible
                    </div>

                    <div class="hero-tag">
                        <span class="hero-tag-icon">⚛</span>
                        Estados cuánticos
                    </div>

                    <div class="hero-tag">
                        <span class="hero-tag-icon">◉</span>
                        Streamlit interactivo
                    </div>
                </div>

                <div class="hero-status">
                    <div class="hero-status-card">
                        <span class="hero-status-label">
                            Motor
                        </span>

                        <span class="hero-status-value">
                            Validado con pruebas
                        </span>
                    </div>

                    <div class="hero-status-card">
                        <span class="hero-status-label">
                            Recuperación ideal
                        </span>

                        <span class="hero-status-value">
                            Fidelidad del 100 %
                        </span>
                    </div>

                    <div class="hero-status-card">
                        <span class="hero-status-label">
                            Modelo físico
                        </span>

                        <span class="hero-status-value">
                            Ruido configurable
                        </span>
                    </div>
                </div>
            </div>

            <div class="hero-footnote">
                Analogía computacional y didáctica. No reproduce
                relatividad general ni un agujero negro físico real.
            </div>
        </section>
        """
    )