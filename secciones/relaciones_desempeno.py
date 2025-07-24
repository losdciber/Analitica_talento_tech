import streamlit as st
import plotly.express as px

def mostrar(df):
    st.title("📈 Relaciones entre Producción, PIB y Empleo")

    # Validar columnas necesarias
    columnas_necesarias = ["PIB", "Producción Total", "Empleo Energía", "País"]
    if not all(col in df.columns for col in columnas_necesarias):
        st.error("El DataFrame no contiene las columnas necesarias: " + ", ".join(columnas_necesarias))
        return

    # Gráfico 1: Producción vs PIB
    fig1 = px.scatter(
        df,
        x="PIB",
        y="Producción Total",
        color="País",
        size="Empleo Energía",
        hover_name="País",
        title="Relación entre PIB y Producción Total de Energía"
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
    **Tipo de gráfico:** Dispersión (scatter plot).  
    **Qué muestra:** Visualiza la relación entre el Producto Interno Bruto (PIB) y la Producción Total de Energía.  
    Cada punto representa un país, y su tamaño refleja el nivel de empleo en el sector energético.
    """)

    # Gráfico 2: Empleo vs Producción
    fig2 = px.scatter(
        df,
        x="Empleo Energía",
        y="Producción Total",
        color="País",
        hover_name="País",
        title="Relación entre Empleo en Energía y Producción Total"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
    **Tipo de gráfico:** Dispersión.  
    **Qué muestra:** Examina si un mayor empleo en el sector energético se asocia con una mayor producción total de energía.
    """)

    # Gráfico 3: PIB vs Empleo
    fig3 = px.scatter(
        df,
        x="PIB",
        y="Empleo Energía",
        color="País",
        hover_name="País",
        title="Relación entre PIB y Empleo en Energía"
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    **Tipo de gráfico:** Dispersión.  
    **Qué muestra:** Permite analizar si existe una correlación entre el crecimiento económico (PIB) y el empleo en el sector energético por país.
    """)

