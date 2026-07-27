import json
from html import escape

import pandas as pd
import streamlit as st

from logic.irreversible import generar_tabla_and
from logic.reversible import (
    comprobar_recuperacion,
    generar_tabla_cnot,
)
from quantum.engine import ResultadoMotor
from quantum.metrics import calcular_metricas_sistema
from quantum.noise import ejecutar_con_ruido


def crear_tabla_metricas(
    resultado: ResultadoMotor,
) -> pd.DataFrame:
    """
    Reúne las métricas locales de los tres cúbits
    durante las etapas inicial, distribuida y recuperada.
    """

    etapas = {
        "Inicial": resultado.estado_inicial,
        "Distribuido": resultado.estado_distribuido,
        "Recuperado": resultado.estado_recuperado,
    }

    filas = []

    for nombre_etapa, estado in etapas.items():
        metricas = calcular_metricas_sistema(estado)

        for metrica in metricas:
            filas.append(
                {
                    "Etapa": nombre_etapa,
                    "Cúbit": metrica.qubit,
                    "Entropía": round(
                        metrica.entropia,
                        8,
                    ),
                    "Pureza": round(
                        metrica.pureza,
                        8,
                    ),
                }
            )

    return pd.DataFrame(filas)


def crear_resumen(
    resultado: ResultadoMotor,
    theta: float,
    phi: float,
    nivel_ruido: float,
    fidelidad_ruidosa: float,
) -> dict:
    """
    Crea un resumen estructurado de la simulación.
    """

    recuperacion_cnot = comprobar_recuperacion()

    return {
        "proyecto": (
            "Preservación de información mediante lógica "
            "reversible y circuitos cuánticos"
        ),
        "parametros": {
            "theta_grados": theta,
            "phi_grados": phi,
            "nivel_ruido": nivel_ruido,
        },
        "resultados": {
            "and_es_irreversible": True,
            "cnot_recupera_todas_las_entradas": all(
                recuperacion_cnot.values()
            ),
            "fidelidad_ideal": resultado.fidelidad,
            "fidelidad_con_ruido": fidelidad_ruidosa,
            "perdida_por_ruido": (
                1.0 - fidelidad_ruidosa
            ),
        },
        "alcance": (
            "Modelo lógico y computacional simplificado. "
            "No representa un agujero negro físico real."
        ),
    }


def crear_informe_html(
    resultado: ResultadoMotor,
    theta: float,
    phi: float,
    nivel_ruido: float,
    fidelidad_ruidosa: float,
    tabla_metricas: pd.DataFrame,
) -> str:
    """
    Genera un informe HTML autocontenido.

    Puede abrirse en el navegador y guardarse posteriormente
    como PDF mediante la opción de impresión.
    """

    tabla_and = pd.DataFrame(
        generar_tabla_and()
    )

    tabla_and.columns = [
        "Entrada A",
        "Entrada B",
        "Salida",
    ]

    tabla_cnot = pd.DataFrame(
        generar_tabla_cnot()
    )

    recuperacion_cnot = comprobar_recuperacion()

    porcentaje_cnot = (
        sum(recuperacion_cnot.values())
        / len(recuperacion_cnot)
        * 100
    )

    fidelidad_ideal = resultado.fidelidad * 100
    fidelidad_ruido = fidelidad_ruidosa * 100
    perdida = 100 - fidelidad_ruido

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">

    <title>
        Evidencia técnica de lógica cuántica
    </title>

    <style>
        body {{
            font-family:
                Arial,
                Helvetica,
                sans-serif;

            max-width: 1000px;
            margin: 40px auto;
            padding: 0 24px;
            color: #172033;
            line-height: 1.55;
        }}

        h1, h2 {{
            color: #312e81;
        }}

        .portada {{
            padding: 32px;
            border-radius: 18px;
            color: white;
            background:
                linear-gradient(
                    135deg,
                    #111827,
                    #312e81
                );
            margin-bottom: 30px;
        }}

        .aviso {{
            padding: 14px;
            border-left: 5px solid #f59e0b;
            background: #fffbeb;
            margin: 20px 0;
        }}

        .metricas {{
            display: grid;
            grid-template-columns:
                repeat(3, 1fr);
            gap: 14px;
            margin: 20px 0;
        }}

        .metrica {{
            padding: 16px;
            border-radius: 12px;
            background: #f1f5f9;
            border: 1px solid #dbe2ea;
        }}

        .metrica strong {{
            display: block;
            font-size: 1.35rem;
            margin-top: 5px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0 26px;
        }}

        th, td {{
            padding: 9px;
            border: 1px solid #cbd5e1;
            text-align: center;
        }}

        th {{
            background: #e0e7ff;
        }}

        .conclusion {{
            padding: 20px;
            border-radius: 14px;
            background: #ecfdf5;
            border: 1px solid #6ee7b7;
        }}

        @media print {{
            body {{
                margin: 0;
                max-width: none;
            }}

            .portada {{
                break-after: avoid;
            }}
        }}
    </style>
</head>

