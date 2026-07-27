import pandas as pd
import streamlit as st

from logic.irreversible import (
    detectar_colisiones,
    generar_tabla_and,
)
from logic.reversible import (
    comprobar_recuperacion,
    generar_tabla_cnot,
    tiene_colisiones,
)
from quantum.circuits import dibujar_circuito
from quantum.engine import ejecutar_motor
from quantum.metrics import calcular_metricas_sistema
from quantum.noise import ejecutar_con_ruido
from quantum.visualizations import crear_esferas_bloch
from ui.black_hole_visual import (
    RUTA_IMAGEN,
    cargar_imagen_base64,
    crear_html_visual,
    obtener_datos_etapa,
)


THETA_DEMO = 120
PHI_DEMO = 95

PASOS = [
    {
        "titulo": "Problema y objetivo",
        "tiempo": "0:00 – 0:35",
    },
    {
        "titulo": "Lógica irreversible",
        "tiempo": "0:35 – 1:15",
    },
    {
        "titulo": "Lógica reversible",
        "tiempo": "1:15 – 1:55",
    },
    {
        "titulo": "Circuito cuántico",
        "tiempo": "1:55 – 3:20",
    },
    {
        "titulo": "Modelo del agujero negro",
        "tiempo": "3:20 – 4:35",
    },
    {
        "titulo": "Ruido y conclusión",
        "tiempo": "4:35 – 5:55",
    },
]


def tarjeta_guion(texto: str) -> None:
    """Muestra el fragmento recomendado para la exposición."""

    st.markdown("#### Explicación")

    st.info(texto)


def render_portada() -> None:
    st.html(
        """
        <div style="
            padding: 2.4rem;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background:
                radial-gradient(
                    circle at 80% 20%,
                    rgba(124, 58, 237, 0.28),
                    transparent 34%
                ),
                radial-gradient(
                    circle at 20% 80%,
                    rgba(56, 189, 248, 0.12),
                    transparent 30%
                ),
                rgba(255, 255, 255, 0.035);
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
            margin-bottom: 1.5rem;
        ">
            <div style="
                font-size: 3.2rem;
                margin-bottom: 0.4rem;
            ">
                ⚛
            </div>

            <h1 style="
                margin: 0 0 0.7rem 0;
                font-size: 2.4rem;
                letter-spacing: -0.04em;
            ">
                ¿Se destruye la información?
            </h1>

            <p style="
                color: #b8bfd6;
                font-size: 1.1rem;
                line-height: 1.6;
                max-width: 850px;
                margin: 0 auto;
            ">
                Comparación entre lógica irreversible, lógica reversible
                y circuitos cuánticos mediante un modelo inspirado en
                la paradoja de la información de los agujeros negros.
            </p>
        </div>
        """
    )

    columna_area, columna_aplicacion, columna_evidencia = st.columns(3)

    with columna_area:
        st.metric(
            "Área",
            "Lógica matemática",
        )

    with columna_aplicacion:
        st.metric(
            "Aplicación",
            "Desarrollo de software",
        )

    with columna_evidencia:
        st.metric(
            "Evidencia",
            "Simulación en Python",
        )

    tarjeta_guion(
        """
        En el desarrollo de software, transformar información no siempre
        significa conservarla. Algunas operaciones permiten reconstruir
        la entrada original, mientras que otras eliminan esa posibilidad.

        El objetivo del proyecto es comparar esos casos y utilizar un
        circuito cuántico simplificado para representar cómo la información
        puede distribuirse sin ser necesariamente destruida.
        """
    )

def render_and() -> None:
    st.header("Lógica irreversible: puerta AND")

    tabla = pd.DataFrame(generar_tabla_and())
    tabla.columns = [
        "Entrada A",
        "Entrada B",
        "Salida",
    ]

    columna_tabla, columna_resultado = st.columns([1.2, 1])

    with columna_tabla:
        st.dataframe(
            tabla,
            use_container_width=True,
            hide_index=True,
        )

    with columna_resultado:
        colisiones = detectar_colisiones()
        entradas_salida_cero = colisiones[0]

        st.metric(
            "Entradas posibles para la salida 0",
            len(entradas_salida_cero),
        )

        st.error(
            "La salida 0 puede provenir de 00, 01 o 10."
        )

        st.write(
            "Al observar únicamente la salida, no es posible "
            "reconstruir de manera única la entrada."
        )

    tarjeta_guion(
        """
        AND es irreversible porque varias entradas generan una misma
        salida. Si solamente recibimos un cero, no podemos saber si la
        entrada original fue 00, 01 o 10.

        Aquí la pérdida no es física ni cuántica: es una pérdida lógica
        causada por una transformación que elimina distinciones entre
        entradas.
        """
    )


