import streamlit as st

def mostrar():
    st.title("📁 Estructura del Proyecto")

    archivo_md = "estructura_proyecto.md"

    try:
        with open(archivo_md, "r", encoding="utf-8") as file:
            contenido = file.read()
            st.markdown(contenido)
    except FileNotFoundError:
        st.error(f"❗ No se encontró el archivo `{archivo_md}`. Ejecuta primero `generar_mermaid.py` para generarlo.")
