import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from utils import clasificar_y_filtrar_productos, obtener_produccion_mensual

def mostrar(df):
    st.title("🌍 Comparativos Internacionales")

    # 🎛️ Filtros generales
    with st.sidebar:
        st.markdown("### 🎛️ Filtros - Comparativos Internacionales")

        paises = ['Todos'] + sorted(df['Country'].dropna().unique())
        pais = st.selectbox("🌍 País", paises)

        anios = sorted(df['Year'].dropna().unique())
        anio = st.selectbox("📅 Año", anios, index=len(anios) - 1)

    # Tabs principales
    tab1, tab2 = st.tabs([
        "📊 1. Participación por País (Año actual)",
        "🌍 2. Evolución % Renovable vs No Renovable (Multipaís)"
    ])

    # === TAB 1 ===
    with tab1:
        st.markdown("### 🧭 Participación Renovable vs No Renovable por País")

        productos_excluir = [
            'Electricity', 'Total Combustible Fuels',
            'Total Renewables (Hydro, Geo, Solar, Wind, Other)',
            'Not Specified', 'Data is estimated for this month'
        ]
        productos_renovables = [
            'Hydro', 'Wind', 'Geothermal', 'Combustible Renewables', 'Solar', 'Other Renewables'
        ]

        df_filtrado = df[~df['Product'].isin(productos_excluir)].copy()
        df_filtrado['Energy_Type'] = df_filtrado['Product'].apply(
            lambda x: 'Renewable' if x in productos_renovables else 'Non-Renewable'
        )
        df_year = df_filtrado[df_filtrado['Year'] == anio]

        if not df_year.empty:
            df_grouped = df_year.groupby(['Country', 'Energy_Type'])['Value'].sum().reset_index()
            df_total = df_grouped.groupby('Country')['Value'].sum().reset_index(name='Total_Value')
            df_grouped = df_grouped.merge(df_total, on='Country')
            df_grouped['Percentage'] = df_grouped['Value'] / df_grouped['Total_Value'] * 100
            df_pivot = df_grouped.pivot(index='Country', columns='Energy_Type', values='Percentage').fillna(0)

            if 'Renewable' in df_pivot.columns and 'Non-Renewable' in df_pivot.columns:
                df_pivot = df_pivot[['Renewable', 'Non-Renewable']]
                colores = ['#2ca02c', '#d62728']
            elif 'Renewable' in df_pivot.columns:
                df_pivot = df_pivot[['Renewable']]
                colores = ['#2ca02c']
            elif 'Non-Renewable' in df_pivot.columns:
                df_pivot = df_pivot[['Non-Renewable']]
                colores = ['#d62728']
            else:
                st.warning("No hay datos suficientes para mostrar el gráfico.")
                return

            df_pivot = df_pivot.sort_values(by='Renewable', ascending=False) if 'Renewable' in df_pivot.columns else df_pivot

            fig, ax = plt.subplots(figsize=(11, 5))
            df_pivot.plot(kind='bar', stacked=True, color=colores, ax=ax)
            ax.set_title(f'Participación porcentual de energía por país - {anio}')
            ax.set_ylabel('Porcentaje (%)')
            ax.set_ylim(0, 100)
            ax.legend(title='Tipo de Energía', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.xticks(rotation=90, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning(f"No hay datos para el año {anio}.")

    # === TAB 2 ===
    with tab2:
        st.markdown("### 🌍 Evolución de Participación % Renovable vs No Renovable (Multipaís)")

        df_energy = clasificar_y_filtrar_productos(obtener_produccion_mensual(), pais='Todos')
        df_energy['Year'] = pd.to_datetime(df_energy['Time'], format='%B %Y').dt.year
        paises_disponibles = sorted(df_energy['Country'].dropna().unique())

        if 'paises_seleccionados_multi' not in st.session_state:
            st.session_state.paises_seleccionados_multi = paises_disponibles[:6]

        # 🔘 Botones de selección
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("❌ Deseleccionar todos"):
                st.session_state.paises_seleccionados_multi = []

        with col2:
            if st.button("🌐 Seleccionar OECD"):
                st.session_state.paises_seleccionados_multi = [p for p in paises_disponibles if 'oecd' in p.lower()]

        with col3:
            if st.button("🌎 Latinoamérica"):
                latinoamericanos = [
                    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Costa Rica", "Cuba", "Dominican Republic",
                    "Ecuador", "El Salvador", "Guatemala", "Honduras", "Mexico", "Nicaragua", "Panama", "Paraguay",
                    "Peru", "Uruguay", "Venezuela"
                ]
                st.session_state.paises_seleccionados_multi = [p for p in paises_disponibles if p in latinoamericanos]

        with col4:
            if st.button("🏆 Países representativos"):
                representativos = [
                    "Colombia","United States", "People's Republica of China", "India", "Germany", "France", "Brazil", "Japan", "United Kingdom", "Russia", "Canada, Spain, Korea"
                ]
                st.session_state.paises_seleccionados_multi = [p for p in paises_disponibles if p in representativos][:12]

        # 🎛️ Selector de países
        paises_seleccionados = st.multiselect(
            "🌐 Selecciona hasta 12 países para comparar",
            options=paises_disponibles,
            default=st.session_state.paises_seleccionados_multi,
            max_selections=12,
            key='paises_seleccionados_multi'
        )

        df_multi = df_energy[df_energy['Country'].isin(paises_seleccionados)]

        if df_multi.empty:
            st.warning("No hay datos para los países seleccionados.")
            return

        df_total = df_multi.groupby(['Country', 'Year'])['Value'].sum().reset_index(name='Total_Value')
        df_group = df_multi.groupby(['Country', 'Year', 'Energy_Type'])['Value'].sum().reset_index()
        df_group = df_group.merge(df_total, on=['Country', 'Year'])
        df_group['Percentage'] = df_group['Value'] / df_group['Total_Value'] * 100

        df_group['Energy_Type'] = pd.Categorical(df_group['Energy_Type'], categories=["Renewable", "Non-Renewable"])
        df_group = df_group.sort_values(by=['Country', 'Year', 'Energy_Type'])

        num_paises = len(paises_seleccionados)
        wrap_dinamico = 2 if num_paises <= 4 else 4
        altura_dinamica = min(600, 300 + 160 * ((num_paises - 1) // wrap_dinamico + 1))

        fig_multi = px.bar(
            df_group,
            x='Year',
            y='Percentage',
            color='Energy_Type',
            facet_col='Country',
            facet_col_wrap=wrap_dinamico,
            barmode='stack',
            labels={"Percentage": "Porcentaje (%)", "Energy_Type": "Tipo"},
            category_orders={"Energy_Type": ["Renewable", "Non-Renewable"]},
            color_discrete_map={"Renewable": "#2ca02c", "Non-Renewable": "#d62728"}
        )

        fig_multi.update_layout(
            height=altura_dinamica,
            title="Comparativo de Participación Renovable vs No Renovable (Multipaís)",
            yaxis_range=[0, 100],
            showlegend=True
        )

        st.plotly_chart(fig_multi, use_container_width=True)



