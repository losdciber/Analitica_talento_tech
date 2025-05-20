
import sqlite3
import pandas as pd

def cargar_datos():
    conn = sqlite3.connect("data/analisis_energetico.db")
    query = """
    SELECT * 
    FROM 'Monthly_Electricity_Statistics'
    WHERE Country NOT LIKE '%OECD%' 
    AND Country NOT LIKE '%Total%'
    ORDER BY Country ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df['Year'] = df['Time'].str.extract(r'(\d{4})')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    return df

def obtener_produccion_mensual():
    conn = sqlite3.connect("data/analisis_energetico.db")
    query = """
    SELECT Product, Country, Time, Value, Balance
    FROM Monthly_Electricity_Statistics
    WHERE Balance = 'Net Electricity Production'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def clasificar_y_filtrar_productos(df, pais=None, tipo_energia='ambas'):
    productos_excluir = [
        'Electricity', 'Total Combustible Fuels',
        'Total Renewables (Hydro, Geo, Solar, Wind, Other)',
        'Not Specified', 'Data is estimated for this month'
    ]
    productos_renovables = [
        'Hydro', 'Wind', 'Geothermal',
        'Combustible Renewables', 'Solar', 'Other Renewables'
    ]
    df_filtrado = df[~df['Product'].isin(productos_excluir)].copy()
    df_filtrado['Energy_Type'] = df_filtrado['Product'].apply(
        lambda x: 'Renewable' if x in productos_renovables else 'Non-Renewable'
    )
    if pais and pais != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Country'] == pais]
    if tipo_energia == 'renovables':
        df_filtrado = df_filtrado[df_filtrado['Energy_Type'] == 'Renewable']
    elif tipo_energia == 'no_renovables':
        df_filtrado = df_filtrado[df_filtrado['Energy_Type'] == 'Non-Renewable']
    return df_filtrado
