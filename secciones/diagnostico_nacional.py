
import streamlit as st
import plotly.express as px

def mostrar(pais, anio, df):
    st.subheader(f"Diagnóstico Energético - {pais} ({anio})")

    df_filtrado = df[df['Year'] == anio]
    if pais != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Country'] == pais]

    st.markdown("### 🏭 Gráfico 1: Producción por Fuente")
    fig1 = px.bar(df_filtrado, x="Value", y="Product", orientation="h", title="Producción por Fuente")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 🧁 Gráfico 2: Distribución de Producción")
    fig2 = px.pie(df_filtrado, names="Product", values="Value", title="Distribución de Producción")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### ⚖️ Gráfico 3: Balance energético")
    balance_df = df_filtrado[df_filtrado['Balance'].notna()]
    fig3 = px.bar(balance_df, x="Balance", y="Value", color="Balance", title="Balance Energético")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 📉 Gráfico 4: Tendencia Histórica")
    tendencia_df = df[df['Country'] == pais] if pais != 'Todos' else df
    tendencia_df = tendencia_df.groupby(['Year'])['Value'].sum().reset_index()
    fig4 = px.line(tendencia_df, x="Year", y="Value", title="Tendencia Histórica de Producción")
    st.plotly_chart(fig4, use_container_width=True)
