
import streamlit as st
import plotly.express as px

def mostrar(pais, anio, df):
    st.subheader(f"Diagnóstico Energético - {pais} ({anio})")

    df_filtrado = df[df['Year'] == anio]
    if pais != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Country'] == pais]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏭 Gráfico 1: Producción por Fuente")
        st.plotly_chart(
            px.bar(df_filtrado, x="Value", y="Product", orientation="h", title="Producción por Fuente"),
            use_container_width=True
        )

        st.markdown("### ⚖️ Gráfico 2: Balance energético")
        st.plotly_chart(
            px.histogram(df_filtrado, x="Balance", y="Value", title="Balance Energético"),
            use_container_width=True
        )

    with col2:
        st.markdown("### 🧁 Gráfico 3: Distribución de Producción")
        st.plotly_chart(
            px.pie(df_filtrado, names="Product", values="Value", title="Distribución de Producción"),
            use_container_width=True
        )

        st.markdown("### 📉 Gráfico 4: Tendencia Histórica")
        tendencia_df = df[df['Country'] == pais] if pais != 'Todos' else df
        st.plotly_chart(
            px.line(tendencia_df, x="Year", y="Value", title="Tendencia Histórica"),
            use_container_width=True
        )
