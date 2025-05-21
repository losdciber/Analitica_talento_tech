
import streamlit as st
import plotly.express as px
from utils import obtener_emisiones_co2

def mostrar(anio):
    """
    Visualiza las emisiones de CO₂ para Colombia en el año seleccionado.
    Los datos se extraen de la tabla específica de emisiones.
    """
    df = obtener_emisiones_co2()

    df_filtrado = df[df['Year'] == anio]

    if df_filtrado.empty or "CO2 Emissions" not in df_filtrado["Product"].unique():
        st.warning("⚠️ No hay datos de emisiones de CO₂ disponibles para el año seleccionado.")
        return

    df_emisiones = df_filtrado[df_filtrado["Product"] == "CO2 Emissions"]

    st.markdown("### 🌍 Gráfico 1: Emisiones totales de CO₂")
    fig1 = px.bar(
        df_emisiones,
        x="Year",
        y="Value",
        title="Emisiones totales de CO₂ (Colombia)",
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 📈 Gráfico 2: Tendencia histórica de emisiones en Colombia")
    df_hist = df[df['Product'] == "CO2 Emissions"]
    df_hist = df_hist.groupby("Year")["Value"].sum().reset_index()

    fig2 = px.line(
        df_hist,
        x="Year",
        y="Value",
        title="Evolución de las emisiones de CO₂ en Colombia"
    )
    st.plotly_chart(fig2, use_container_width=True)
