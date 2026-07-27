import pandas as pd
import streamlit as st
from ui.comparison_section import render_comparison_section
from ui.hero import render_hero
from ui.quantum_section import render_quantum_section
from ui.advanced_quantum import render_motor_avanzado
from ui.intro_section import render_intro
from ui.presentation_mode import render_modo_presentacion
from logic.irreversible import (
    agrupar_entradas_por_salida,
    detectar_colisiones,
    generar_tabla_and,
)
from logic.reversible import (
    comprobar_recuperacion,
    generar_tabla_cnot,
    tiene_colisiones,
)
from quantum.circuits import (
    crear_circuito_medicion,
    crear_circuito_recuperacion,
    dibujar_circuito,
    simular_circuito,
)
from ui.styles import aplicar_estilos
from ui.logic_sections import (
    render_and_section,
    render_cnot_section,
)

# Configuración general
st.set_page_config(
    page_title="Preservación de información",
    page_icon="⚛️",
    layout="wide",
)

aplicar_estilos()


# Encabezado
render_hero()

# Pestañas principales
(
    tab_presentacion,
    tab_intro,
    tab_and,
    tab_cnot,
    tab_circuito,
    tab_motor,
    tab_comparacion,
) = st.tabs(
    [
        "Modo presentación",
        "Introducción",
        "Lógica irreversible",
        "Lógica reversible",
        "Circuito cuántico",
        "Motor avanzado",
        "Comparación final",
    ]
)
# ---------------------------------------------------------
# INTRODUCCIÓN
# ---------------------------------------------------------
with tab_presentacion:
    render_modo_presentacion()
with tab_intro:
    render_intro()

# ---------------------------------------------------------
# LÓGICA IRREVERSIBLE
# ---------------------------------------------------------
with tab_and:
    render_and_section()



# ---------------------------------------------------------
# LÓGICA REVERSIBLE
# ---------------------------------------------------------
with tab_cnot:
    render_cnot_section()

# ---------------------------------------------------------
# CIRCUITO CUÁNTICO
# ---------------------------------------------------------
with tab_circuito:
    render_quantum_section()

with tab_motor:
    render_motor_avanzado()


# ---------------------------------------------------------
# COMPARACIÓN FINAL
# ---------------------------------------------------------
with tab_comparacion:
    render_comparison_section()