def render_cnot() -> None:
    st.header("Lógica reversible: puerta CNOT")

    tabla = pd.DataFrame(generar_tabla_cnot())
    recuperacion = comprobar_recuperacion()

    columna_tabla, columna_metricas = st.columns([1.25, 1])

    with columna_tabla:
        st.dataframe(
            tabla,
            use_container_width=True,
            hide_index=True,
        )

    with columna_metricas:
        st.metric(
            "¿Presenta colisiones?",
            "Sí" if tiene_colisiones() else "No",
        )

        porcentaje = (
            sum(recuperacion.values())
            / len(recuperacion)
            * 100
        )

        st.metric(
            "Entradas recuperadas",
            f"{porcentaje:.0f} %",
        )

        st.success(
            "Aplicar CNOT dos veces devuelve cada entrada original."
        )

    tarjeta_guion(
        """
        CNOT mantiene una correspondencia única entre entradas y salidas.
        Además, es su propia inversa: al aplicarla una segunda vez,
        recuperamos exactamente la entrada.

        Esta propiedad introduce la idea central del proyecto:
        una transformación reversible conserva la información necesaria
        para reconstruir el estado anterior.
        """
    )


def render_circuito_cuantico() -> None:
    st.header("Distribución y recuperación cuántica")

    resultado = ejecutar_motor(
        theta_grados=THETA_DEMO,
        phi_grados=PHI_DEMO,
    )

    metricas_distribuidas = calcular_metricas_sistema(
        resultado.estado_distribuido
    )

    entropia_media = sum(
        metrica.entropia
        for metrica in metricas_distribuidas
    ) / len(metricas_distribuidas)

    pureza_media = sum(
        metrica.pureza
        for metrica in metricas_distribuidas
    ) / len(metricas_distribuidas)

    metricas = st.columns(3)

    with metricas[0]:
        st.metric("Estado preparado", f"θ={THETA_DEMO}°, φ={PHI_DEMO}°")

    with metricas[1]:
        st.metric(
            "Entropía distribuida",
            f"{entropia_media:.4f}",
        )

    with metricas[2]:
        st.metric(
            "Fidelidad recuperada",
            f"{resultado.fidelidad * 100:.4f} %",
        )

    columna_circuito, columna_bloch = st.columns(2)

    with columna_circuito:
        st.markdown("#### Circuito reversible")

        figura_circuito = dibujar_circuito(
            resultado.circuito_recuperacion
        )

        st.pyplot(
            figura_circuito,
            use_container_width=True,
        )

    with columna_bloch:
        st.markdown("#### Información distribuida")

        figura_bloch = crear_esferas_bloch(
            resultado.estado_distribuido,
            "Estado distribuido",
        )

        st.pyplot(
            figura_bloch,
            use_container_width=True,
        )

        st.caption(
            f"Pureza local promedio: {pureza_media:.4f}"
        )

    tarjeta_guion(
        """
        El circuito prepara un estado general y después aplica puertas
        unitarias que distribuyen la información entre tres cúbits.

        Al observar cada cúbit por separado, la entropía aumenta y la
        pureza disminuye. Sin embargo, el sistema global conserva la
        información en sus correlaciones.

        Al aplicar el circuito inverso, recuperamos el estado original
        con una fidelidad del 100 % en el modelo ideal.
        """
    )


def render_agujero_negro() -> None:
    st.header("Analogía con la paradoja de la información")

    resultado = ejecutar_motor(
        theta_grados=THETA_DEMO,
        phi_grados=PHI_DEMO,
    )

    try:
        imagen_uri = cargar_imagen_base64(
            str(RUTA_IMAGEN)
        )

    except FileNotFoundError as error:
        st.error(str(error))
        return

    (
        entropia,
        pureza,
        estado_sistema,
        mensaje,
    ) = obtener_datos_etapa(
        resultado,
        "Radiación",
    )

    html = crear_html_visual(
        imagen_uri=imagen_uri,
        etapa="Radiación",
        entropia=entropia,
        pureza=pureza,
        fidelidad=resultado.fidelidad,
        estado_sistema=estado_sistema,
    )

    st.html(html)

    st.info(mensaje)

    st.warning(
        "La visualización es una analogía computacional. "
        "No simula gravedad, espacio-tiempo ni radiación de Hawking."
    )

    tarjeta_guion(
        """
        La paradoja de la información pregunta qué ocurre con la
        información de la materia que cae en un agujero negro.

        Nuestro programa no simula un agujero negro real. Utiliza este
        problema como contexto para mostrar una posibilidad lógica:
        que la información deje de ser accesible localmente, pero siga
        conservada en el estado global y pueda recuperarse mediante una
        transformación inversa.
        """
    )


