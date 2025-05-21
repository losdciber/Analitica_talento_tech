
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import clasificar_y_filtrar_productos, obtener_produccion_mensual

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
    fig_line = px.line(
        df_pivot,
        x='YearMonth',
        y=df_pivot.columns[1:],
        color_discrete_map={"Renewable": "#2ca02c", "Non-Renewable": "#d62728"},
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### 📊 Gráfico 2: Generación mensual apilada por tipo")
    fig_bar = px.bar(
        df_pivot,
        x='YearMonth',
        y=df_pivot.columns[1:],
        barmode="stack",
        color_discrete_map={"Renewable": "#2ca02c", "Non-Renewable": "#d62728"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("### 📉 Gráfico 3: Participación porcentual anual de energías renovables vs no renovables")
    df_energy_filtered = clasificar_y_filtrar_productos(df_energy, pais=pais)
    df_energy_filtered['Year'] = df_energy_filtered['Time'].dt.year
    df_total_by_year = df_energy_filtered.groupby('Year')['Value'].sum().reset_index(name='Total_Year_Value')
    df_agg = df_energy_filtered.groupby(['Year', 'Energy_Type'])['Value'].sum().reset_index()
    df_agg = df_agg.merge(df_total_by_year, on='Year')
    df_agg['Percentage'] = df_agg['Value'] / df_agg['Total_Year_Value'] * 100
    df_percent_pivot = df_agg.pivot(index='Year', columns='Energy_Type', values='Percentage').fillna(0)
    if 'Renewable' in df_percent_pivot.columns and 'Non-Renewable' in df_percent_pivot.columns:
        df_percent_pivot = df_percent_pivot[['Renewable', 'Non-Renewable']]
    fig_porc = px.bar(
        df_percent_pivot,
        x=df_percent_pivot.index,
        y=['Renewable', 'Non-Renewable'],
        title=f"% Participación de Energía Renovable vs No Renovable - {pais if pais != 'Todos' else 'Global'}",
        labels={"value": "Porcentaje (%)", "Year": "Año", "variable": "Tipo de Energía"},
        barmode='stack',
        color_discrete_map={"Renewable": "#2ca02c", "Non-Renewable": "#d62728"}
    )
    fig_porc.update_layout(yaxis_range=[0, 100], xaxis_title="Año", yaxis_title="Porcentaje (%)", legend_title="Tipo de Energía")
    st.plotly_chart(fig_porc, use_container_width=True)
