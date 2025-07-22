import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ejecutar_consulta

# Diccionario de tablas por sector
tablas = {
    'Sector Transporte': 'International Energy Agency - transport total final consumption by source in Colombia',
    'Sector Residencial': 'International Energy Agency - residential total final consumption by source in Colombia',
    'Sector Industrial': 'International Energy Agency - industry total final consumption by source in Colombia'
}

# Paleta de colores fija por fuente
colores_fijos = {
    'Electricity': '#636EFA',
    'Gasoline': '#EF553B',
    'Diesel': '#00CC96',
    'Natural Gas': '#AB63FA',
    'Jet fuel': '#FFA15A',
    'Biofuels and waste': '#19D3F3',
    'Solar': '#FF6692',
    'Wind': '#B6E880',
    'Hydro': '#FF97FF',
    'Geothermal': '#FECB52',
    'Coal': '#A3A3A3',
    'Kerosene': '#2ca02c',
    'Liquefied petroleum gases': '#d62728',
    'Fuel oil': '#9467bd',
    'Other': '#8c564b'
}

def mostrar(df_global):
    st.title("⚡ Consumo Energético por Sector")

    # Crear pestañas por sector
    nombres_sectores = list(tablas.keys())
    tabs = st.tabs(nombres_sectores)

    for i, (sector, tabla) in enumerate(tablas.items()):
        with tabs[i]:
            df_sector = ejecutar_consulta(f"SELECT * FROM '{tabla}'")
            df_sector = df_sector[df_sector["Value"].notna()]

            if df_sector.empty:
                st.warning(f"No hay datos válidos para {sector}.")
                continue

            anios = sorted(df_sector["Year"].dropna().unique())
            fuentes_disponibles = sorted(df_sector["Source"].dropna().unique())

            # Filtros exclusivos de esta pestaña
            with st.sidebar:
                st.markdown(f"### 🎛️ Filtros - {sector}")
                anio_sel = st.selectbox(
                    "📅 Año",
                    options=anios,
                    index=len(anios) - 1,
                    key=f"anio_{sector}"
                )
                fuentes_sel = st.multiselect(
                    "🔌 Fuentes energéticas",
                    options=fuentes_disponibles,
                    default=fuentes_disponibles,
                    key=f"fuentes_{sector}"
                )

            # Filtrar datos
            df_anio = df_sector[df_sector["Year"] == anio_sel]
            df_anio_filtrado = df_anio[df_anio["Source"].isin(fuentes_sel)]

            # Torta y barras
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🧁 Torta por Fuente")
                fig_pie = px.pie(
                    df_anio_filtrado,
                    names="Source",
                    values="Value",
                    hole=0.3,
                    title=f"{sector} - {anio_sel}",
                    color="Source",
                    color_discrete_map=colores_fijos
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                st.markdown("#### 📊 Barras Apiladas 100%")
                df_group = df_sector[df_sector["Source"].isin(fuentes_sel)]
                df_group = df_group.groupby(["Year", "Source"])["Value"].sum().reset_index()
                df_group["Total"] = df_group.groupby("Year")["Value"].transform("sum")
                df_group["Porcentaje"] = df_group["Value"] / df_group["Total"] * 100

                fig_bar = px.bar(
                    df_group,
                    x="Year",
                    y="Porcentaje",
                    color="Source",
                    title="Participación % por Fuente",
                    labels={"Porcentaje": "Participación (%)", "Source": "Fuente", "Year": "Año"},
                    color_discrete_map=colores_fijos
                )
                fig_bar.update_layout(barmode="stack", yaxis=dict(range=[0, 100]))
                st.plotly_chart(fig_bar, use_container_width=True)

            # Área apilada histórica
            st.markdown("#### 📈 Evolución Histórica Absoluta")
            df_historico = df_sector[df_sector["Source"].isin(fuentes_sel)]
            df_area = df_historico.groupby(["Year", "Source"])["Value"].sum().reset_index()

            fig_area = px.area(
                df_area,
                x="Year",
                y="Value",
                color="Source",
                title=f"Evolución del Consumo - {sector}",
                labels={"Value": "Consumo (TJ)", "Year": "Año", "Source": "Fuente"},
                color_discrete_map=colores_fijos
            )
            fig_area.update_layout(legend_title_text="Fuente", hovermode="x unified")
            st.plotly_chart(fig_area, use_container_width=True)





