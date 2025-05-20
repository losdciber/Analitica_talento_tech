
import streamlit as st
from utils import cargar_datos
from secciones import diagnostico_nacional, tendencia_mensual, comparativos_internacionales

st.set_page_config(page_title="Dashboard Energético", layout="wide")
st.title("Dashboard Energético Interactivo")

# Cargar datos
df = cargar_datos()

# Sidebar global
with st.sidebar:
    st.title("🔌 Dashboard Energético")
    paises = ['Todos'] + sorted(df['Country'].dropna().unique())
    pais = st.selectbox("🌍 Selecciona un país", paises)

    anios = sorted(df['Year'].dropna().unique())
    if anios:
        anio = st.selectbox("📅 Selecciona un año", anios, index=len(anios) - 1)
    else:
        st.warning("⚠️ No hay años disponibles.")
        st.stop()

    seccion = st.radio("📁 Secciones del Dashboard", [
        "Diagnóstico Nacional",
        "Comparativos Internacionales",
        "Tendencia Mensual"
    ])

# Navegación
if seccion == "Diagnóstico Nacional":
    diagnostico_nacional.mostrar(pais, anio, df)
elif seccion == "Comparativos Internacionales":
    comparativos_internacionales.mostrar(pais, anio, df)
elif seccion == "Tendencia Mensual":
    tendencia_mensual.mostrar(pais, anio)
