
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def mostrar(pais, anio, df):
    st.subheader(f"Comparativos Internacionales - {anio}")

    df_anio = df[df['Year'] == anio]
    top_paises = df_anio.groupby('Country')['Value'].sum().nlargest(10).reset_index()

    st.markdown("### 🌍 Gráfico 1: Treemap – Top 10 Países")
    fig1 = px.treemap(top_paises, path=['Country'], values='Value', title="Top 10 Países por Producción")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 📊 Gráfico 2: Barras – Top 10 Países")
    fig2 = px.bar(top_paises, x="Country", y="Value", text_auto=True, title="Producción por País")
    st.plotly_chart(fig2, use_container_width=True)

    # Subgráficos comparativos
    fuentes_renovables = ['Wind', 'Solar', 'Other Renewables', 'Hydro', 'Geothermal', 'Combustible Renewables']
    fuentes_no_renovables = ['Coal, Peat and Manufactured Gases', 'Oil and Petroleum Products', 'Natural Gas',
                             'Other Combustible Non-Renewables', 'Nuclear']
    df_net = df[df['Balance'] == 'Net Electricity Production'].copy()
    df_net_anio = df_net[df_net['Year'] == anio]
    df_ren = df_net_anio[df_net_anio['Product'].isin(fuentes_renovables)]
    df_no_ren = df_net_anio[df_net_anio['Product'].isin(fuentes_no_renovables)]

    df_ren_pivot = df_ren.groupby(['Year', 'Product'])['Value'].sum().reset_index().pivot(index='Year', columns='Product', values='Value').fillna(0)
    df_no_ren_pivot = df_no_ren.groupby(['Year', 'Product'])['Value'].sum().reset_index().pivot(index='Year', columns='Product', values='Value').fillna(0)

    fig_sub = make_subplots(rows=1, cols=2, subplot_titles=("Energías Renovables", "Energías No Renovables"))
    for col in df_ren_pivot.columns:
        fig_sub.add_trace(go.Bar(name=col, x=df_ren_pivot.index, y=df_ren_pivot[col]), row=1, col=1)
    for col in df_no_ren_pivot.columns:
        fig_sub.add_trace(go.Bar(name=col, x=df_no_ren_pivot.index, y=df_no_ren_pivot[col]), row=1, col=2)

    fig_sub.update_layout(barmode='stack', height=500, title_text="Comparativo Energético por Año")
    st.markdown("### 🪟 Gráfico 3: Subgráficos Comparativos")
    st.plotly_chart(fig_sub, use_container_width=True)
