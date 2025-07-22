import streamlit as st 
from utils import cargar_datos
from secciones import (
    home,
    matriz_energetica,
    consumo_energetico,
    matriz_electrica,
    comparativos_internacionales,
    emisiones_co2,
    relaciones_desempeno,
    predicciones,
    flujos_energeticos,
    estructura_proyecto  # nueva sección
)

# Configurar la página para pantalla amplia
st.set_page_config(page_title="Dashboard Energético", layout="wide")

# Cargar datos una sola vez
df = cargar_datos()

# Estilos CSS personalizados responsivos
st.markdown("""
    <style>
    /* Estilo sidebar */
    [data-testid="stSidebar"] {
        background-color: #f2f2f2;
    }
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #000000;
        padding-bottom: 10px;
    }
    .sidebar-radio label {
        font-size: 17px;
        padding: 8px 12px;
        border-radius: 6px;
        display: block;
        margin-bottom: 5px;
        color: #000000;
        transition: background-color 0.3s ease;
    }
    .sidebar-radio label:hover {
        background-color: #d6d6d6;
        color: #000000;
    }
    .sidebar-radio input:checked + div {
        background-color: #cccccc !important;
        color: #000000 !important;
    }

    /* Responsividad para Mermaid en móviles */
    .mermaid svg {
        width: 100% !important;
        height: auto !important;
    }

    @media only screen and (min-width: 768px) {
        .mermaid svg {
            width: 80% !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar de navegación
menu_opciones = {
    "Home": "Home",
    "Matriz Energética": "Matriz Energética",
    "Consumo Energético": "Consumo Energético",
    "Matriz Eléctrica": "Matriz Eléctrica",
    "Comparativos Internacionales": "Comparativos Internacionales",
    "Emisiones de CO2": "Emisiones de CO2",
    "Análisis de Relaciones y Desempeño": "Análisis de Relaciones y Desempeño",
    "Predicciones": "Predicciones",
    "Flujos Energéticos": "Flujos Energéticos",
    "Estructura del Proyecto": "Estructura del Proyecto"  # agregado al menú
}

with st.sidebar:
    st.markdown('<div class="sidebar-title">Menú de navegación</div>', unsafe_allow_html=True)
    seccion = st.radio(
        "",
        list(menu_opciones.keys()),
        format_func=lambda x: menu_opciones[x],
        key="navegacion"
    )

# Enrutamiento por sección
if seccion == "Home":
    home.mostrar()
elif seccion == "Matriz Energética":
    matriz_energetica.mostrar(df)
elif seccion == "Consumo Energético":
    consumo_energetico.mostrar(df)
elif seccion == "Matriz Eléctrica":
    matriz_electrica.mostrar(df)
elif seccion == "Comparativos Internacionales":
    comparativos_internacionales.mostrar(df)
elif seccion == "Emisiones de CO2":
    emisiones_co2.mostrar(df)
elif seccion == "Análisis de Relaciones y Desempeño":
    relaciones_desempeno.mostrar(df)
elif seccion == "Predicciones":
    predicciones.mostrar()
elif seccion == "Flujos Energéticos":
    flujos_energeticos.mostrar()
elif seccion == "Estructura del Proyecto":
    estructura_proyecto.mostrar()  # función que visualizará el diagrama
