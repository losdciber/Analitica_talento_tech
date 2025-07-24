import streamlit as st
import pandas as pd
import plotly.express as px
from utils import ejecutar_consulta

def relaciones_desempeno():
    st.title("📈 Relaciones entre Variables de Desempeño")

    # Consulta para traer los datos desde la base de datos
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

    # Transformación de los datos
    df_pivot = df.pivot_table(index=['pais', 'anio'], 
                              columns='producto', 
                              values='valor', 
                              aggfunc='sum').reset_index()

    # Opciones de columnas numéricas disponibles
    columnas_numericas = df_pivot.select_dtypes(include='number').columns.tolist()

    if len(columnas_numericas) < 2:
        st.warning("Se requieren al menos dos variables numéricas para analizar.")
        return

    # Selección de variables por el usuario
    var_x = st.selectbox("Selecciona la variable del eje X:", columnas_numericas)
    var_y = st.selectbox("Selecciona la variable del eje Y:", [col for col in columnas_numericas if col != var_x])

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

    # Cálculo de correlación
    correlacion = df_pivot[[var_x, var_y]].corr().iloc[0, 1]
    st.subheader("🔍 Análisis de Correlación")
    st.markdown(f"""
    El coeficiente de correlación de Pearson entre **{var_x}** y **{var_y}** es: **{correlacion:.2f}**

    - Un valor cercano a +1 indica una fuerte correlación positiva.
    - Un valor cercano a -1 indica una fuerte correlación negativa.
    - Un valor cercano a 0 indica una relación débil o inexistente.
    """)

    # Descripción del gráfico
    st.markdown("""
    ---
    ### 📊 Detalles del Gráfico

    **Tipo de gráfico**: Gráfico de dispersión (scatter plot)  
    **Qué muestra**: Este gráfico permite visualizar la relación entre dos variables numéricas seleccionadas.  
    Cada punto representa un país en un año específico.  
    Al analizar la tendencia de los puntos, puedes identificar relaciones lineales o patrones de comportamiento energético entre variables como consumo, producción o emisiones.
    """)

# Llamar la función si se ejecuta directamente
if __name__ == "__main__":
    relaciones_desempeno()