<body>
    <section class="portada">
        <h1 style="color: white;">
            ¿Se destruye la información?
        </h1>

        <p>
            Evidencia técnica de la comparación entre lógica
            irreversible, lógica reversible y circuitos cuánticos.
        </p>
    </section>

    <div class="aviso">
        Este documento corresponde a un modelo lógico y
        computacional simplificado. No simula físicamente
        un agujero negro, gravedad, espacio-tiempo ni
        radiación de Hawking.
    </div>

    <h2>Parámetros de la simulación</h2>

    <div class="metricas">
        <div class="metrica">
            Ángulo θ
            <strong>{theta:.0f}°</strong>
        </div>

        <div class="metrica">
            Ángulo φ
            <strong>{phi:.0f}°</strong>
        </div>

        <div class="metrica">
            Ruido aplicado
            <strong>{nivel_ruido * 100:.0f} %</strong>
        </div>
    </div>

    <h2>1. Lógica irreversible: AND</h2>

    <p>
        La puerta AND presenta colisiones porque varias
        entradas diferentes generan la misma salida.
    </p>

    {tabla_and.to_html(index=False)}

    <h2>2. Lógica reversible: CNOT</h2>

    <p>
        CNOT no presenta colisiones y, al aplicarse dos veces,
        recuperó el {porcentaje_cnot:.0f} % de las entradas.
    </p>

    {tabla_cnot.to_html(index=False)}

    <h2>3. Métricas del circuito cuántico</h2>

    <p>
        La entropía y la pureza muestran cómo cambia el estado
        local de cada cúbit durante la distribución y la
        recuperación.
    </p>

    {tabla_metricas.to_html(index=False)}

    <h2>4. Fidelidad de recuperación</h2>

    <div class="metricas">
        <div class="metrica">
            Modelo ideal
            <strong>{fidelidad_ideal:.6f} %</strong>
        </div>

        <div class="metrica">
            Modelo con ruido
            <strong>{fidelidad_ruido:.6f} %</strong>
        </div>

        <div class="metrica">
            Degradación
            <strong>{perdida:.6f} %</strong>
        </div>
    </div>

    <section class="conclusion">
        <h2>Conclusión técnica</h2>

        <p>
            AND representa una transformación irreversible,
            porque diferentes entradas pueden producir la misma
            salida. CNOT y las puertas cuánticas unitarias
            conservan una transformación invertible.
        </p>

        <p>
            Durante la etapa distribuida, la información deja
            de estar localizada en un solo cúbit y pasa a las
            correlaciones globales del sistema. En el modelo
            ideal, la transformación inversa permite recuperar
            el estado inicial. El ruido, en cambio, altera el
            estado durante la ejecución y reduce su fidelidad.
        </p>
    </section>
</body>
</html>
"""


def render_panel_exportacion(
    resultado: ResultadoMotor,
    theta: float,
    phi: float,
) -> None:
    """
    Renderiza los botones para descargar las evidencias
    técnicas de la simulación.
    """

    st.subheader("Exportación de evidencias")

    st.write(
        """
        Descarga los resultados actuales para incorporarlos
        al informe, conservarlos como respaldo o mostrarlos
        durante la presentación.
        """
    )

    nivel_ruido_porcentaje = st.slider(
        "Ruido utilizado en la evidencia:",
        min_value=0,
        max_value=30,
        value=3,
        step=1,
        format="%d %%",
        key="ruido_exportacion",
    )

    nivel_ruido = nivel_ruido_porcentaje / 100

    resultado_ruidoso = ejecutar_con_ruido(
        theta_grados=theta,
        phi_grados=phi,
        nivel_ruido=nivel_ruido,
    )

    tabla_metricas = crear_tabla_metricas(
        resultado
    )

    resumen = crear_resumen(
        resultado=resultado,
        theta=theta,
        phi=phi,
        nivel_ruido=nivel_ruido,
        fidelidad_ruidosa=(
            resultado_ruidoso.fidelidad
        ),
    )

    informe_html = crear_informe_html(
        resultado=resultado,
        theta=theta,
        phi=phi,
        nivel_ruido=nivel_ruido,
        fidelidad_ruidosa=(
            resultado_ruidoso.fidelidad
        ),
        tabla_metricas=tabla_metricas,
    )

    csv_metricas = tabla_metricas.to_csv(
        index=False
    ).encode("utf-8-sig")

    json_resumen = json.dumps(
        resumen,
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8")

    html_bytes = informe_html.encode("utf-8")

    columna_html, columna_csv, columna_json = st.columns(3)

    with columna_html:
        st.download_button(
            label="Descargar informe HTML",
            data=html_bytes,
            file_name="evidencia_logica_cuantica.html",
            mime="text/html",
            use_container_width=True,
            key="descargar_html",
        )

    with columna_csv:
        st.download_button(
            label="Descargar métricas CSV",
            data=csv_metricas,
            file_name="metricas_cuanticas.csv",
            mime="text/csv",
            use_container_width=True,
            key="descargar_csv",
        )

    with columna_json:
        st.download_button(
            label="Descargar resumen JSON",
            data=json_resumen,
            file_name="resumen_simulacion.json",
            mime="application/json",
            use_container_width=True,
            key="descargar_json",
        )

    st.info(
        """
        El archivo HTML puede abrirse en cualquier navegador.
        Desde allí puedes usar **Imprimir → Guardar como PDF**
        para obtener una evidencia lista para adjuntar.
        """
    )