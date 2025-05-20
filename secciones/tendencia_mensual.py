
import streamlit as st
import plotly.express as px
from utils import clasificar_y_filtrar_productos, obtener_produccion_mensual
import pandas as pd

def mostrar(pais, anio):
    df_energy = obtener_produccion_mensual()
    df_energy['Time'] = pd.to_datetime(df_energy['Time'], format='%B %Y')
    df_energy['YearMonth'] = df_energy['Time'].dt.strftime('%Y-%m')

    tipos_energia = {
        'Renovables y No Renovables': 'ambas',
        'Solo Renovables': 'renovables',
        'Solo No Renovables': 'no_renovables'
    }
    tipo_energia = st.selectbox("Tipo de Energía", list(tipos_energia.keys()))
    modo = tipos_energia[tipo_energia]

    df_filtrado = clasificar_y_filtrar_productos(df_energy, pais=pais, tipo_energia=modo)
    df_monthly = df_filtrado.groupby(['YearMonth', 'Energy_Type'])['Value'].sum().reset_index()

    if df_monthly.empty:
        st.warning(f"No hay datos disponibles para {pais} y tipo {tipo_energia}")
        return

    df_pivot = df_monthly.pivot(index='YearMonth', columns='Energy_Type', values='Value').fillna(0)
    if 'Renewable' in df_pivot.columns and 'Non-Renewable' in df_pivot.columns:
        df_pivot = df_pivot[['Renewable', 'Non-Renewable']]
    df_pivot = df_pivot.reset_index()

    st.markdown("### 📈 Gráfico 1: Tendencia mensual de energía por tipo")
    fig_line = px.line(df_pivot, x='YearMonth', y=df_pivot.columns[1:], markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### 📊 Gráfico 2: Generación mensual apilada por tipo")
    fig_bar = px.bar(df_pivot, x='YearMonth', y=df_pivot.columns[1:], barmode="stack")
    st.plotly_chart(fig_bar, use_container_width=True)
