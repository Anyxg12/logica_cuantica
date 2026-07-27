import streamlit as st


def aplicar_estilos() -> None:
    """
    Aplica la identidad visual general de la aplicación.

    El diseño utiliza una estética espacial oscura con detalles
    en violeta, cian y naranja, coherente con el modelo visual
    del agujero negro.
    """

    st.markdown(
        """
        <style>
        /* =====================================================
           VARIABLES GENERALES
        ===================================================== */

        :root {
            --bg-main: #060814;
            --bg-secondary: #0d1120;
            --surface: rgba(18, 23, 42, 0.78);
            --surface-light: rgba(255, 255, 255, 0.055);
            --border: rgba(148, 163, 184, 0.17);

            --purple: #a855f7;
            --purple-soft: #c084fc;
            --cyan: #22d3ee;
            --orange: #f97316;
            --green: #4ade80;

            --text-primary: #f8fafc;
            --text-secondary: #aeb8cf;
        }


        /* =====================================================
           FONDO DE LA APLICACIÓN
        ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 78% 8%,
                    rgba(126, 34, 206, 0.17),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 12% 35%,
                    rgba(8, 145, 178, 0.10),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 70% 80%,
                    rgba(249, 115, 22, 0.055),
                    transparent 24%
                ),
                linear-gradient(
                    180deg,
                    #050711 0%,
                    #080b18 48%,
                    #060814 100%
                );
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;

            background-image:
                radial-gradient(
                    circle,
                    rgba(255, 255, 255, 0.45) 0 0.7px,
                    transparent 0.9px
                ),
                radial-gradient(
                    circle,
                    rgba(168, 85, 247, 0.28) 0 0.8px,
                    transparent 1px
                );

            background-size:
                73px 73px,
                119px 119px;

            background-position:
                0 0,
                31px 47px;

            opacity: 0.32;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: rgba(5, 7, 17, 0.72);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.055);
        }

        [data-testid="stToolbar"] {
            right: 1rem;
        }


        /* =====================================================
           CONTENEDOR PRINCIPAL
        ===================================================== */

        .block-container {
            position: relative;
            z-index: 1;

            max-width: 1280px;
            padding-top: 2.4rem;
            padding-bottom: 5rem;
        }


        /* =====================================================
           TIPOGRAFÍA
        ===================================================== */

        h1, h2, h3, h4 {
            color: var(--text-primary);
            letter-spacing: -0.025em;
        }

        h1 {
            font-size: clamp(2.3rem, 5vw, 4.4rem) !important;
            font-weight: 850 !important;
            line-height: 1.02 !important;

            background:
                linear-gradient(
                    90deg,
                    #ffffff 0%,
                    #d8b4fe 50%,
                    #67e8f9 100%
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        h2 {
            margin-top: 2rem !important;
            font-weight: 780 !important;
        }

        h3 {
            font-weight: 720 !important;
        }

        p, li {
            color: var(--text-secondary);
            line-height: 1.65;
        }

        .hero-subtitle {
            max-width: 880px;
            color: #b9c2d8;
            font-size: 1.12rem;
            line-height: 1.65;
            margin-top: -0.4rem;
            margin-bottom: 1.8rem;
        }

        .accent {
            color: var(--purple-soft);
            font-weight: 750;
        }


        /* =====================================================
           PESTAÑAS
        ===================================================== */

        div[data-baseweb="tab-list"] {
            gap: 0.4rem;
            padding: 0.42rem;

            border: 1px solid var(--border);
            border-radius: 16px;

            background: rgba(9, 13, 27, 0.72);
            backdrop-filter: blur(14px);
        }

        button[data-baseweb="tab"] {
            height: auto;
            min-height: 42px;

            padding: 0.55rem 0.9rem;
            border-radius: 11px;

            color: #9ca7bf;
            font-weight: 650;

            transition:
                color 0.2s ease,
                background 0.2s ease,
                transform 0.2s ease;
        }

        button[data-baseweb="tab"]:hover {
            color: white;
            background: rgba(168, 85, 247, 0.09);
            transform: translateY(-1px);
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: white;
            background:
                linear-gradient(
                    135deg,
                    rgba(168, 85, 247, 0.27),
                    rgba(34, 211, 238, 0.10)
                );

            box-shadow:
                inset 0 0 0 1px rgba(192, 132, 252, 0.32),
                0 8px 25px rgba(88, 28, 135, 0.15);
        }

        div[data-baseweb="tab-highlight"] {
            display: none;
        }


        /* =====================================================
           MÉTRICAS
        ===================================================== */

        [data-testid="stMetric"] {
            position: relative;
            overflow: hidden;

            min-height: 112px;
            padding: 1.1rem 1.15rem;

            border: 1px solid var(--border);
            border-radius: 18px;

            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.065),
                    rgba(255, 255, 255, 0.025)
                );

            box-shadow:
                0 16px 40px rgba(0, 0, 0, 0.17);

            backdrop-filter: blur(12px);

            transition:
                transform 0.25s ease,
                border-color 0.25s ease,
                box-shadow 0.25s ease;
        }

        [data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;

            width: 100%;
            height: 2px;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    var(--purple),
                    var(--cyan),
                    transparent
                );

            opacity: 0.78;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: rgba(192, 132, 252, 0.35);

            box-shadow:
                0 20px 48px rgba(0, 0, 0, 0.26),
                0 0 30px rgba(168, 85, 247, 0.07);
        }

        [data-testid="stMetricLabel"] {
            color: #9ca7bf;
            font-weight: 620;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff;
            font-weight: 760;
            letter-spacing: -0.035em;
        }


        /* =====================================================
           TARJETAS PERSONALIZADAS
        ===================================================== */

        .concept-card {
            position: relative;
            overflow: hidden;

            min-height: 210px;
            padding: 1.45rem;

            border: 1px solid var(--border);
            border-radius: 20px;

            background:
                linear-gradient(
                    150deg,
                    rgba(255, 255, 255, 0.065),
                    rgba(255, 255, 255, 0.018)
                );

            box-shadow:
                0 18px 46px rgba(0, 0, 0, 0.19);

            backdrop-filter: blur(14px);

            transition:
                transform 0.28s ease,
                border-color 0.28s ease,
                box-shadow 0.28s ease;
        }

        .concept-card::after {
            content: "";
            position: absolute;
            width: 130px;
            height: 130px;
            right: -55px;
            top: -55px;
            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(168, 85, 247, 0.24),
                    transparent 68%
                );
        }

        .concept-card:hover {
            transform: translateY(-5px);
            border-color: rgba(192, 132, 252, 0.38);

            box-shadow:
                0 24px 58px rgba(0, 0, 0, 0.28),
                0 0 40px rgba(168, 85, 247, 0.075);
        }

        .concept-card h3 {
            position: relative;
            z-index: 1;

            margin-top: 0;
            margin-bottom: 0.65rem;

            color: white;
        }

        .concept-card p {
            position: relative;
            z-index: 1;

            color: #aeb8cf;
            font-size: 0.94rem;
        }


        /* =====================================================
           ALERTAS
        ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.11);
            backdrop-filter: blur(12px);

            box-shadow:
                0 12px 32px rgba(0, 0, 0, 0.13);
        }


        /* =====================================================
           TABLAS
        ===================================================== */

        [data-testid="stDataFrame"] {
            overflow: hidden;

            border: 1px solid var(--border);
            border-radius: 16px;

            background: rgba(10, 14, 29, 0.65);

            box-shadow:
                0 16px 38px rgba(0, 0, 0, 0.16);
        }


        /* =====================================================
           BOTONES
        ===================================================== */

        .stButton > button,
        .stDownloadButton > button {
            min-height: 44px;

            border: 1px solid rgba(192, 132, 252, 0.36);
            border-radius: 999px;

            color: white;

            background:
                linear-gradient(
                    135deg,
                    rgba(126, 34, 206, 0.92),
                    rgba(79, 70, 229, 0.88)
                );

            box-shadow:
                0 10px 28px rgba(88, 28, 135, 0.22);

            font-weight: 680;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                filter 0.2s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-2px);

            filter: brightness(1.12);

            box-shadow:
                0 14px 35px rgba(126, 34, 206, 0.32),
                0 0 24px rgba(168, 85, 247, 0.14);
        }

        .stButton > button:disabled {
            opacity: 0.35;
            transform: none;
            box-shadow: none;
        }


        /* =====================================================
           SLIDERS
        ===================================================== */

        [data-testid="stSlider"] {
            padding:
                0.85rem 0.95rem 0.65rem;

            border: 1px solid rgba(255, 255, 255, 0.075);
            border-radius: 15px;

            background: rgba(255, 255, 255, 0.025);
        }


        /* =====================================================
           SELECTORES Y RADIOS
        ===================================================== */

        [data-testid="stRadio"] {
            padding:
                0.75rem 0.9rem;

            border: 1px solid rgba(255, 255, 255, 0.075);
            border-radius: 14px;

            background: rgba(255, 255, 255, 0.025);
        }

        [data-baseweb="select"] > div {
            border-radius: 13px;
            border-color: rgba(255, 255, 255, 0.13);

            background: rgba(17, 22, 39, 0.85);
        }


        /* =====================================================
           EXPANDERS
        ===================================================== */

        [data-testid="stExpander"] {
            overflow: hidden;

            border: 1px solid var(--border);
            border-radius: 16px;

            background: rgba(255, 255, 255, 0.025);
        }


        /* =====================================================
           GRÁFICOS
        ===================================================== */

        [data-testid="stPlotlyChart"],
        [data-testid="stImage"],
        [data-testid="stPyplot"] {
            overflow: hidden;

            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 18px;

            background: rgba(8, 11, 24, 0.55);

            box-shadow:
                0 16px 42px rgba(0, 0, 0, 0.17);
        }


        /* =====================================================
           PROGRESO
        ===================================================== */

        [data-testid="stProgress"] > div > div {
            border-radius: 999px;

            background:
                linear-gradient(
                    90deg,
                    var(--purple),
                    var(--cyan)
                );

            box-shadow:
                0 0 16px rgba(168, 85, 247, 0.3);
        }


        /* =====================================================
           DIVISORES
        ===================================================== */

        hr {
            border: 0;
            height: 1px;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    rgba(192, 132, 252, 0.25),
                    rgba(34, 211, 238, 0.17),
                    transparent
                );
        }


        /* =====================================================
           BARRA DE DESPLAZAMIENTO
        ===================================================== */

        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #070914;
        }

        ::-webkit-scrollbar-thumb {
            border: 2px solid #070914;
            border-radius: 999px;

            background:
                linear-gradient(
                    180deg,
                    #7e22ce,
                    #0891b2
                );
        }


        /* =====================================================
           RESPONSIVE
        ===================================================== */

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            h1 {
                font-size: 2.5rem !important;
            }

            button[data-baseweb="tab"] {
                font-size: 0.78rem;
                padding-left: 0.62rem;
                padding-right: 0.62rem;
            }

            .concept-card {
                min-height: auto;
            }
        }

        @media (max-width: 600px) {
            .block-container {
                padding-top: 1.2rem;
            }

            h1 {
                font-size: 2.05rem !important;
            }

            .hero-subtitle {
                font-size: 0.98rem;
            }

            [data-testid="stMetric"] {
                min-height: 96px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )