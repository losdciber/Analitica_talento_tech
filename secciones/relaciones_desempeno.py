import streamlit as st

import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from utils import obtener_emisiones_co2, obtener_datos_corr_emisiones_y_generacion

def mostrar(anio=2022):
    st.header("Relación entre desempeño y emisiones de CO₂")

    # --- SIDEBAR ---
    st.sidebar.title("Matrices disponibles")
    mostrar_matriz_confusion = st.sidebar.checkbox("Matriz de confusión")
    mostrar_matriz_correlacion = st.sidebar.checkbox("Matriz de correlación")

    # --- SLIDERS DE CLASIFICACIÓN ---
    st.subheader("Ajuste de niveles de clasificación")
    bajo_max = st.slider("Límite para 'Bajo'", 0.0, 20.0, 7.0)
    medio_max = st.slider("Límite para 'Medio'", bajo_max + 0.1, 30.0, 20.0)
    st.markdown("- 'Bajo' ≤ {:.1f}".format(bajo_max))
    st.markdown("- {:.1f} < 'Medio' ≤ {:.1f}".format(bajo_max, medio_max))
    st.markdown("- 'Alto' > {:.1f}".format(medio_max))

    # --- DATOS Y CLASIFICACIÓN ---
    df = obtener_emisiones_co2()

    def clasificar_emisiones(valor):
        if valor <= bajo_max:
            return "Bajo"
        elif valor <= medio_max:
            return "Medio"
        else:
            return "Alto"

    df_clasificado = df.copy()
    df_clasificado["Clasificación"] = df_clasificado["Value"].apply(clasificar_emisiones)

    etiquetas = {"Bajo": 0, "Medio": 1, "Alto": 2}
    df_clasificado["Etiqueta"] = df_clasificado["Clasificación"].map(etiquetas)

    # --- ENTRENAMIENTO DEL MODELO ---
    X = df_clasificado[["Value"]]
    y = df_clasificado["Etiqueta"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LogisticRegression(multi_class='ovr')
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    # --- CLASIFICACIÓN MANUAL ---
    st.subheader("Clasificador en tiempo real")
    valor_manual = st.number_input("Ingrese un valor de emisión (Mt de CO₂):", 0.0, 40.0, 10.0)
    pred_clase = modelo.predict([[valor_manual]])[0]
    clase_nombre = list(etiquetas.keys())[list(etiquetas.values()).index(pred_clase)]
    st.markdown(f"*Resultado:* El modelo predice que este valor pertenece a la categoría *{clase_nombre}*.")

    # --- MATRIZ DE CONFUSIÓN INTERACTIVA ---
    if mostrar_matriz_confusion:
        st.subheader("Matriz de confusión")
        st.markdown("""
        Esta matriz compara las predicciones del modelo con los valores reales.  
        - La diagonal muestra los aciertos.  
        - Las otras celdas muestran los errores de predicción.
        """)

        labels = ["Bajo", "Medio", "Alto"]
        z = cm.tolist()
        fig = ff.create_annotated_heatmap(z, x=labels, y=labels, colorscale='Blues')
        fig.update_layout(height=350, width=350, margin=dict(t=40, l=40, b=40))
        st.plotly_chart(fig, use_container_width=False)
        st.write("Precisión del modelo: {:.2f}%".format(modelo.score(X_test, y_test) * 100))

    # --- MATRIZ DE CORRELACIÓN INTERACTIVA CON ANÁLISIS ---
    if mostrar_matriz_correlacion:
        st.subheader("Matriz de correlación")
        st.markdown("""
        Esta matriz muestra cómo se relacionan entre sí las siguientes variables:
        - *EmisionesFosiles*: emisiones por combustibles fósiles.
        - *GeneracionCarbon*: generación eléctrica por carbón.
        - *GeneracionGas*: generación por gas natural.
        """)

        df_corr = obtener_datos_corr_emisiones_y_generacion()

        if not df_corr.empty:
            matriz_corr = df_corr[['EmisionesFosiles', 'GeneracionCarbon', 'GeneracionGas']].corr()

            fig = ff.create_annotated_heatmap(
                z=matriz_corr.values.round(2),
                x=list(matriz_corr.columns),
                y=list(matriz_corr.index),
                colorscale='RdBu',
                showscale=True,
                reversescale=True,
                zmin=-1,
                zmax=1,
                annotation_text=matriz_corr.round(2).astype(str).values
            )
            fig.update_layout(height=400, width=400, margin=dict(t=40, l=40, b=40))
            st.plotly_chart(fig, use_container_width=False)

            st.markdown("""
            *Leyenda de variables:*

            - *EmisionesFosiles*: Emisiones de CO₂ de fuentes fósiles (carbón, gas, petróleo).
            - *GeneracionCarbon*: Generación eléctrica usando carbón.
            - *GeneracionGas*: Generación eléctrica usando gas natural.

            Estas variables están correlacionadas para entender si *más generación* implica *más emisiones* o no.
            """)

            # Análisis automático
            st.subheader("Análisis automático de relaciones")

            for i in matriz_corr.columns:
                for j in matriz_corr.columns:
                    if i != j:
                        corr = matriz_corr.loc[i, j]
                        interpretacion = ""
                        if abs(corr) >= 0.8:
                            intensidad = "muy fuerte"
                        elif abs(corr) >= 0.5:
                            intensidad = "moderada"
                        elif abs(corr) >= 0.3:
                            intensidad = "débil"
                        else:
                            intensidad = "muy débil o nula"

                        tipo = "positiva (directamente proporcional)" if corr > 0 else "negativa (inversamente proporcional)" if corr < 0 else "sin relación"
                        st.markdown(f"- *{i} vs {j}*: correlación de {corr:.2f} → relación {intensidad} y {tipo}.")
        else:
            st.warning("No hay datos suficientes para calcular la matriz.")