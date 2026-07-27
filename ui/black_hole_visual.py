import base64
from html import escape
from pathlib import Path

import streamlit as st

from quantum.engine import ResultadoMotor
from quantum.metrics import calcular_metricas_sistema


ETAPAS = [
    "Entrada",
    "Distribución",
    "Radiación",
    "Recuperación",
]

RUTA_IMAGEN = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "images"
    / "black_hole.png"
)


@st.cache_data(show_spinner=False)
def cargar_imagen_base64(ruta: str) -> str:
    """
    Convierte una imagen local en una URI Base64.

    Esto permite utilizarla dentro del HTML sin depender
    de una dirección externa.
    """
    ruta_imagen = Path(ruta)

    if not ruta_imagen.exists():
        raise FileNotFoundError(
            f"No se encontró la imagen: {ruta_imagen}"
        )

    contenido = ruta_imagen.read_bytes()
    codificada = base64.b64encode(contenido).decode("utf-8")

    extension = ruta_imagen.suffix.lower()

    tipos_mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    mime = tipos_mime.get(extension, "image/png")

    return f"data:{mime};base64,{codificada}"


def obtener_datos_etapa(
    resultado: ResultadoMotor,
    etapa: str,
) -> tuple[float, float, str, str]:
    """
    Devuelve las métricas y textos correspondientes
    a la etapa seleccionada.
    """

    if etapa == "Entrada":
        estado = resultado.estado_inicial
        estado_sistema = "Información localizada"
        mensaje = (
            "El estado preparado mediante θ y φ se encuentra "
            "principalmente en el primer cúbit."
        )

    elif etapa == "Distribución":
        estado = resultado.estado_distribuido
        estado_sistema = "Información entrelazada"
        mensaje = (
            "Las puertas unitarias distribuyen la información "
            "entre los tres cúbits mediante correlaciones."
        )

    elif etapa == "Radiación":
        estado = resultado.estado_distribuido
        estado_sistema = "Información no localizada"
        mensaje = (
            "La información no puede identificarse observando "
            "un solo cúbit, pero continúa presente globalmente."
        )

    else:
        estado = resultado.estado_recuperado
        estado_sistema = "Estado reconstruido"
        mensaje = (
            "La transformación inversa recupera el estado "
            "cuántico preparado originalmente."
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

    return (
        entropia_promedio,
        pureza_promedio,
        estado_sistema,
        mensaje,
    )


def crear_html_visual(
    imagen_uri: str,
    etapa: str,
    entropia: float,
    pureza: float,
    fidelidad: float,
    estado_sistema: str,
) -> str:
    """
    Construye el panel visual cinematográfico del modelo.
    """

    indice = ETAPAS.index(etapa)

    opacidad_entrada = "1" if indice <= 1 else "0.25"
    opacidad_salida = "1" if indice >= 2 else "0.20"

    intensidad_cian = (
        "1"
        if etapa in ("Entrada", "Distribución")
        else "0.35"
    )

    intensidad_violeta = (
        "1"
        if etapa in ("Radiación", "Recuperación")
        else "0.30"
    )

    pasos_html = ""

    for posicion, nombre in enumerate(ETAPAS):
        if posicion < indice:
            clase = "completo"
        elif posicion == indice:
            clase = "actual"
        else:
            clase = ""

        pasos_html += f"""
        <div class="process-step {clase}">
            <div class="step-number">{posicion + 1}</div>
            <div>
                <strong>{nombre}</strong>
                <span>{_descripcion_paso(nombre)}</span>
            </div>
        </div>
        """

    return f"""
    <div class="bh-dashboard">
        <style>
            .bh-dashboard {{
                position: relative;
                display: grid;
                grid-template-columns: 260px minmax(0, 1fr);
                min-height: 690px;
                overflow: hidden;
                border-radius: 26px;
                border: 1px solid rgba(255, 255, 255, 0.12);
                background: #050711;
                box-shadow:
                    0 28px 80px rgba(0, 0, 0, 0.45);
                color: #f8fafc;
            }}

            .bh-sidebar {{
                position: relative;
                z-index: 5;
                padding: 25px 20px;
                background:
                    linear-gradient(
                        180deg,
                        rgba(7, 10, 22, 0.97),
                        rgba(8, 12, 25, 0.93)
                    );
                border-right:
                    1px solid rgba(255, 255, 255, 0.10);
                backdrop-filter: blur(14px);
            }}

            .bh-kicker {{
                color: #b68cff;
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.18em;
                text-transform: uppercase;
            }}

            .bh-heading {{
                margin: 7px 0 8px;
                font-size: 1.55rem;
                line-height: 1.12;
                letter-spacing: -0.025em;
            }}

            .bh-description {{
                color: #9ca7bf;
                font-size: 0.82rem;
                line-height: 1.55;
                margin-bottom: 24px;
            }}

            .sidebar-label {{
                margin: 19px 0 9px;
                color: #d7dcec;
                font-size: 0.72rem;
                font-weight: 750;
                letter-spacing: 0.09em;
                text-transform: uppercase;
            }}

            .stage-card,
            .metric-card {{
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 0.10);
                background: rgba(255, 255, 255, 0.045);
            }}

            .stage-card {{
                padding: 15px;
            }}

            .stage-name {{
                color: #c084fc;
                font-size: 1rem;
                font-weight: 800;
                margin-bottom: 5px;
            }}

            .stage-state {{
                color: #aeb8cf;
                font-size: 0.75rem;
                line-height: 1.45;
            }}

            .metric-card {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 13px;
                margin-bottom: 8px;
            }}

            .metric-label {{
                color: #aeb8cf;
                font-size: 0.73rem;
            }}

            .metric-value {{
                font-weight: 800;
                font-size: 0.91rem;
            }}

            .metric-cyan {{
                color: #3ddcff;
            }}

            .metric-purple {{
                color: #c084fc;
            }}

            .metric-green {{
                color: #4ade80;
            }}

            .bh-main {{
                position: relative;
                min-width: 0;
                background:
                    linear-gradient(
                        180deg,
                        rgba(1, 3, 10, 0.03),
                        rgba(1, 3, 10, 0.42)
                    ),
                    url("{imagen_uri}")
                    center center / cover no-repeat;
            }}

            .bh-main::before {{
                content: "";
                position: absolute;
                inset: 0;
                background:
                    linear-gradient(
                        90deg,
                        rgba(4, 7, 17, 0.55),
                        transparent 23%,
                        transparent 72%,
                        rgba(4, 7, 17, 0.35)
                    ),
                    linear-gradient(
                        180deg,
                        rgba(0, 0, 0, 0.08),
                        rgba(0, 0, 0, 0.52)
                    );
            }}

            .flow-left,
            .flow-right {{
                position: absolute;
                top: 46%;
                width: 32%;
                height: 3px;
                border-radius: 99px;
                filter: drop-shadow(0 0 9px currentColor);
            }}

            .flow-left {{
                left: 3%;
                color: #22d3ee;
                opacity: {intensidad_cian};
                background:
                    linear-gradient(
                        90deg,
                        transparent,
                        #22d3ee,
                        rgba(255, 255, 255, 0.95)
                    );
            }}

            .flow-right {{
                right: 3%;
                color: #c026d3;
                opacity: {intensidad_violeta};
                background:
                    linear-gradient(
                        90deg,
                        rgba(255, 255, 255, 0.95),
                        #c026d3,
                        transparent
                    );
            }}

            .packet {{
                position: absolute;
                top: calc(46% - 5px);
                width: 11px;
                height: 11px;
                border-radius: 50%;
            }}

            .packet-in {{
                left: 4%;
                opacity: {opacidad_entrada};
                background: #67e8f9;
                box-shadow:
                    0 0 12px #22d3ee,
                    0 0 25px #22d3ee;
                animation: travel-in 2.4s ease-in-out infinite;
            }}

            .packet-out {{
                left: 53%;
                opacity: {opacidad_salida};
                background: #e879f9;
                box-shadow:
                    0 0 12px #c026d3,
                    0 0 25px #c026d3;
                animation: travel-out 2.6s ease-in-out infinite;
            }}

            .scene-label {{
                position: absolute;
                z-index: 3;
                max-width: 230px;
                padding: 11px 13px;
                border-radius: 12px;
                background: rgba(4, 7, 17, 0.64);
                border: 1px solid rgba(255, 255, 255, 0.12);
                backdrop-filter: blur(8px);
            }}

            .scene-label strong {{
                display: block;
                margin-bottom: 4px;
                font-size: 0.86rem;
            }}

            .scene-label span {{
                color: #adb7cf;
                font-size: 0.72rem;
                line-height: 1.4;
            }}

            .label-input {{
                left: 5%;
                top: 8%;
            }}

            .label-input strong {{
                color: #4de8ff;
            }}

            .label-output {{
                right: 5%;
                top: 8%;
            }}

            .label-output strong {{
                color: #dc79ff;
            }}

            .process-panel {{
                position: absolute;
                z-index: 4;
                left: 4%;
                right: 4%;
                bottom: 25px;
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 8px;
                padding: 14px;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.12);
                background: rgba(4, 7, 18, 0.76);
                backdrop-filter: blur(12px);
            }}

            .process-step {{
                display: flex;
                align-items: center;
                gap: 8px;
                min-width: 0;
                padding: 9px;
                border-radius: 12px;
                color: #667088;
                transition: 0.3s ease;
            }}

            .process-step.actual {{
                color: white;
                background: rgba(168, 85, 247, 0.16);
                box-shadow:
                    inset 0 0 0 1px rgba(192, 132, 252, 0.45);
            }}

            .process-step.completo {{
                color: #74eeb0;
            }}

            .step-number {{
                display: grid;
                place-items: center;
                flex: 0 0 27px;
                height: 27px;
                border-radius: 50%;
                border: 1px solid currentColor;
                font-size: 0.72rem;
                font-weight: 800;
            }}

            .process-step strong {{
                display: block;
                font-size: 0.72rem;
            }}

            .process-step span {{
                display: block;
                margin-top: 2px;
                font-size: 0.61rem;
                line-height: 1.25;
                color: #8994ab;
            }}

            @keyframes travel-in {{
                0% {{
                    transform: translateX(0);
                    opacity: 0;
                }}
                15% {{
                    opacity: {opacidad_entrada};
                }}
                85% {{
                    opacity: {opacidad_entrada};
                }}
                100% {{
                    transform: translateX(320px);
                    opacity: 0;
                }}
            }}

            @keyframes travel-out {{
                0% {{
                    transform: translateX(0);
                    opacity: 0;
                }}
                15% {{
                    opacity: {opacidad_salida};
                }}
                85% {{
                    opacity: {opacidad_salida};
                }}
                100% {{
                    transform: translateX(310px);
                    opacity: 0;
                }}
            }}

            @media (max-width: 900px) {{
                .bh-dashboard {{
                    grid-template-columns: 1fr;
                }}

                .bh-sidebar {{
                    border-right: 0;
                    border-bottom:
                        1px solid rgba(255, 255, 255, 0.10);
                }}

                .bh-main {{
                    min-height: 570px;
                }}
            }}

            @media (max-width: 650px) {{
                .process-panel {{
                    grid-template-columns: repeat(2, 1fr);
                }}

                .scene-label {{
                    display: none;
                }}
            }}
        </style>

        <aside class="bh-sidebar">
            <div class="bh-kicker">
                Analogía cuántica
            </div>

            <div class="bh-heading">
                Agujero negro e información
            </div>

            <div class="bh-description">
                Modelo computacional inspirado en la paradoja
                de la información.
            </div>

            <div class="sidebar-label">
                Etapa actual
            </div>

            <div class="stage-card">
                <div class="stage-name">
                    {etapa}
                </div>

                <div class="stage-state">
                    {estado_sistema}
                </div>
            </div>

            <div class="sidebar-label">
                Métricas globales
            </div>

            <div class="metric-card">
                <span class="metric-label">
                    Entropía local
                </span>

                <span class="metric-value metric-purple">
                    {entropia:.4f}
                </span>
            </div>

            <div class="metric-card">
                <span class="metric-label">
                    Pureza local
                </span>

                <span class="metric-value metric-cyan">
                    {pureza:.4f}
                </span>
            </div>

            <div class="metric-card">
                <span class="metric-label">
                    Fidelidad ideal
                </span>

                <span class="metric-value metric-green">
                    {fidelidad * 100:.2f} %
                </span>
            </div>
        </aside>

        <main class="bh-main">
            <div class="flow-left"></div>
            <div class="flow-right"></div>

            <div class="packet packet-in"></div>
            <div class="packet packet-out"></div>

            <div class="scene-label label-input">
                <strong>Información entrante</strong>
                <span>
                    El estado preparado entra y comienza
                    a distribuirse en el sistema.
                </span>
            </div>

            <div class="scene-label label-output">
                <strong>Radiación conceptual</strong>
                <span>
                    La información deja de estar localizada,
                    pero permanece codificada globalmente.
                </span>
            </div>

            <div class="process-panel">
                {pasos_html}
            </div>
        </main>
    </div>
    """


def _descripcion_paso(nombre: str) -> str:
    descripciones = {
        "Entrada": "Estado inicial",
        "Distribución": "Entrelazamiento",
        "Radiación": "Información parcial",
        "Recuperación": "Circuito inverso",
    }

    return descripciones[nombre]


def render_modelo_agujero_negro(
    resultado: ResultadoMotor,
) -> None:
    """
    Renderiza el modelo visual interactivo.
    """

    st.subheader(
        "Modelo visual inspirado en un agujero negro"
    )

    st.write(
        """
        La visualización representa de forma didáctica cómo
        la información puede dejar de estar localizada sin
        desaparecer del sistema global.
        """
    )

    etapa = st.radio(
        "Etapa del proceso:",
        options=ETAPAS,
        horizontal=True,
        key="etapa_agujero_negro",
    )

    try:
        imagen_uri = cargar_imagen_base64(
            str(RUTA_IMAGEN)
        )

    except FileNotFoundError as error:
        st.error(str(error))
        st.caption(
            "Comprueba que la imagen esté en "
            "`assets/images/black_hole.png`."
        )
        return

    (
        entropia,
        pureza,
        estado_sistema,
        mensaje,
    ) = obtener_datos_etapa(
        resultado,
        etapa,
    )

    html = crear_html_visual(
        imagen_uri=imagen_uri,
        etapa=etapa,
        entropia=entropia,
        pureza=pureza,
        fidelidad=resultado.fidelidad,
        estado_sistema=estado_sistema,
    )

    st.html(html)

    st.info(escape(mensaje))

    st.caption(
        "Esta representación es una analogía computacional. "
        "No simula un agujero negro físico, relatividad general "
        "ni radiación de Hawking real."
    )