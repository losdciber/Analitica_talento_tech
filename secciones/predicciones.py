import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sklearn.linear_model import LinearRegression
from prophet import Prophet
import streamlit as st
import plotly.graph_objects as go
from utils import obtener_emisiones_co2

def agregar_ruido(predicciones, escala=0.03):
    ruido = np.random.normal(loc=0, scale=escala * np.abs(predicciones))
    return predicciones + ruido

def mostrar(df=None):
    st.title("🌿 Explorador de Emisiones de CO₂")

    if df is None:
        df = obtener_emisiones_co2()

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)

    first_year = df['Year'].min()
    sectores = df['Sector'].unique()

    # — Panel lateral: simple y claro —
    st.sidebar.header("🔧 Personaliza tu vista")
    sector = st.sidebar.selectbox("📍 Elige un sector", sectores)

    st.sidebar.subheader("📅 Escoge hasta qué año predecir")
    col1, col2 = st.sidebar.columns(2)
    mostrar_2030 = col1.button(" Ver hasta 2030")
    mostrar_2050 = col2.button(" Ver hasta 2050")

    # Año de corte según el botón presionado
    if mostrar_2050:
        last_year = 2050
    else:
        last_year = 2030  # Por defecto o si se pulsa 2030

    anio_inicio = first_year
    anio_fin = last_year
    years_to_predict = np.arange(2023, last_year + 1)

    modelos = st.sidebar.multiselect(
        "🔮 ¿Qué métodos de predicción quieres ver?",
        ['Lineal', 'Prophet'],
        default=['Lineal', 'Prophet']
    )
    ruido_escala = st.sidebar.slider(
        "🎲 Añadir realismo (subidas y bajadas)",
        min_value=0.0, max_value=0.1, value=0.03,
        help="Esto imita los cambios inesperados que ocurren en la realidad"
    )

    # Predicciones
    resultados = {}
    for sec in sectores:
        df_sec = df[df['Sector'] == sec]
        X = df_sec['Year'].values.reshape(-1, 1)
        y = df_sec['Value'].values

        # Regresión Lineal
        model_lin = LinearRegression()
        model_lin.fit(X, y)
        pred_lin = model_lin.predict(years_to_predict.reshape(-1, 1))
        pred_lin = agregar_ruido(pred_lin, escala=ruido_escala)

        # Prophet
        df_prophet = df_sec.rename(columns={'Year': 'ds', 'Value': 'y'})
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds'], format='%Y')
        model_prophet = Prophet(yearly_seasonality=False)
        model_prophet.fit(df_prophet)
        future = pd.DataFrame({'ds': pd.date_range(start='2023-01-01', end=f'{last_year}-01-01', freq='YS')})
        forecast = model_prophet.predict(future)
        pred_prophet = agregar_ruido(forecast['yhat'].values, escala=ruido_escala)

        resultados[sec] = {
            'Lineal': pd.DataFrame({'Year': years_to_predict, 'Value': pred_lin}),
            'Prophet': pd.DataFrame({'Year': years_to_predict, 'Value': pred_prophet})
        }

    df_real = df[(df['Sector'] == sector) & (df['Year'] >= anio_inicio) & (df['Year'] <= anio_fin)]

    # Tabs con explicaciones
    tabs = st.tabs(["📊 Datos Reales", "📈 Predicciones"])

    with tabs[0]:
        st.subheader(f"📌 Datos Históricos del Sector: {sector}")
        st.markdown("🔍 Estos son los valores reales de emisiones de CO₂ registrados entre los años seleccionados.")
        st.dataframe(df_real[['Year', 'Value']].reset_index(drop=True), use_container_width=True)

    with tabs[1]:
        st.subheader("🔮 Explorando el Futuro")
        st.markdown("Aquí puedes comparar cómo diferentes métodos intentan **predecir el futuro** con base en los datos históricos.")

        if 'Lineal' in modelos:
            st.markdown("### 📈 Predicción Lineal")
            st.markdown("""
            La regresión lineal traza una línea recta que mejor se ajusta a los datos históricos.
            Es simple y útil para observar tendencias generales.
            """)
            df_pred_lin = resultados[sector]['Lineal']
            df_pred_lin_filtrado = df_pred_lin[(df_pred_lin['Year'] >= anio_inicio) & (df_pred_lin['Year'] <= anio_fin)]
            st.dataframe(df_pred_lin_filtrado, use_container_width=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_real['Year'], y=df_real['Value'],
                mode='lines+markers', name='Datos reales', line=dict(color='black', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df_pred_lin_filtrado['Year'], y=df_pred_lin_filtrado['Value'],
                mode='lines+markers', name='Predicción Lineal', line=dict(color='blue')
            ))
            fig.update_layout(
                title="Comparativa con Modelo Lineal",
                xaxis_title="Año",
                yaxis_title="Mt CO₂",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        if 'Prophet' in modelos:
            st.markdown("### 🔮 Predicción con Prophet")
            st.markdown("""
            Prophet es un modelo desarrollado por Facebook, muy bueno para datos con patrones a lo largo del tiempo.
            Aquí intenta predecir el futuro usando años anteriores como guía.
            """)
            df_pred_prophet = resultados[sector]['Prophet']
            df_pred_prophet_filtrado = df_pred_prophet[(df_pred_prophet['Year'] >= anio_inicio) & (df_pred_prophet['Year'] <= anio_fin)]
            st.dataframe(df_pred_prophet_filtrado, use_container_width=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_real['Year'], y=df_real['Value'],
                mode='lines+markers', name='Datos reales', line=dict(color='black', width=2)
            ))
            fig.add_trace(go.Scatter(
                x=df_pred_prophet_filtrado['Year'], y=df_pred_prophet_filtrado['Value'],
                mode='lines+markers', name='Predicción Prophet', line=dict(color='green')
            ))
            fig.update_layout(
                title="Comparativa con Modelo Prophet",
                xaxis_title="Año",
                yaxis_title="Mt CO₂",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.info("💡 Puedes cambiar de sector, método o año desde la barra lateral. ¡Explora diferentes futuros posibles!")
