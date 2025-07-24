import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ejecutar_consulta

def relaciones_desempeno():
    st.title("📈 Relaciones entre Variables de Desempeño")

    # Consulta SQL para traer los datos desde la base de datos
    query = """
    SELECT 
        pais, anio, tipo_energia, tipo_fuente, producto, valor
    FROM energia
    WHERE valor IS NOT NULL
    """
    df = ejecutar_consulta(query)

    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return

    # Reorganizar los datos para tener variables numéricas como columnas
    df_pivot = df.pivot_table(
        index=['pais', 'anio'], 
        columns='producto', 
        values='valor', 
        aggfunc='sum'
    ).reset_index()

    # Extraer columnas numéricas
    columnas_numericas = df_pivot.select_dtypes(include='number').columns.tolist()

    if len(columnas_numericas) < 2:
        st.warning("Se requieren al menos dos variables numéricas para hacer el análisis.")
        return

    # Selección de variables por parte del usuario
    var_x = st.selectbox("📌 Selecciona la variable para el eje X:", columnas_numericas)
    var_y = st.selectbox("📌 Selecciona la variable para el eje Y:", [col for col in columnas_numericas if col != var_x])

    # Gráfico de dispersión
    fig = px.scatter(
        df_pivot,
        x=var_x,
        y=var_y,
        color="pais",
        hover_data=["anio"],
        title=f"Relación entre {var_x} y {var_y}"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Cálculo del coeficiente de correlación
    correlacion = df_pivot[[var_x, var_y]].corr().iloc[0, 1]
    st.subheader("🔍 Análisis de Correlación")
    st.markdown(f"""
    El coeficiente de correlación de Pearson entre **{var_x}** y **{var_y}** es: **{correlacion:.2f}**

    - **+1**: Correlación perfectamente positiva  
    - **-1**: Correlación perfectamente negativa  
    - **0**: Sin correlación lineal  
    """)

    # Descripción del gráfico
    st.markdown("""
    ---
    ### ℹ️ Detalles del Gráfico

    - **Tipo de gráfico**: Dispersión (scatter plot)  
    - **Qué representa**: Muestra la relación entre dos variables numéricas.  
    - **Cada punto**: Representa un país en un año determinado.  
    - **Utilidad**: Detectar patrones, tendencias, y relaciones entre producción, consumo o emisiones de energía.
    """)

# Permite ejecutar la app directamente con `python Relaciones_desempeno.py`
if __name__ == "__main__":
    relaciones_desempeno()
