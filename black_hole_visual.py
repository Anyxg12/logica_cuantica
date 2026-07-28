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
    Construye la experiencia visual interactiva en HTML5 Canvas 2D + Sci-Fi HUD Avanzado.
    """
    indice_etapa = ETAPAS.index(etapa)

    # Cálculo de amplitudes del estado inicial para el HUD
    rad_theta = math.radians(theta)
    prob_0 = math.cos(rad_theta / 2.0) ** 2
    prob_1 = math.sin(rad_theta / 2.0) ** 2

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
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            user-select: none;
        }}

        body {{
            background: #02040a;
            color: #f8fafc;
            overflow: hidden;
        }}

        .bh-wrapper {{
            position: relative;
            width: 100%;
            height: 720px;
            border-radius: 26px;
            overflow: hidden;
            border: 1px solid rgba(168, 85, 247, 0.3);
            background: radial-gradient(circle at 50% 50%, #0b0f24 0%, #02040a 100%);
            box-shadow: 0 30px 100px rgba(0,0,0,0.85), inset 0 0 70px rgba(168, 85, 247, 0.1);
        }}

        /* Canvas visualizer */
        #bhCanvas {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }}

        /* Texture overlay */
        .bg-texture {{
            position: absolute;
            inset: 0;
            z-index: 0;
            background-image: url("{imagen_uri}");
            background-position: center;
            background-size: cover;
            opacity: 0.16;
            filter: blur(6px) contrast(1.3);
            mix-blend-mode: screen;
            pointer-events: none;
        }}

        /* HUD Main Container */
        .hud-overlay {{
            position: absolute;
            inset: 0;
            z-index: 10;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 22px 26px;
        }}

        .hud-overlay * {{
            pointer-events: auto;
        }}

        /* Header HUD Bar */
        .hud-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(6, 10, 24, 0.72);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 18px;
            padding: 14px 22px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
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
            background: #22d3ee;
            box-shadow: 0 0 14px #22d3ee, 0 0 28px #22d3ee;
            animation: pulseGlow 2s infinite ease-in-out;
        }}

        @keyframes pulseGlow {{
            0%, 100% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.4); opacity: 1; }}
        }}

        .hud-main-title {{
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, #ffffff, #c084fc 45%, #38bdf8);
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
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 6px 14px;
        }}

        .hud-metric-pill .label {{
            font-size: 0.64rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .hud-metric-pill .val {{
            font-size: 0.95rem;
            font-weight: 800;
            font-family: monospace;
        }}

        .val-purple {{ color: #c084fc; text-shadow: 0 0 10px rgba(192, 132, 252, 0.5); }}
        .val-cyan {{ color: #38bdf8; text-shadow: 0 0 10px rgba(56, 189, 248, 0.5); }}
        .val-green {{ color: #4ade80; text-shadow: 0 0 10px rgba(74, 222, 128, 0.5); }}
        .val-amber {{ color: #fbbf24; text-shadow: 0 0 10px rgba(251, 191, 36, 0.5); }}

        /* HUD Hologram Side Panels */
        .hud-center-labels {{
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            transform: translateY(-50%);
            display: flex;
            justify-content: space-between;
            padding: 0 28px;
            pointer-events: none;
        }}

        .hud-side-card {{
            background: rgba(5, 8, 22, 0.76);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 16px 20px;
            max-width: 230px;
            box-shadow: 0 14px 35px rgba(0,0,0,0.6);
            transition: all 0.3s ease;
        }}

        .hud-side-card strong {{
            display: block;
            font-size: 0.84rem;
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

        .state-vector-pill {{
            margin-top: 8px;
            padding: 4px 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            font-size: 0.68rem;
            font-family: monospace;
            color: #e2e8f0;
        }}

        /* Bottom Step Bar Navigation */
        .hud-footer {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            background: rgba(5, 8, 22, 0.78);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 20px;
            padding: 12px;
            box-shadow: 0 14px 45px rgba(0, 0, 0, 0.65);
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
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(56, 189, 248, 0.14));
            border-color: rgba(192, 132, 252, 0.55);
            box-shadow: 0 0 22px rgba(168, 85, 247, 0.28), inset 0 0 14px rgba(192, 132, 252, 0.22);
        }}

        .hud-step.actual .hud-step-badge {{
            background: #a855f7;
            color: white;
            border-color: #c084fc;
            box-shadow: 0 0 12px #a855f7;
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
        <div class="bg-texture"></div>
        <canvas id="bhCanvas"></canvas>

        <div class="hud-overlay">
            <div class="hud-header">
                <div class="hud-title-box">
                    <div class="hud-pulse-dot"></div>
                    <div>
                        <div class="hud-main-title">MODELO DE PARADOJA &mdash; AGUJERO NEGRO CUÁNTICO</div>
                        <div class="hud-subtitle">Etapa activa: {etapa} &bull; {estado_sistema}</div>
                    </div>
                </div>

                <div class="hud-metrics-strip">
                    <div class="hud-metric-pill">
                        <span class="label">Ángulos θ, φ</span>
                        <span class="val val-amber">{theta:.0f}°, {phi:.0f}°</span>
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
                    <div class="state-vector-pill">P(|0⟩): {prob_0*100:.1f}% | P(|1⟩): {prob_1*100:.1f}%</div>
                </div>
                <div class="hud-side-card card-out">
                    <strong>Reconstrucción (|Ψ_out⟩)</strong>
                    <p>Radiación de Hawking descodificada mediante circuito inverso.</p>
                    <div class="state-vector-pill">Coherencia: {fidelidad*100:.1f}%</div>
                </div>
            </div>

            <div class="hud-footer">
                {pasos_html}
            </div>
        </div>
    </div>

    <script>
    (function() {{
        const canvas = document.getElementById('bhCanvas');
        const ctx = canvas.getContext('2d');

        const ETAPA_ACTUAL = "{etapa}";
        const ENTROPIA = {entropia};
        const PUREZA = {pureza};
        const FIDELIDAD = {fidelidad};
        const THETA = {theta};
        const PHI = {phi};

        let width, height, cx, cy;
        let particles = [];
        let accretionParticles = [];
        let mouseX = 0, mouseY = 0;
        let targetMouseX = 0, targetMouseY = 0;
        let time = 0;

        function resize() {{
            const dpr = window.devicePixelRatio || 1;
            const rect = canvas.getBoundingClientRect();
            width = rect.width;
            height = rect.height;
            canvas.width = width * dpr;
            canvas.height = height * dpr;
            ctx.scale(dpr, dpr);
            cx = width / 2;
            cy = height / 2;
        }}

        window.addEventListener('resize', resize);
        resize();

        document.addEventListener('mousemove', (e) => {{
            const rect = canvas.getBoundingClientRect();
            targetMouseX = (e.clientX - rect.left - cx) * 0.08;
            targetMouseY = (e.clientY - rect.top - cy) * 0.08;
        }});

        // Accretion disk particles
        const NUM_ACCRETION = 380;
        for (let i = 0; i < NUM_ACCRETION; i++) {{
            accretionParticles.push({{
                r: 70 + Math.random() * 160,
                angle: Math.random() * Math.PI * 2,
                speed: (0.006 + Math.random() * 0.016) * (1 + (PHI / 360) * 0.5),
                size: 0.8 + Math.random() * 2.4,
                hue: Math.random() > 0.35 ? (260 + (THETA / 180) * 50) : (180 + Math.random() * 40),
                opacity: 0.25 + Math.random() * 0.75,
                tiltY: 0.28 + Math.random() * 0.12
            }});
        }}

        // Quantum Information Flow Particles
        const NUM_QUANTUM = 200;
        for (let i = 0; i < NUM_QUANTUM; i++) {{
            resetQuantumParticle(i);
        }}

        function resetQuantumParticle(idx) {{
            const p = particles[idx] || {{}};
            p.t = Math.random();
            p.speed = 0.003 + Math.random() * 0.007;

            if (ETAPA_ACTUAL === "Entrada") {{
                p.x = Math.random() * (width * 0.28);
                p.y = cy + (Math.random() - 0.5) * (80 + (THETA / 180) * 60);
                p.targetX = cx;
                p.targetY = cy;
                p.color = Math.random() > 0.3 ? "#38bdf8" : "#22d3ee";
                p.glow = "#00f3ff";
                p.size = 2 + Math.random() * 3.2;
            }} else if (ETAPA_ACTUAL === "Distribución") {{
                p.angle = Math.random() * Math.PI * 2;
                p.r = 55 + Math.random() * 120;
                p.speed = 0.018 + Math.random() * 0.035;
                p.color = Math.random() > 0.5 ? "#c084fc" : "#38bdf8";
                p.glow = "#a855f7";
                p.size = 1.8 + Math.random() * 3.2;
            }} else if (ETAPA_ACTUAL === "Radiación") {{
                p.x = cx + (Math.random() - 0.5) * 45;
                p.y = cy + (Math.random() - 0.5) * 45;
                const dir = Math.random() * Math.PI * 2;
                p.vx = Math.cos(dir) * (1.3 + Math.random() * 2.8);
                p.vy = Math.sin(dir) * (1.3 + Math.random() * 2.8);
                p.color = "#e879f9";
                p.glow = "#d946ef";
                p.size = 2 + Math.random() * 2.8;
            }} else {{ // Recuperación
                p.x = cx + (Math.random() - 0.5) * 20;
                p.y = cy + (Math.random() - 0.5) * 20;
                p.vx = 2.8 + Math.random() * 3.8;
                p.vy = (Math.random() - 0.5) * 1.6;
                p.color = "#4ade80";
                p.glow = "#22c55e";
                p.size = 2.5 + Math.random() * 3.2;
            }}
            particles[idx] = p;
        }}

        function drawBackgroundGrid() {{
            ctx.strokeStyle = "rgba(168, 85, 247, 0.04)";
            ctx.lineWidth = 1;
            const step = 45;
            for (let x = 0; x < width; x += step) {{
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, height);
                ctx.stroke();
            }}
            for (let y = 0; y < height; y += step) {{
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(width, y);
                ctx.stroke();
            }}
        }}

        function drawBlackHole() {{
            const bhX = cx + mouseX;
            const bhY = cy + mouseY;

            // Gravitational Lensing Outer Glow
            const lGrad = ctx.createRadialGradient(bhX, bhY, 40, bhX, bhY, 270);
            lGrad.addColorStop(0, 'rgba(168, 85, 247, 0.48)');
            lGrad.addColorStop(0.35, 'rgba(56, 189, 248, 0.22)');
            lGrad.addColorStop(0.7, 'rgba(217, 70, 239, 0.09)');
            lGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');

            ctx.fillStyle = lGrad;
            ctx.beginPath();
            ctx.arc(bhX, bhY, 270, 0, Math.PI * 2);
            ctx.fill();

            // Accretion Disk Swirl
            accretionParticles.forEach(p => {{
                p.angle += p.speed;
                const rx = p.r;
                const ry = p.r * p.tiltY;
                const x = bhX + Math.cos(p.angle) * rx;
                const y = bhY + Math.sin(p.angle) * ry;

                ctx.fillStyle = 'hsla(' + p.hue + ', 90%, 65%, ' + p.opacity + ')';
                ctx.shadowColor = 'hsl(' + p.hue + ', 90%, 65%)';
                ctx.shadowBlur = 8;
                ctx.beginPath();
                ctx.arc(x, y, p.size, 0, Math.PI * 2);
                ctx.fill();
            }});
            ctx.shadowBlur = 0;

            // Photon Ring (Event Horizon Aura)
            const pRingGrad = ctx.createRadialGradient(bhX, bhY, 52, bhX, bhY, 70);
            pRingGrad.addColorStop(0, '#ffffff');
            pRingGrad.addColorStop(0.4, '#c084fc');
            pRingGrad.addColorStop(0.8, '#38bdf8');
            pRingGrad.addColorStop(1, 'transparent');

            ctx.fillStyle = pRingGrad;
            ctx.beginPath();
            ctx.arc(bhX, bhY, 70, 0, Math.PI * 2);
            ctx.fill();

            // Central Singularity Shadow
            const bhGrad = ctx.createRadialGradient(bhX, bhY, 0, bhX, bhY, 58);
            bhGrad.addColorStop(0, '#000000');
            bhGrad.addColorStop(0.85, '#020308');
            bhGrad.addColorStop(1, 'rgba(15, 23, 42, 0.95)');

            ctx.fillStyle = bhGrad;
            ctx.beginPath();
            ctx.arc(bhX, bhY, 58, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = "rgba(255, 255, 255, 0.65)";
            ctx.lineWidth = 1.5;
            ctx.shadowColor = "#38bdf8";
            ctx.shadowBlur = 14;
            ctx.beginPath();
            ctx.arc(bhX, bhY, 58, 0, Math.PI * 2);
            ctx.stroke();
            ctx.shadowBlur = 0;
        }}

        function updateAndDrawQuantumParticles() {{
            const bhX = cx + mouseX;
            const bhY = cy + mouseY;

            particles.forEach((p, idx) => {{
                ctx.fillStyle = p.color;
                ctx.shadowColor = p.glow;
                ctx.shadowBlur = 12;

                if (ETAPA_ACTUAL === "Entrada") {{
                    p.x += (bhX - p.x) * 0.032;
                    p.y += (bhY - p.y) * 0.032;
                    if (Math.hypot(bhX - p.x, bhY - p.y) < 58) {{
                        resetQuantumParticle(idx);
                    }}
                }} else if (ETAPA_ACTUAL === "Distribución") {{
                    p.angle += p.speed;
                    p.x = bhX + Math.cos(p.angle) * p.r;
                    p.y = bhY + Math.sin(p.angle) * (p.r * 0.4);
                }} else if (ETAPA_ACTUAL === "Radiación") {{
                    p.x += p.vx;
                    p.y += p.vy;
                    if (p.x < 0 || p.x > width || p.y < 0 || p.y > height) {{
                        resetQuantumParticle(idx);
                    }}
                }} else {{ // Recuperación
                    p.x += p.vx;
                    p.y += p.vy;
                    if (p.x > width + 20) {{
                        resetQuantumParticle(idx);
                    }}
                }}

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
            }});
            ctx.shadowBlur = 0;
        }}

        function animate() {{
            time += 0.015;
            mouseX += (targetMouseX - mouseX) * 0.05;
            mouseY += (targetMouseY - mouseY) * 0.05;

            ctx.clearRect(0, 0, width, height);
            drawBackgroundGrid();
            drawBlackHole();
            updateAndDrawQuantumParticles();

            requestAnimationFrame(animate);
        }}

        animate();
    }})();
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
    Renderiza el modelo visual interactivo en Streamlit.
    """
    st.subheader("🌌 Modelo Visual del Agujero Negro e Información Cuántica")

    st.write(
        """
        Esta simulación interactiva ilustra la **Paradoja de la Información del Agujero Negro**
        mediante un circuito de preserveración cuántica. Observa cómo la información cae en la singularidad,
        se dispersa en el horizonte de sucesos mediante entrelazamiento y es reconducida con alta fidelidad.
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

    components.html(html, height=740)

    st.info(escape(mensaje))

    st.caption(
        "💡 *Nota didáctica*: Esta representación es un modelo analógico cuántico que utiliza puertas unitarias "
        "reversibles para simular la recuperación de estados en horizontes gravitacionales."
    )