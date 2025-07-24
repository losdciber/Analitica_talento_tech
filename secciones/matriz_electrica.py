import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from utils import clasificar_y_filtrar_productos, obtener_produccion_mensual, ejecutar_consulta
import sqlite3

def mostrar(df_global):
    st.title("🔌 Matriz Eléctrica")

    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Filtros - Matriz Eléctrica")

        paises = ['Todos'] + sorted(df_global['Country'].dropna().unique())
        pais = st.selectbox("🌍 Selecciona un país", paises)

        tipos_energia = {
            'Renovables y No Renovables': 'ambas',
            'Solo Renovables': 'renovables',
            'Solo No Renovables': 'no_renovables'
        }
        tipo_energia = st.selectbox("🔋 Tipo de Energía", list(tipos_energia.keys()))
        modo = tipos_energia[tipo_energia]

    # Cargar datos
    df_energy = obtener_produccion_mensual()
    df_energy['Time'] = pd.to_datetime(df_energy['Time'], format='%B %Y')
    df_energy['YearMonth'] = df_energy['Time'].dt.strftime('%Y-%m')

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 1. Composición de la Matriz Eléctrica",
        "📈 2. Tendencias Matriz Eléctrica",
        "📉 3. % Participación Renovable-No Renovable",
        "📊 4. Desglose Renovables vs No Renovables"
    ])

    # 📌 TAB 1: Composición
    with tab1:
        st.markdown("### 📌 Participación Total de Renovables vs No Renovables")

        df_compo = clasificar_y_filtrar_productos(df_energy, pais=pais)
        df_resumen = df_compo.groupby("Energy_Type")["Value"].sum().reset_index()
        df_resumen["Porcentaje"] = df_resumen["Value"] / df_resumen["Value"].sum() * 100

        fig_comp = px.pie(
            df_resumen,
            names="Energy_Type",
            values="Value",
            hole=0.3,
            color="Energy_Type",
            color_discrete_map={"Renewable": "#2ca02c", "Non-Renewable": "#d62728"},
        )
        fig_comp.update_traces(textposition='inside', textinfo='percent+label')
        fig_comp.update_layout(
            title=f"Composición de la Matriz Eléctrica - {pais if pais != 'Todos' else 'Global'}",
            legend_title="Tipo de Energía"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        st.caption("🧁 Este gráfico de torta muestra la proporción total de energía renovable y no renovable en la matriz eléctrica seleccionada.")

    # 📈 TAB 2: Tendencias
    with tab2:
        df_filtrado = clasificar_y_filtrar_productos(df_energy, pais=pais, tipo_energia=modo)
        df_monthly = df_filtrado.groupby(['YearMonth', 'Energy_Type'])['Value'].sum().reset_index()

        if df_monthly.empty:
            st.warning(f"No hay datos disponibles para {pais} y tipo {tipo_energia}")
            return

        st.markdown("### 📈 Generación Eléctrica Mensual")

        fig_line = px.line(
            df_monthly,
            x='YearMonth',
            y='Value',
            color='Energy_Type',
            markers=True,
            labels={"Value": "Generación (GWh)", "Energy_Type": "Tipo"},
            color_discrete_map={"Renewable": "#2ca02c", "Non-Renewable": "#d62728"},
            template='simple_white'
        )
        fig_line.update_traces(line=dict(width=3), marker=dict(size=6))
        fig_line.update_layout(
            xaxis_title="Mes",
            yaxis_title="Generación (GWh)",
            legend_title="Tipo de Energía",
            xaxis=dict(tickangle=-45, showline=True, linewidth=1, linecolor='black'),
            yaxis=dict(showline=True, linewidth=1, linecolor='black'),
            font=dict(family="Arial", size=13),
            plot_bgcolor='white',
            margin=dict(t=60, l=40, r=30, b=60),
            height=450
        )
        st.plotly_chart(fig_line, use_container_width=True)
        st.caption("📈 Este gráfico de líneas muestra la evolución mensual de la generación de electricidad según el tipo de fuente energética.")

    # 📉 TAB 3: Porcentaje anual
    with tab3:
        df_energy_filtered = clasificar_y_filtrar_productos(df_energy, pais=pais)
        df_energy_filtered['Year'] = df_energy_filtered['Time'].dt.year

        df_total_by_year = df_energy_filtered.groupby('Year')['Value'].sum().reset_index(name='Total_Year_Value')
        df_agg = df_energy_filtered.groupby(['Year', 'Energy_Type'])['Value'].sum().reset_index()
        df_agg = df_agg.merge(df_total_by_year, on='Year')
        df_agg['Percentage'] = df_agg['Value'] / df_agg['Total_Year_Value'] * 100

        fig_porc = px.bar(
            df_agg, x='Year', y='Percentage', color='Energy_Type',
            barmode='stack', labels={"Percentage": "Porcentaje (%)", "Energy_Type": "Tipo"},
            title=f"% Participación de Energía Renovable vs No Renovable - {pais if pais != 'Todos' else 'Global'}",
            color_discrete_map={"Renewable": "#2ca02c", "Non-Renewable": "#d62728"}
        )
        fig_porc.update_layout(yaxis_range=[0, 100], xaxis_title="Año", yaxis_title="Porcentaje (%)", legend_title="Tipo de Energía")
        st.plotly_chart(fig_porc, use_container_width=True)
        st.caption("📊 Este gráfico de barras apiladas muestra la participación porcentual anual de fuentes renovables y no renovables en la generación total.")

    # 📊 TAB 4: Comparativo Renovables vs No Renovables
    with tab4:
        st.markdown("### ⚖️ Desglose de Energías Renovables y No Renovables")

        conn = ejecutar_consulta("SELECT 1")
        conn = conn.connection if hasattr(conn, 'connection') else sqlite3.connect("data/analisis_energetico.db")

        pais_sql = pais.replace("'", "''")
        pais_filter = "" if pais == 'Todos' else f"AND Country = '{pais_sql}'"

        fuentes_renovables = "'Wind', 'Solar', 'Other Renewables', 'Hydro', 'Geothermal', 'Combustible Renewables'"
        fuentes_no_renovables = "'Coal, Peat and Manufactured Gases', 'Oil and Petroleum Products', 'Natural Gas', 'Other Combustible Non-Renewables', 'Nuclear'"

        query_renovables = f"""
        SELECT SUBSTR(Time, -4) AS Year, Product, SUM(Value) AS Total_GWh
        FROM Monthly_Electricity_Statistics
        WHERE Balance = 'Net Electricity Production' AND Product IN ({fuentes_renovables}) {pais_filter}
        AND Time NOT LIKE '%2025%'
        GROUP BY Year, Product
        ORDER BY Year ASC
        """

        query_no_renovables = f"""
        SELECT SUBSTR(Time, -4) AS Year, Product, SUM(Value) AS Total_GWh
        FROM Monthly_Electricity_Statistics
        WHERE Balance = 'Net Electricity Production' AND Product IN ({fuentes_no_renovables}) {pais_filter}
        AND Time NOT LIKE '%2025%'
        GROUP BY Year, Product
        ORDER BY Year ASC
        """

        df_ren = pd.read_sql_query(query_renovables, conn)
        df_no_ren = pd.read_sql_query(query_no_renovables, conn)

        if df_ren.empty and df_no_ren.empty:
            st.warning(f"No hay datos disponibles para {pais}.")
            return

        fig, axs = plt.subplots(1, 2, figsize=(12, 4))

        if not df_ren.empty:
            df_ren_pivot = df_ren.pivot(index='Year', columns='Product', values='Total_GWh').fillna(0)
            df_ren_pivot.plot(kind='bar', stacked=True, ax=axs[0], legend=False)
            axs[0].set_title("Energías Renovables")
            axs[0].set_ylabel("GWh Generados")
            axs[0].legend(title='Fuentes Renovables', loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2)
        else:
            axs[0].text(0.5, 0.5, 'No hay datos renovables', ha='center', va='center')
            axs[0].axis('off')

        if not df_no_ren.empty:
            df_no_ren_pivot = df_no_ren.pivot(index='Year', columns='Product', values='Total_GWh').fillna(0)
            df_no_ren_pivot.plot(kind='bar', stacked=True, ax=axs[1], legend=False)
            axs[1].set_title("Energías No Renovables")
            axs[1].set_ylabel("GWh Generados")
            axs[1].legend(title='Fuentes No Renovables', loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2)
        else:
            axs[1].text(0.5, 0.5, 'No hay datos no renovables', ha='center', va='center')
            axs[1].axis('off')

        plt.suptitle(f"{pais if pais != 'Todos' else 'Global'}", fontsize=14)
        st.pyplot(fig)
        st.caption("📊 Estos gráficos de barras apiladas muestran el desglose anual por fuente de generación de electricidad renovable y no renovable.")
