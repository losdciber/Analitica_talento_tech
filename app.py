#Importaciones

#Se importa Streamlit, la biblioteca principal para crear la interfaz web.
#Se importa cargar_datos desde el módulo utils.py para cargar los datos.
#Se importa cada módulo desde secciones/, cada uno contiene una función mostrar() que representa una vista o sección del dashboard.


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

#Establece el título del navegador como "Dashboard Energético".
#La opción layout="wide" hace que la app utilice el ancho completo de la pantalla, ideal para dashboards.

st.set_page_config(page_title="Dashboard Energético", layout="wide")

# Cargar datos

#Carga los datos una sola vez al inicio para ser usados en varias secciones.
#Esto optimiza el rendimiento, evitando recargas innecesarias.

df = cargar_datos()

# Estilos CSS personalizados responsivos

#Este bloque:

#Personaliza el sidebar:

#Cambia colores, tamaño de fuente, efecto hover, y estilos activos.

#Mejora visualización de gráficas Mermaid (diagrama de flujo, arquitectura, etc.), especialmente en dispositivos móviles.

#Buen toque para hacer más profesional y responsivo el dashboard.

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

# Menú lateral de navegación (Sidebar)

#Define las opciones del menú como claves de un diccionario.

#Usa st.radio para que el usuario elija una sección del dashboard.

#La clave seleccionada se guarda en seccion.

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

#Según la selección del menú, se llama la función mostrar() de cada módulo.

#Las secciones que necesitan datos (df) los reciben como parámetro.

#Otras secciones (como home, predicciones, estructura_proyecto, etc.) no necesitan el df.

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