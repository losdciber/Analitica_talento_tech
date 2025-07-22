import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ejecutar_consulta, mostrar_tarjeta_valor_maximo

def mostrar(df):
    st.title("🌿 Emisiones de CO₂")

    # Obtener datos
    df = ejecutar_consulta("SELECT * FROM 'International Energy Agency - CO2 emissions by sector in Colombia'")

    # 🎛️ Filtros en el sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Filtros - Emisiones de CO₂")
        anios = sorted(df['Year'].dropna().unique())
        anio_sel = st.selectbox("📅 Año", anios, index=len(anios) - 1)
        sectores_disponibles = sorted(df['Sector'].dropna().unique())
        sectores_sel = st.multiselect("🏭 Sectores", sectores_disponibles, default=sectores_disponibles)

    # Filtro de datos
    df_filtrado = df[(df['Year'] == anio_sel) & (df['Sector'].isin(sectores_sel))].copy()
    df_filtrado = df_filtrado.sort_values(by='Value', ascending=False).reset_index(drop=True)

    # Calcular participación porcentual
    total_emisiones = df_filtrado['Value'].sum()
    df_filtrado['Porcentaje'] = df_filtrado['Value'] / total_emisiones * 100

    # 🏆 Tarjeta
    mostrar_tarjeta_valor_maximo(
        df_filtrado,
        campo_clave="Sector",
        campo_valor="Value",
        titulo=f"",
        unidad="MtCO₂",
        color="#1F4E79"
    )

    # 📊 Tabla + Gráfico lado a lado alineados
    st.markdown("### 📋 Emisiones de CO₂ por Sector - %Participación")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.dataframe(
            df_filtrado[['Sector', 'Value']],
            hide_index=True,
            use_container_width=True,
            height=(len(df_filtrado) * 35 + 50)
        )

    with col2:
        fig = px.bar(
            df_filtrado,
            x="Porcentaje",
            y="Sector",
            orientation="h",
            color_discrete_sequence=["salmon"],
            text=df_filtrado["Porcentaje"].apply(lambda x: f"{x:.1f}%")
        )
        fig.update_layout(
            title="% de Participación del sector",
            xaxis_title=None,
            yaxis_title=None,
            yaxis=dict(showticklabels=False, categoryorder='total ascending'),
            xaxis=dict(showticklabels=False),
            margin=dict(l=10, r=10, t=38, b=10),
            height=(len(df_filtrado) * 35 + 50),
            uniformtext_minsize=9,
            uniformtext_mode='show',
        )
        st.plotly_chart(fig, use_container_width=True)

    # 📈 Gráfico de área apilada
    st.markdown("### 📈 Evolución Histórica de Emisiones")
    df_group = df[df['Sector'].isin(sectores_sel)].groupby(['Year', 'Sector'])['Value'].sum().reset_index()
    fig2 = px.area(
        df_group,
        x='Year',
        y='Value',
        color='Sector',
        #title='Evolución Histórica de Emisiones de CO₂ por Sector',
        labels={'Value': 'Emisiones de CO₂ (MtCO₂)'}
    )
    fig2.update_layout(legend_title_text='Sector', hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

