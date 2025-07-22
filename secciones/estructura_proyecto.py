import streamlit as st

def mostrar():
    st.title("Estructura del Proyecto")
    st.markdown("""
    Esta sección presenta la estructura general del proyecto.

    **Carpetas principales:**
    - `utils.py`: Funciones auxiliares para cargar datos u otras tareas comunes.
    - `secciones/`: Módulos independientes para cada sección del dashboard.
    - `data/`: Fuente de datos crudos o procesados.
    - `app.py`: Punto de entrada del dashboard.
    
    **Estrategia modular:** cada sección se actualiza de forma independiente, facilitando mantenimiento, escalabilidad y lectura del código.

    **Optimización:** Adaptado para escritorio y dispositivos móviles para una visualización ágil.
    """)
