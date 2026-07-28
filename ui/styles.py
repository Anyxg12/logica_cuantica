import streamlit as st


def aplicar_estilos() -> None:
    """
    Aplica la identidad visual general de la aplicación con un diseño espacial
    cinematográfico, glassmorphism premium y neón hiper-moderno.
    """

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        /* =====================================================
           VARIABLES GENERALES & TEMAS NEÓN
        ===================================================== */

        :root {
            --bg-main: #03050c;
            --bg-secondary: #080c1d;
            --surface: rgba(14, 19, 39, 0.72);
            --surface-hover: rgba(24, 31, 60, 0.85);
            --border: rgba(168, 85, 247, 0.18);
            --border-glow: rgba(56, 189, 248, 0.4);

            --purple: #a855f7;
            --purple-glow: #c084fc;
            --cyan: #38bdf8;
            --cyan-glow: #00f3ff;
            --emerald: #4ade80;
            --pink: #e879f9;

            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
        }

        /* =====================================================
           FONDO DE LA APLICACIÓN ESPACIAL
        ===================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 82% 12%,
                    rgba(168, 85, 247, 0.18),
                    transparent 35%
                ),
                radial-gradient(
                    circle at 18% 45%,
                    rgba(56, 189, 248, 0.14),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 75% 85%,
                    rgba(232, 121, 249, 0.08),
                    transparent 32%
                ),
                linear-gradient(
                    180deg,
                    #03050c 0%,
                    #070a19 45%,
                    #040612 100%
                ) !important;
            font-family: 'Inter', sans-serif !important;
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
                    rgba(255, 255, 255, 0.35) 0 0.8px,
                    transparent 1px
                ),
                radial-gradient(
                    circle,
                    rgba(168, 85, 247, 0.25) 0 0.9px,
                    transparent 1.1px
                );
            background-size: 85px 85px, 130px 130px;
            background-position: 0 0, 40px 60px;
            opacity: 0.28;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: rgba(4, 6, 15, 0.75) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* =====================================================
           CONTENEDOR PRINCIPAL & TIPOGRAFÍA
        ===================================================== */

        .block-container {
            position: relative;
            z-index: 1;
            max-width: 1300px;
            padding-top: 2.2rem;
            padding-bottom: 5rem;
        }

        h1, h2, h3, h4 {
            color: var(--text-primary);
            letter-spacing: -0.03em;
        }

        h1 {
            font-size: clamp(2.4rem, 5.5vw, 4.5rem) !important;
            font-weight: 850 !important;
            line-height: 1.04 !important;
            background: linear-gradient(100deg, #ffffff 10%, #d8b4fe 50%, #38bdf8 90%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem !important;
        }

        h2 {
            margin-top: 2.2rem !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #ffffff, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h3 {
            font-weight: 750 !important;
            color: #f1f5f9;
        }

        p, li {
            color: var(--text-secondary);
            line-height: 1.7;
            font-size: 1rem;
        }

        /* =====================================================
           PESTAÑAS NEÓN DE ALTA RESOLUCIÓN
        ===================================================== */

        div[data-baseweb="tab-list"] {
            gap: 0.5rem;
            padding: 0.5rem;
            border: 1px solid var(--border);
            border-radius: 18px;
            background: rgba(7, 11, 25, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.4);
        }

        button[data-baseweb="tab"] {
            min-height: 44px;
            padding: 0.6rem 1.1rem;
            border-radius: 12px;
            color: #94a3b8;
            font-weight: 650;
            font-size: 0.92rem;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        button[data-baseweb="tab"]:hover {
            color: #ffffff;
            background: rgba(168, 85, 247, 0.12);
            transform: translateY(-1px);
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ffffff !important;
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.35), rgba(56, 189, 248, 0.18)) !important;
            box-shadow: inset 0 0 0 1px rgba(192, 132, 252, 0.45), 0 8px 25px rgba(168, 85, 247, 0.25) !important;
        }

        div[data-baseweb="tab-highlight"] {
            display: none;
        }

        /* =====================================================
           TARJETAS DE MÉTRICAS STREAMLIT
        ===================================================== */

        [data-testid="stMetric"] {
            position: relative;
            overflow: hidden;
            min-height: 115px;
            padding: 1.15rem 1.25rem;
            border: 1px solid var(--border);
            border-radius: 20px;
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015));
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            transition: all 0.3s ease;
        }

        [data-testid="stMetric"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--purple), var(--cyan), transparent);
            opacity: 0.85;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: rgba(192, 132, 252, 0.45);
            box-shadow: 0 22px 50px rgba(0, 0, 0, 0.35), 0 0 35px rgba(168, 85, 247, 0.12);
        }

        [data-testid="stMetricLabel"] {
            color: #94a3b8;
            font-weight: 650;
            font-size: 0.85rem;
        }

        [data-testid="stMetricValue"] {
            color: #ffffff;
            font-weight: 800;
            letter-spacing: -0.03em;
            font-family: 'JetBrains Mono', monospace, sans-serif;
        }

        /* =====================================================
           BOTONES & CONTROLES SLIDER/RADIO
        ===================================================== */

        .stButton > button,
        .stDownloadButton > button {
            min-height: 46px;
            border: 1px solid rgba(192, 132, 252, 0.4);
            border-radius: 999px;
            color: white;
            background: linear-gradient(135deg, rgba(147, 51, 234, 0.95), rgba(79, 70, 229, 0.9));
            box-shadow: 0 10px 30px rgba(147, 51, 234, 0.3);
            font-weight: 700;
            letter-spacing: 0.02em;
            transition: all 0.25s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            filter: brightness(1.15);
            box-shadow: 0 14px 40px rgba(147, 51, 234, 0.45), 0 0 30px rgba(168, 85, 247, 0.25);
        }

        [data-testid="stSlider"] {
            padding: 0.9rem 1.1rem 0.7rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.025);
            backdrop-filter: blur(10px);
        }

        [data-testid="stRadio"] {
            padding: 0.85rem 1rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.025);
            backdrop-filter: blur(10px);
        }

        /* =====================================================
           ALERTAS & NOTIFICACIONES
        ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(14px);
            box-shadow: 0 14px 35px rgba(0, 0, 0, 0.2);
        }

        /* =====================================================
           BARRA DE DESPLAZAMIENTO
        ===================================================== */

        ::-webkit-scrollbar {
            width: 9px;
            height: 9px;
        }

        ::-webkit-scrollbar-track {
            background: #040612;
        }

        ::-webkit-scrollbar-thumb {
            border: 2px solid #040612;
            border-radius: 999px;
            background: linear-gradient(180deg, #9333ea, #0284c7);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )