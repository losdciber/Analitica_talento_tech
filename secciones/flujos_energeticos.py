import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import ejecutar_consulta

def mostrar():
    st.subheader("🔄 Diagramas de Flujo Energético")

    def construir_sankey(df, titulo):
        df = df[df['value'] > 0]
        etiquetas = pd.unique(df[['source', 'target']].values.ravel()).tolist()
        df['source_id'] = df['source'].apply(lambda x: etiquetas.index(x))
        df['target_id'] = df['target'].apply(lambda x: etiquetas.index(x))

        colores_fuentes = ["#4B8BBE", "#5DADE2", "#76D7C4", "#82E0AA", "#2ECC71", "#48C9B0"]
        colores_destinos = ["#F5B041", "#F1948A", "#E67E22", "#EC7063", "#CD6155"]
        colores = []

        for etiqueta in etiquetas:
            if etiqueta in df['source'].values:
                color = colores_fuentes[len(colores) % len(colores_fuentes)]
            else:
                color = colores_destinos[len(colores) % len(colores_destinos)]
            colores.append(color)

        textos = [
            f"{df.iloc[i]['source']} → {df.iloc[i]['target']}<br>{df.iloc[i]['value']:.2f} PJ"
            for i in range(len(df))
        ]

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                label=etiquetas,
                line=dict(color="gray", width=0.5),
                color=colores
            ),
            link=dict(
                source=df['source_id'],
                target=df['target_id'],
                value=df['value'],
                color="rgba(160,160,160,0.3)",
                customdata=textos,
                hovertemplate='%{customdata}<extra></extra>'
            )
        )])
        fig.update_layout(title_text=titulo, font_size=13, height=500)
        return fig

    tab1, tab2 = st.tabs(["🔷 Flujo Primario", "🟠 Flujo Secundario"])

    # TAB 1: FLUJO PRIMARIO
    with tab1:
        df_primario = ejecutar_consulta("SELECT * FROM view_sankey_flujo_primario;")

        with st.expander("🔎 Filtros del Flujo Primario", expanded=True):
            paises = sorted(df_primario['Country'].unique())
            pais = st.selectbox("Selecciona el país", paises, key="pais_primario")
            anios = sorted(df_primario[df_primario['Country'] == pais]['Year'].unique())
            anio = st.selectbox("Selecciona el año", anios, key="anio_primario")

        df_filtrado = df_primario[
            (df_primario['Country'] == pais) & 
            (df_primario['Year'] == anio)
        ]
        df_filtrado = df_filtrado.groupby(['source', 'target'], as_index=False)['value'].sum()

        st.plotly_chart(
            construir_sankey(df_filtrado, f"Flujo Primario de Energía ({pais}, {anio})"),
            use_container_width=True
        )

        st.markdown("""
        **Tipo de gráfico:** Diagrama de Sankey  
        **Qué muestra:** Este diagrama representa el flujo de energía **primaria** desde las fuentes originales (como petróleo, gas, carbón o renovables) hacia diferentes usos o sectores. Las **anchuras de las líneas** indican la magnitud del flujo energético en petajulios (PJ), facilitando la visualización de cómo se distribuye y transforma la energía en un país durante un año específico.
        """)

        st.markdown("### 📋 Tabla de datos del flujo primario")
        st.dataframe(df_filtrado.rename(columns={
            "source": "Fuente",
            "target": "Destino",
            "value": "Valor (PJ)"
        }))

        with st.expander("🧠 Interpretación del Flujo"):
            total = df_filtrado['value'].sum()
            top_flujos = df_filtrado.sort_values('value', ascending=False).head(3)

            st.markdown(f"""
            - En el año **{anio}**, **{pais}** tuvo un flujo energético total de aproximadamente **{total:,.2f} PJ**.
            - Los principales flujos de energía fueron:
            """)
            for _, row in top_flujos.iterrows():
                st.markdown(f"  • **{row['source']} → {row['target']}**: {row['value']:,.2f} PJ")

    # TAB 2: FLUJO SECUNDARIO
    with tab2:
        df_secundario = ejecutar_consulta("SELECT * FROM view_sankey_flujo_secundario;")

        with st.expander("🔎 Filtros del Flujo Secundario", expanded=True):
            paises = sorted(df_secundario['Country'].unique())
            pais = st.selectbox("Selecciona el país", paises, key="pais_secundario")
            anios = sorted(df_secundario[df_secundario['Country'] == pais]['Year'].unique())
            anio = st.selectbox("Selecciona el año", anios, key="anio_secundario")

        df_filtrado = df_secundario[
            (df_secundario['Country'] == pais) & 
            (df_secundario['Year'] == anio)
        ]
        df_filtrado = df_filtrado.groupby(['source', 'target'], as_index=False)['value'].sum()

        st.plotly_chart(
            construir_sankey(df_filtrado, f"Flujo Secundario de Energía ({pais}, {anio})"),
            use_container_width=True
        )

        st.markdown("""
        **Tipo de gráfico:** Diagrama de Sankey  
        **Qué muestra:** Este gráfico muestra el flujo de energía **secundaria**, es decir, cómo la energía ya transformada (por ejemplo, electricidad o combustibles refinados) se distribuye entre distintos sectores como transporte, industria o residencial. Las líneas conectan los orígenes con los destinos y su grosor representa el volumen energético en petajulios (PJ).
        """)

        st.markdown("### 📋 Tabla de datos del flujo secundario")
        st.dataframe(df_filtrado.rename(columns={
            "source": "Fuente",
            "target": "Destino",
            "value": "Valor (PJ)"
        }))

        with st.expander("🧠 Interpretación del Flujo"):
            total = df_filtrado['value'].sum()
            top_flujos = df_filtrado.sort_values('value', ascending=False).head(3)

            st.markdown(f"""
            - En el año **{anio}**, **{pais}** tuvo un flujo energético total de aproximadamente **{total:,.2f} PJ**.
            - Los principales flujos de energía fueron:
            """)
            for _, row in top_flujos.iterrows():
                st.markdown(f"  • **{row['source']} → {row['target']}**: {row['value']:,.2f} PJ")
