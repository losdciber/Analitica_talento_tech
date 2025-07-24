#Importaciones
#st: para la interfaz web.

#pd: para el manejo de datos.

#px: para gráficos interactivos con Plotly.

#ejecutar_consulta: función personalizada para obtener datos desde una base de datos (probablemente SQLite o PostgreSQL).

# separación clara entre visualización, datos y lógica de consulta.

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ejecutar_consulta

# 🎨 Paleta de colores

#Se define un diccionario para asignar colores específicos a cada fuente energética.

#Esto mejora la consistencia visual entre gráficos.

#Buenísima práctica para que el usuario pueda reconocer intuitivamente cada fuente en gráficos distintos.

COLOR_PALETTE = {
    'PETROLEO': '#636EFA',
    'GAS NATURAL': '#EF553B',
    'CARBON MINERAL': '#00CC96',
    'HIDROENERGIA': '#AB63FA',
    'LENA': '#FFA15A',
    'BAGAZO': '#19D3F3',
    'OTROS RENOVABLES': '#FF6692',
    'RECUPERACION_RESIDUOS': '#B6E880'
}

# Funcion Principal
#Define el punto de entrada de esta sección del dashboard.

#Aunque se recibe df_global, no se usa, ya que internamente se consulta BECO_Histórico.

def mostrar(df_global):
    st.title("🔋 Matriz Energética de Colombia")

    # CConsulta y carga de datos / cargar datos desde la tabla BECO_Histórico


#Obtiene todos los registros de una tabla energética histórica.

#Luego se filtra por año y fuente según las selecciones del usuario.

    df = ejecutar_consulta('SELECT * FROM "BECO_Histórico"')

    # Sidebar con filtros

#Se implementan dos filtros:

#Selección de año.

#Selección de fuentes energéticas.

#Los valores se actualizan dinámicamente con base en los datos disponibles del año seleccionado.

#natural e intuitivo para el usuario.

    with st.sidebar:
        st.markdown("### 🎛️ Filtros - Matriz Energética")

        anios = sorted(df["YEAR"].unique())
        anio = st.selectbox("📅 Selecciona un año", anios, index=len(anios) - 1)

        df_anio = df[df["YEAR"] == anio]
        fuentes_disponibles = sorted(df_anio["NOMBRE_ENERGETICO"].dropna().unique())
        fuentes_sel = st.multiselect(
            "🔌 Selecciona fuentes energéticas",
            options=fuentes_disponibles,
            default=fuentes_disponibles,
            key="fuentes_matriz"
        )

    # Filtrado y preparación de datos

    #Se filtra el DataFrame para incluir solo los valores seleccionados por el usuario.

#Se genera color_map dinámico

    df_filtrado = df_anio[df_anio["NOMBRE_ENERGETICO"].isin(fuentes_sel)]
    color_map = {fuente: COLOR_PALETTE.get(fuente, "#CCCCCC") for fuente in fuentes_sel}

    # Crear pestañas para los gráficos /Gráfica 1: Pie Chart

#Gráfico de pastel para distribución energética de un año específico.

#Usa hole=0.3 para efecto donut.

#Colores personalizados, textinfo='percent+label'.

    tab1, tab2 = st.tabs(["🧁 Distribución Energética", "📈 Participación Histórica"])

    with tab1:
        st.markdown("### 🧁 Distribución Energética por Fuente")
        fig_pie = px.pie(
            df_filtrado,
            values="OFERTA_INTERNA_BRUTA_TJ",
            names="NOMBRE_ENERGETICO",
            title=f"Distribución Energética {anio}",
            hole=0.3,
            color="NOMBRE_ENERGETICO",
            color_discrete_map=color_map,

        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)


        # 🔽 Descripción textual
        st.markdown("""
    **Tipo de gráfico:** Gráfico de pastel (donut)  
    **Descripción:** Este gráfico muestra la participación porcentual de cada fuente energética en la matriz de Colombia para el año seleccionado.  
    Permite comparar visualmente la proporción de energía aportada por cada fuente (como petróleo, gas, hidroenergía, etc.) en un año específico.
    """)

#Gráfica 2: Bar Chart Apilado

#Muestra la evolución histórica del porcentaje de cada fuente energética.

#Agrupa por año y fuente energética, calcula el porcentaje para cada año.

#Gráfico de barras apiladas (barmode="stack").

# uso de transform() y groupby() en pandas.
#Gráfico ideal para ver tendencias a largo plazo.


    with tab2:
        st.markdown("### 📈 Participación % por Fuente - Evolución Histórica")
        df_stack = df[df["NOMBRE_ENERGETICO"].isin(fuentes_sel)].copy()
        df_group = df_stack.groupby(["YEAR", "NOMBRE_ENERGETICO"])["OFERTA_INTERNA_BRUTA_TJ"].sum().reset_index()
        df_group["Porcentaje"] = df_group.groupby("YEAR")["OFERTA_INTERNA_BRUTA_TJ"].transform(
            lambda x: x / x.sum() * 100
        )

        fig_bar = px.bar(
            df_group,
            x="YEAR",
            y="Porcentaje",
            color="NOMBRE_ENERGETICO",
            title="Participación % por Fuente",
            labels={"Porcentaje": "Participación (%)", "YEAR": "Año", "NOMBRE_ENERGETICO": "Fuente"},
            color_discrete_map=color_map
        )
        fig_bar.update_layout(barmode="stack", yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_bar, use_container_width=True)

# 🔽 Descripción textual
        st.markdown("""
    **Tipo de gráfico:** Gráfico de barras apiladas  
    **Descripción:** Este gráfico muestra la evolución histórica de la participación porcentual de cada fuente energética en Colombia.  
    Permite observar cómo ha cambiado la matriz energética del país a lo largo de los años, identificando tendencias, reemplazos o permanencia de fuentes.
    """)