@st.cache_data(show_spinner=False)
def obtener_resultado_ruido_presentacion() -> float:
    """Calcula una vez el resultado usado en la presentación."""

    resultado = ejecutar_con_ruido(
        theta_grados=THETA_DEMO,
        phi_grados=PHI_DEMO,
        nivel_ruido=0.03,
    )

    return resultado.fidelidad


def render_ruido_conclusion() -> None:
    st.header("Modelo ideal, ruido y conclusión")

    fidelidad_ruidosa = (
        obtener_resultado_ruido_presentacion()
    )

    columnas = st.columns(3)

    with columnas[0]:
        st.metric(
            "Recuperación ideal",
            "100.000 %",
        )

    with columnas[1]:
        st.metric(
            "Recuperación con 3 % de ruido",
            f"{fidelidad_ruidosa * 100:.3f} %",
        )

    with columnas[2]:
        perdida = (1 - fidelidad_ruidosa) * 100

        st.metric(
            "Degradación",
            f"{perdida:.3f} %",
        )

    st.markdown("### Conclusión central")

    st.success(
        """
        La información puede desaparecer de una observación local
        sin haber sido destruida en el sistema global.
        """
    )

    st.write(
        """
        - AND muestra irreversibilidad lógica.
        - CNOT demuestra reversibilidad clásica.
        - Las puertas cuánticas unitarias distribuyen y recuperan información.
        - El ruido altera físicamente el estado, aunque la transformación
          matemática siga teniendo inversa.
        """
    )

    tarjeta_guion(
        """
        El proyecto demuestra tres situaciones distintas.

        En AND existe pérdida lógica porque varias entradas comparten una
        salida. En CNOT la información se conserva y puede recuperarse.
        En el circuito cuántico, la información se distribuye en
        correlaciones y reaparece al invertir la transformación.

        Finalmente, el ruido muestra que reversibilidad matemática no
        garantiza recuperación perfecta cuando el estado físico ha sido
        alterado.
        """
    )


RENDERIZADORES = [
    render_portada,
    render_and,
    render_cnot,
    render_circuito_cuantico,
    render_agujero_negro,
    render_ruido_conclusion,
]


def render_modo_presentacion() -> None:
    """
    Renderiza una presentación guiada de aproximadamente
    seis minutos.
    """

    if "paso_presentacion" not in st.session_state:
        st.session_state.paso_presentacion = 0

    paso = st.session_state.paso_presentacion
    datos_paso = PASOS[paso]

    encabezado_1, encabezado_2 = st.columns([4, 1])

    with encabezado_1:
        st.markdown(
            f"### Paso {paso + 1} de {len(PASOS)}: "
            f"{datos_paso['titulo']}"
        )

    with encabezado_2:
        st.metric(
            "Tiempo sugerido",
            datos_paso["tiempo"],
        )

    st.progress(
        (paso + 1) / len(PASOS)
    )

    st.divider()

    RENDERIZADORES[paso]()

    st.divider()

    columna_anterior, columna_centro, columna_siguiente = st.columns(
        [1, 2, 1]
    )

    with columna_anterior:
        if st.button(
            "← Anterior",
            disabled=paso == 0,
            use_container_width=True,
            key="presentacion_anterior",
        ):
            st.session_state.paso_presentacion -= 1
            st.rerun()

    with columna_centro:
        st.caption(
            "Usa las flechas para recorrer el guion sin cambiar "
            "manualmente entre todas las herramientas."
        )

    with columna_siguiente:
        texto_boton = (
            "Finalizar"
            if paso == len(PASOS) - 1
            else "Siguiente →"
        )

        if st.button(
            texto_boton,
            use_container_width=True,
            key="presentacion_siguiente",
        ):
            if paso < len(PASOS) - 1:
                st.session_state.paso_presentacion += 1
            else:
                st.session_state.paso_presentacion = 0

            st.rerun()