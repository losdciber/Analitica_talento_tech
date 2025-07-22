import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ejecutar_consulta

# 🎨 Paleta de colores
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

def mostrar(df_global):
    st.title("🔋 Matriz Energética de Colombia")

    # Cargar datos desde la tabla BECO_Histórico
    df = ejecutar_consulta('SELECT * FROM "BECO_Histórico"')

    # 🎛️ Filtros en el sidebar
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

    # Filtrar datos
    df_filtrado = df_anio[df_anio["NOMBRE_ENERGETICO"].isin(fuentes_sel)]
    color_map = {fuente: COLOR_PALETTE.get(fuente, "#CCCCCC") for fuente in fuentes_sel}

    # Crear pestañas para los gráficos
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
            color_discrete_map=color_map
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

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
