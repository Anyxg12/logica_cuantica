import base64
import math
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

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
    """
    ruta_imagen = Path(ruta)

    if not ruta_imagen.exists():
        return ""

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
        estado_sistema = "Información localizada (|Ψ_in⟩)"
        mensaje = (
            "El estado cuántico preparado mediante los ángulos θ y φ se encuentra "
            "concentrado en el primer cúbit antes del ingreso al horizonte."
        )

    elif etapa == "Distribución":
        estado = resultado.estado_distribuido
        estado_sistema = "Scrambling & Entrelazamiento"
        mensaje = (
            "Las transformaciones unitarias distribuyen y caotizan la información "
            "entre todos los cúbits mediante entrelazamiento cuántico profundo."
        )

    elif etapa == "Radiación":
        estado = resultado.estado_distribuido
        estado_sistema = "Radiación de Hawking (No localizada)"
        mensaje = (
            "La información deja de ser identificable en cúbits individuales, pero "
            "continúa codificada de forma no local en las correlaciones del sistema."
        )

    else:
        estado = resultado.estado_recuperado
        estado_sistema = "Reconstrucción Coherente (|Ψ_out⟩)"
        mensaje = (
            "La transformación univalente inversa descodifica la información, "
            "recuperando el estado cuántico original con alta fidelidad."
        )

    metricas = calcular_metricas_sistema(estado)

    entropia_promedio = sum(m.entropia for m in metricas) / len(metricas)
    pureza_promedio = sum(m.pureza for m in metricas) / len(metricas)

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
    theta: float,
    phi: float,
    estado_sistema: str,
) -> str:
    """
    Construye la simulación 3D WebGL hiper-fotorrealista definitiva con Three.js
    optimizada con retardo seguro CDN para compatibilidad 100% con Streamlit Cloud.
    """
    indice_etapa = ETAPAS.index(etapa)

    pasos_html = ""
    for idx, nombre in enumerate(ETAPAS):
        if idx < indice_etapa:
            clase = "completo"
            icono = "✓"
        elif idx == indice_etapa:
            clase = "actual"
            icono = str(idx + 1)
        else:
            clase = ""
            icono = str(idx + 1)

        pasos_html += f"""
        <div class="hud-step {clase}">
            <div class="hud-step-badge">{icono}</div>
            <div class="hud-step-info">
                <span class="hud-step-title">{nombre}</span>
                <span class="hud-step-sub">{_descripcion_paso(nombre)}</span>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="utf-8"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            user-select: none;
        }}

        body {{
            background: #010207;
            color: #f8fafc;
            overflow: hidden;
        }}

        .bh-wrapper {{
            position: relative;
            width: 100%;
            height: 770px;
            border-radius: 28px;
            overflow: hidden;
            border: 1px solid rgba(168, 85, 247, 0.35);
            background: radial-gradient(circle at 50% 50%, #0c0f26 0%, #010207 100%);
            box-shadow: 0 35px 120px rgba(0,0,0,0.95), inset 0 0 90px rgba(168, 85, 247, 0.15);
        }}

        #webglCanvas {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }}

        .hud-overlay {{
            position: absolute;
            inset: 0;
            z-index: 10;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 24px 28px;
        }}

        .hud-overlay * {{
            pointer-events: auto;
        }}

        .hud-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(8, 12, 28, 0.78);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 14px 24px;
            box-shadow: 0 12px 45px rgba(0, 0, 0, 0.65);
        }}

        .hud-title-box {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .hud-pulse-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #38bdf8;
            box-shadow: 0 0 14px #38bdf8, 0 0 28px #38bdf8;
            animation: pulseGlow 1.8s infinite ease-in-out;
        }}

        @keyframes pulseGlow {{
            0%, 100% {{ transform: scale(1); opacity: 0.85; }}
            50% {{ transform: scale(1.45); opacity: 1; }}
        }}

        .hud-main-title {{
            font-size: 1.15rem;
            font-weight: 850;
            letter-spacing: -0.025em;
            background: linear-gradient(90deg, #ffffff, #c084fc 45%, #38bdf8 85%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hud-subtitle {{
            font-size: 0.76rem;
            color: #94a3b8;
            margin-top: 2px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }}

        .hud-metrics-strip {{
            display: flex;
            gap: 12px;
        }}

        .hud-metric-pill {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 6px 14px;
            white-space: nowrap;
        }}

        .hud-metric-pill .label {{
            font-size: 0.64rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            white-space: nowrap;
        }}

        .hud-metric-pill .val {{
            font-size: 0.92rem;
            font-weight: 800;
            font-family: monospace;
            white-space: nowrap;
        }}

        .val-cyan {{ color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); }}
        .val-purple {{ color: #c084fc; text-shadow: 0 0 10px rgba(192, 132, 252, 0.5); }}
        .val-green {{ color: #4ade80; text-shadow: 0 0 10px rgba(74, 222, 128, 0.5); }}

        .hud-center-labels {{
            position: absolute;
            top: 52%;
            left: 0;
            width: 100%;
            transform: translateY(-50%);
            display: flex;
            justify-content: space-between;
            padding: 0 30px;
            pointer-events: none;
        }}

        .hud-side-card {{
            background: rgba(6, 10, 26, 0.78);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.13);
            border-radius: 18px;
            padding: 16px 20px;
            max-width: 235px;
            box-shadow: 0 16px 40px rgba(0,0,0,0.65);
        }}

        .hud-side-card strong {{
            display: block;
            font-size: 0.85rem;
            margin-bottom: 5px;
            letter-spacing: 0.04em;
        }}

        .hud-side-card p {{
            font-size: 0.73rem;
            color: #a1a1aa;
            line-height: 1.45;
        }}

        .card-in strong {{ color: #38bdf8; }}
        .card-out strong {{ color: #e879f9; }}

        .hud-footer {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            background: rgba(6, 10, 26, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 12px;
            box-shadow: 0 16px 50px rgba(0, 0, 0, 0.7);
        }}

        .hud-step {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .hud-step-badge {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            font-size: 0.78rem;
            font-weight: 800;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #94a3b8;
        }}

        .hud-step-info {{
            display: flex;
            flex-direction: column;
        }}

        .hud-step-title {{
            font-size: 0.82rem;
            font-weight: 750;
            color: #cbd5e1;
        }}

        .hud-step-sub {{
            font-size: 0.66rem;
            color: #64748b;
            margin-top: 1px;
        }}

        .hud-step.actual {{
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.28), rgba(56, 189, 248, 0.18));
            border-color: rgba(192, 132, 252, 0.6);
            box-shadow: 0 0 24px rgba(168, 85, 247, 0.3), inset 0 0 16px rgba(192, 132, 252, 0.2);
        }}

        .hud-step.actual .hud-step-badge {{
            background: #a855f7;
            color: white;
            border-color: #c084fc;
            box-shadow: 0 0 14px #a855f7;
        }}

        .hud-step.actual .hud-step-title {{
            color: #ffffff;
        }}

        .hud-step.actual .hud-step-sub {{
            color: #e9d5ff;
        }}

        .hud-step.completo {{
            border-color: rgba(74, 222, 128, 0.35);
            background: rgba(74, 222, 128, 0.06);
        }}

        .hud-step.completo .hud-step-badge {{
            background: rgba(74, 222, 128, 0.22);
            color: #4ade80;
            border-color: #4ade80;
        }}

        @media (max-width: 800px) {{
            .hud-header {{ flex-direction: column; gap: 12px; align-items: flex-start; }}
            .hud-footer {{ grid-template-columns: repeat(2, 1fr); }}
            .hud-side-card {{ display: none; }}
        }}
    </style>
    </head>
    <body>

    <div class="bh-wrapper">
        <canvas id="webglCanvas"></canvas>

        <div class="hud-overlay">
            <div class="hud-header">
                <div class="hud-title-box">
                    <div class="hud-pulse-dot"></div>
                    <div>
                        <div class="hud-main-title">MODELO DE PRESERVACIÓN DE INFORMACIÓN CUÁNTICA EN EL HORIZONTE DE SUCESOS</div>
                        <div class="hud-subtitle">Etapa activa: {etapa} &bull; {estado_sistema}</div>
                    </div>
                </div>

                <div class="hud-metrics-strip">
                    <div class="hud-metric-pill">
                        <span class="label">Ángulos θ, φ</span>
                        <span class="val val-cyan">{theta:.0f}°, {phi:.0f}°</span>
                    </div>
                    <div class="hud-metric-pill">
                        <span class="label">Entropía</span>
                        <span class="val val-purple">{entropia:.4f}</span>
                    </div>
                    <div class="hud-metric-pill">
                        <span class="label">Pureza</span>
                        <span class="val val-cyan">{pureza:.4f}</span>
                    </div>
                    <div class="hud-metric-pill">
                        <span class="label">Fidelidad</span>
                        <span class="val val-green">{fidelidad * 100:.2f}%</span>
                    </div>
                </div>
            </div>

            <div class="hud-center-labels">
                <div class="hud-side-card card-in">
                    <strong>Estado Preparado (|Ψ_in⟩)</strong>
                    <p>Haz fotónico localizado ingresando al horizonte gravitatorio.</p>
                </div>
                <div class="hud-side-card card-out">
                    <strong>Reconstrucción (|Ψ_out⟩)</strong>
                    <p>Radiación de Hawking descodificada mediante circuito inverso.</p>
                </div>
            </div>

            <div class="hud-footer">
                {pasos_html}
            </div>
        </div>
    </div>

    <script>
    function createSoftParticleTexture() {{
        const canvas = document.createElement('canvas');
        canvas.width = 64;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');
        const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
        grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.18, 'rgba(255, 255, 255, 0.9)');
        grad.addColorStop(0.45, 'rgba(255, 255, 255, 0.3)');
        grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(32, 32, 32, 0, Math.PI * 2);
        ctx.fill();
        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        return texture;
    }}

    function createHighGlowQuantumTexture() {{
        const canvas = document.createElement('canvas');
        canvas.width = 128;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');
        const grad = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
        grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.15, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.35, 'rgba(0, 243, 255, 0.95)');
        grad.addColorStop(0.7, 'rgba(168, 85, 247, 0.45)');
        grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(64, 64, 64, 0, Math.PI * 2);
        ctx.fill();
        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        return texture;
    }}

    function initSim() {{
        if (typeof THREE === 'undefined') {{
            setTimeout(initSim, 50);
            return;
        }}

        const ETAPA_ACTUAL = "{etapa}";
        const THETA = {theta};
        const PHI = {phi};

        const canvas = document.getElementById('webglCanvas');
        const wrapper = document.querySelector('.bh-wrapper');

        if (!canvas || !wrapper) return;

        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x010207, 0.0035);

        const camera = new THREE.PerspectiveCamera(45, wrapper.clientWidth / wrapper.clientHeight, 0.1, 1000);
        camera.position.set(0, 24, 98);

        const renderer = new THREE.WebGLRenderer({{ canvas: canvas, antialias: true, alpha: true }});
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(wrapper.clientWidth, wrapper.clientHeight);

        const particleTexture = createSoftParticleTexture();
        const quantumGlowTexture = createHighGlowQuantumTexture();

        // 1. Singularidad Central
        const singularityGeo = new THREE.SphereGeometry(9.5, 64, 64);
        const singularityMat = new THREE.MeshBasicMaterial({{ color: 0x000000 }});
        const singularity = new THREE.Mesh(singularityGeo, singularityMat);
        scene.add(singularity);

        // Atmósferas Fluorescentes de Borde
        const rimGeo1 = new THREE.SphereGeometry(10.0, 64, 64);
        const rimMat1 = new THREE.MeshBasicMaterial({{
            color: 0xc084fc,
            transparent: true,
            opacity: 0.5,
            side: THREE.BackSide,
            blending: THREE.AdditiveBlending
        }});
        scene.add(new THREE.Mesh(rimGeo1, rimMat1));

        const rimGeo2 = new THREE.SphereGeometry(10.7, 64, 64);
        const rimMat2 = new THREE.MeshBasicMaterial({{
            color: 0x00f3ff,
            transparent: true,
            opacity: 0.35,
            side: THREE.BackSide,
            blending: THREE.AdditiveBlending
        }});
        scene.add(new THREE.Mesh(rimGeo2, rimMat2));

        // 2. Anillos Fotónicos ($1.5 R_s$ y $1.8 R_s$)
        const photonRingGeo1 = new THREE.RingGeometry(9.8, 11.6, 64);
        const photonRingMat1 = new THREE.MeshBasicMaterial({{
            color: 0x00f3ff,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.98,
            blending: THREE.AdditiveBlending
        }});
        const photonRing1 = new THREE.Mesh(photonRingGeo1, photonRingMat1);
        photonRing1.rotation.x = Math.PI / 2;
        scene.add(photonRing1);

        const photonRingGeo2 = new THREE.RingGeometry(11.7, 13.2, 64);
        const photonRingMat2 = new THREE.MeshBasicMaterial({{
            color: 0xc084fc,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.78,
            blending: THREE.AdditiveBlending
        }});
        const photonRing2 = new THREE.Mesh(photonRingGeo2, photonRingMat2);
        photonRing2.rotation.x = Math.PI / 2;
        scene.add(photonRing2);

        // 3. Disco de Acreción Volumétrico (20,000 Partículas con Cinesis Kepleriana)
        const diskCount = 20000;
        const diskGeo = new THREE.BufferGeometry();
        const diskPos = new Float32Array(diskCount * 3);
        const diskColors = new Float32Array(diskCount * 3);
        const diskVelocities = [];

        for (let i = 0; i < diskCount; i++) {{
            const r = 10.5 + Math.random() * 52.0;
            const thetaAngle = Math.random() * Math.PI * 2;
            const yOffset = (Math.random() - 0.5) * (2.0 * (r / 52.0));

            diskPos[i * 3] = r * Math.cos(thetaAngle);
            diskPos[i * 3 + 1] = yOffset;
            diskPos[i * 3 + 2] = r * Math.sin(thetaAngle);

            const keplerSpeed = (0.36 / Math.sqrt(r)) * (1 + (PHI / 360) * 0.4);
            diskVelocities.push({{ r: r, angle: thetaAngle, speed: keplerSpeed }});

            const normR = (r - 10.5) / 52.0;
            const color = new THREE.Color();
            if (normR < 0.22) {{
                color.setHSL(0.53 - normR * 0.08, 1.0, 0.88);
            }} else if (normR < 0.62) {{
                color.setHSL(0.72 + normR * 0.06, 0.95, 0.68);
            }} else {{
                color.setHSL(0.78, 0.9, 0.45);
            }}
            diskColors[i * 3] = color.r;
            diskColors[i * 3 + 1] = color.g;
            diskColors[i * 3 + 2] = color.b;
        }}

        diskGeo.setAttribute('position', new THREE.BufferAttribute(diskPos, 3));
        diskGeo.setAttribute('color', new THREE.BufferAttribute(diskColors, 3));

        const diskMat = new THREE.PointsMaterial({{
            size: 1.6,
            map: particleTexture,
            vertexColors: true,
            transparent: true,
            opacity: 0.88,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        }});

        const accretionDisc = new THREE.Points(diskGeo, diskMat);
        scene.add(accretionDisc);

        // 4. Arcos de Lente Gravitacional Polar (6,000 Partículas)
        const lensCount = 6000;
        const lensGeo = new THREE.BufferGeometry();
        const lensPos = new Float32Array(lensCount * 3);
        const lensColors = new Float32Array(lensCount * 3);
        const lensVelocities = [];

        for (let i = 0; i < lensCount; i++) {{
            const isTop = Math.random() > 0.5;
            const r = 10.2 + Math.random() * 40.0;
            const angle = Math.random() * Math.PI * 2;
            const arcY = (isTop ? 1 : -1) * (Math.sin(angle * 0.5) * (15 + (r / 40) * 18) + Math.random() * 3.0);

            lensPos[i * 3] = r * Math.cos(angle);
            lensPos[i * 3 + 1] = arcY;
            lensPos[i * 3 + 2] = r * Math.sin(angle) * 0.38;

            const keplerSpeed = 0.28 / Math.sqrt(r);
            lensVelocities.push({{ r: r, angle: angle, speed: keplerSpeed }});

            const color = isTop ? new THREE.Color(0x00f3ff) : new THREE.Color(0xc084fc);
            lensColors[i * 3] = color.r;
            lensColors[i * 3 + 1] = color.g;
            lensColors[i * 3 + 2] = color.b;
        }}

        lensGeo.setAttribute('position', new THREE.BufferAttribute(lensPos, 3));
        lensGeo.setAttribute('color', new THREE.BufferAttribute(lensColors, 3));

        const lensMat = new THREE.PointsMaterial({{
            size: 1.5,
            map: particleTexture,
            vertexColors: true,
            transparent: true,
            opacity: 0.82,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        }});

        const lensMesh = new THREE.Points(lensGeo, lensMat);
        scene.add(lensMesh);

        // 5. Chorros Polares Relativistas (1,500 Partículas)
        const jetCount = 1500;
        const jetGeo = new THREE.BufferGeometry();
        const jetPos = new Float32Array(jetCount * 3);
        const jetColors = new Float32Array(jetCount * 3);
        const jetData = [];

        for (let i = 0; i < jetCount; i++) {{
            const isNorth = Math.random() > 0.5;
            const y = (isNorth ? 1 : -1) * (9.5 + Math.random() * 38.0);
            const spread = 0.8 + (Math.abs(y) / 38.0) * 4.5;
            const angle = Math.random() * Math.PI * 2;
            const x = Math.cos(angle) * Math.random() * spread;
            const z = Math.sin(angle) * Math.random() * spread;

            jetPos[i * 3] = x;
            jetPos[i * 3 + 1] = y;
            jetPos[i * 3 + 2] = z;

            jetData.push({{ isNorth: isNorth, speed: 0.38 + Math.random() * 0.48, spread: spread }});

            const color = isNorth ? new THREE.Color(0x00f3ff) : new THREE.Color(0xe879f9);
            jetColors[i * 3] = color.r;
            jetColors[i * 3 + 1] = color.g;
            jetColors[i * 3 + 2] = color.b;
        }}

        jetGeo.setAttribute('position', new THREE.BufferAttribute(jetPos, 3));
        jetGeo.setAttribute('color', new THREE.BufferAttribute(jetColors, 3));

        const jetMat = new THREE.PointsMaterial({{
            size: 1.8,
            map: particleTexture,
            vertexColors: true,
            transparent: true,
            opacity: 0.75,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        }});

        const jetMesh = new THREE.Points(jetGeo, jetMat);
        scene.add(jetMesh);

        // 6. Haz Fotónico Cuántico de Alta Visibilidad (800 Orbes de Gran Tamaño)
        const qCount = 800;
        const qGeo = new THREE.BufferGeometry();
        const qPos = new Float32Array(qCount * 3);
        const qColors = new Float32Array(qCount * 3);
        const qData = [];

        for (let i = 0; i < qCount; i++) {{
            const p = {{}};
            if (ETAPA_ACTUAL === "Entrada") {{
                p.x = -98 + Math.random() * 48;
                p.y = (Math.random() - 0.5) * 22;
                p.z = (Math.random() - 0.5) * 22;
                p.vx = 0.7 + Math.random() * 0.85;
                p.vy = (Math.random() - 0.5) * 0.12;
                p.vz = (Math.random() - 0.5) * 0.12;
                p.color = new THREE.Color(0xffffff);
            }} else if (ETAPA_ACTUAL === "Distribución") {{
                p.r = 10.5 + Math.random() * 40;
                p.angle = Math.random() * Math.PI * 2;
                p.speed = 0.03 + Math.random() * 0.045;
                p.x = p.r * Math.cos(p.angle);
                p.y = (Math.random() - 0.5) * 5.0;
                p.z = p.r * Math.sin(p.angle);
                p.color = Math.random() > 0.5 ? new THREE.Color(0xffffff) : new THREE.Color(0x00f3ff);
            }} else if (ETAPA_ACTUAL === "Radiación") {{
                p.x = (Math.random() - 0.5) * 6;
                p.y = (Math.random() - 0.5) * 6;
                p.z = (Math.random() - 0.5) * 6;
                const dir = new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize();
                p.vx = dir.x * (0.6 + Math.random() * 0.9);
                p.vy = dir.y * (0.6 + Math.random() * 0.9);
                p.vz = dir.z * (0.6 + Math.random() * 0.9);
                p.color = new THREE.Color(0xffaefc);
            }} else {{
                p.x = (Math.random() - 0.5) * 4;
                p.y = (Math.random() - 0.5) * 4;
                p.z = (Math.random() - 0.5) * 4;
                p.vx = 0.95 + Math.random() * 1.25;
                p.vy = (Math.random() - 0.5) * 0.1;
                p.vz = (Math.random() - 0.5) * 0.1;
                p.color = new THREE.Color(0x5ff59e);
            }}

            qPos[i * 3] = p.x;
            qPos[i * 3 + 1] = p.y;
            qPos[i * 3 + 2] = p.z;

            qColors[i * 3] = p.color.r;
            qColors[i * 3 + 1] = p.color.g;
            qColors[i * 3 + 2] = p.color.b;

            qData.push(p);
        }}

        qGeo.setAttribute('position', new THREE.BufferAttribute(qPos, 3));
        qGeo.setAttribute('color', new THREE.BufferAttribute(qColors, 3));

        const qMat = new THREE.PointsMaterial({{
            size: 4.8,
            map: quantumGlowTexture,
            vertexColors: true,
            transparent: true,
            opacity: 1.0,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        }});

        const qParticlesMesh = new THREE.Points(qGeo, qMat);
        scene.add(qParticlesMesh);

        // 7. Estrellas Espaciales (2,000 Estrellas)
        const starCount = 2000;
        const starGeo = new THREE.BufferGeometry();
        const starPos = new Float32Array(starCount * 3);
        for (let i = 0; i < starCount; i++) {{
            starPos[i * 3] = (Math.random() - 0.5) * 750;
            starPos[i * 3 + 1] = (Math.random() - 0.5) * 750;
            starPos[i * 3 + 2] = (Math.random() - 0.5) * 750;
        }}
        starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
        const starMat = new THREE.PointsMaterial({{ size: 0.85, map: particleTexture, color: 0xe0e7ff, transparent: true, opacity: 0.72, blending: THREE.AdditiveBlending, depthWrite: false }});
        scene.add(new THREE.Points(starGeo, starMat));

        // Órbita de Cámara Suave
        let mouseX = 0, mouseY = 0;
        let targetMouseX = 0, targetMouseY = 0;

        document.addEventListener('mousemove', (e) => {{
            const rect = wrapper.getBoundingClientRect();
            targetMouseX = ((e.clientX - rect.left) / wrapper.clientWidth - 0.5) * 2;
            targetMouseY = ((e.clientY - rect.top) / wrapper.clientHeight - 0.5) * 2;
        }});

        function animate() {{
            requestAnimationFrame(animate);

            mouseX += (targetMouseX - mouseX) * 0.05;
            mouseY += (targetMouseY - mouseY) * 0.05;

            camera.position.x = mouseX * 32;
            camera.position.y = 24 + (-mouseY * 26);
            camera.lookAt(0, 0, 0);

            // Cinesis Kepleriana del Disco
            const positions = accretionDisc.geometry.attributes.position.array;
            for (let i = 0; i < diskCount; i++) {{
                const p = diskVelocities[i];
                p.angle += p.speed;
                positions[i * 3] = p.r * Math.cos(p.angle);
                positions[i * 3 + 2] = p.r * Math.sin(p.angle);
            }}
            accretionDisc.geometry.attributes.position.needsUpdate = true;

            // Arcos de Lente Gravitacional
            const lPositions = lensMesh.geometry.attributes.position.array;
            for (let i = 0; i < lensCount; i++) {{
                const p = lensVelocities[i];
                p.angle += p.speed;
                lPositions[i * 3] = p.r * Math.cos(p.angle);
                lPositions[i * 3 + 2] = p.r * Math.sin(p.angle) * 0.38;
            }}
            lensMesh.geometry.attributes.position.needsUpdate = true;

            // Chorros Polares
            const jPositions = jetMesh.geometry.attributes.position.array;
            for (let i = 0; i < jetCount; i++) {{
                const p = jetData[i];
                let y = jPositions[i * 3 + 1];
                if (p.isNorth) {{
                    y += p.speed;
                    if (y > 45) y = 9.5;
                }} else {{
                    y -= p.speed;
                    if (y < -45) y = -9.5;
                }}
                jPositions[i * 3 + 1] = y;
            }}
            jetMesh.geometry.attributes.position.needsUpdate = true;

            // Flujo Fotónico Cuántico de Alta Visibilidad
            const qPositions = qParticlesMesh.geometry.attributes.position.array;
            for (let i = 0; i < qCount; i++) {{
                const p = qData[i];
                if (ETAPA_ACTUAL === "Entrada") {{
                    p.x += p.vx;
                    p.y += (0 - p.y) * 0.03;
                    p.z += (0 - p.z) * 0.03;
                    if (p.x > 0) {{
                        p.x = -98;
                        p.y = (Math.random() - 0.5) * 22;
                        p.z = (Math.random() - 0.5) * 22;
                    }}
                }} else if (ETAPA_ACTUAL === "Distribución") {{
                    p.angle += p.speed;
                    p.x = p.r * Math.cos(p.angle);
                    p.z = p.r * Math.sin(p.angle);
                }} else if (ETAPA_ACTUAL === "Radiación") {{
                    p.x += p.vx;
                    p.y += p.vy;
                    p.z += p.vz;
                    if (Math.hypot(p.x, p.y, p.z) > 98) {{
                        p.x = (Math.random() - 0.5) * 6;
                        p.y = (Math.random() - 0.5) * 6;
                        p.z = (Math.random() - 0.5) * 6;
                    }}
                }} else {{
                    p.x += p.vx;
                    p.y += (0 - p.y) * 0.03;
                    p.z += (0 - p.z) * 0.03;
                    if (p.x > 98) {{
                        p.x = 0;
                        p.y = (Math.random() - 0.5) * 4;
                        p.z = (Math.random() - 0.5) * 4;
                    }}
                }}

                qPositions[i * 3] = p.x;
                qPositions[i * 3 + 1] = p.y;
                qPositions[i * 3 + 2] = p.z;
            }}
            qParticlesMesh.geometry.attributes.position.needsUpdate = true;

            renderer.render(scene, camera);
        }}

        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = wrapper.clientWidth / wrapper.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(wrapper.clientWidth, wrapper.clientHeight);
        }});
    }}

    if (document.readyState === 'complete') {{
        initSim();
    }} else {{
        window.addEventListener('load', initSim);
    }}
    </script>
    </body>
    </html>
    """


def _descripcion_paso(nombre: str) -> str:
    descripciones = {
        "Entrada": "Estado inicial local |Ψ_in⟩",
        "Distribución": "Entrelazamiento univalente",
        "Radiación": "Scrambling de Hawking",
        "Recuperación": "Circuito inverso |Ψ_out⟩",
    }
    return descripciones[nombre]


def render_modelo_agujero_negro(
    resultado: ResultadoMotor,
) -> None:
    """
    Renderiza la simulación 3D WebGL del agujero negro.
    """
    st.subheader("🌌 Simulación de Preservación de Información Cuántica en el Horizonte de Sucesos")

    st.write(
        """
        Esta simulación tridimensional en **WebGL (Three.js)** recrea la atracción gravitacional
        sobre el estado cuántico $|Ψ\\rangle$. Observa cómo la información ingresa al horizonte de sucesos, se dispersa en
        órbitas de entrelazamiento y es reconducida mediante la transformación univalente inversa.
        """
    )

    etapa = st.radio(
        "Selecciona la etapa del proceso cuántico:",
        options=ETAPAS,
        horizontal=True,
        key="etapa_agujero_negro",
    )

    imagen_uri = cargar_imagen_base64(str(RUTA_IMAGEN))

    entropia, pureza, estado_sistema, mensaje = obtener_datos_etapa(
        resultado,
        etapa,
    )

    html = crear_html_visual(
        imagen_uri=imagen_uri,
        etapa=etapa,
        entropia=entropia,
        pureza=pureza,
        fidelidad=resultado.fidelidad,
        theta=resultado.theta_grados,
        phi=resultado.phi_grados,
        estado_sistema=estado_sistema,
    )

    components.html(html, height=790)

    st.info(escape(mensaje))

    st.caption(
        "💡 *Nota de simulación*: El entorno tridimensional renderiza la curvatura lumínica en la esfera de fotones "
        "y el disco de acreción volumétrico con partículas de información interactivas."
    )