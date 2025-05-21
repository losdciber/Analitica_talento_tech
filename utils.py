
import sqlite3
import pandas as pd

def ejecutar_consulta(query):
    """
    Ejecuta una consulta SQL en la base de datos 'analisis_energetico.db' y devuelve un DataFrame.

    Parámetros:
    - query: Cadena de texto con la consulta SQL.

    Retorna:
    - DataFrame con el resultado de la consulta.
    """
    conn = sqlite3.connect("data/analisis_energetico.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def cargar_datos():
    """
    Carga toda la tabla 'Monthly_Electricity_Statistics' desde la base de datos SQLite,
    excluyendo registros globales o promedios agregados como "OECD" o "Total", y agrega
    una columna de año (Year) para facilitar análisis anuales.

    Retorna:
    - DataFrame con los datos filtrados y columna adicional 'Year'.
    """
    query = """
    SELECT * 
    FROM 'Monthly_Electricity_Statistics'
    WHERE Country NOT LIKE '%OECD%' 
      AND Country NOT LIKE '%Total%'
    ORDER BY Country ASC
    """
    df = ejecutar_consulta(query)
    df['Year'] = df['Time'].str.extract(r'(\d{4})')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    return df

def obtener_produccion_mensual():
    """
    Consultar la base de datos para obtener únicamente los registros donde
    el balance sea 'Net Electricity Production'. Devuelve columnas clave
    como Product, Country, Time, Value y Balance.

    Retorna:
    - DataFrame con datos de producción neta de electricidad.
    """
    query = """
    SELECT Product, Country, Time, Value, Balance
    FROM Monthly_Electricity_Statistics
    WHERE Balance = 'Net Electricity Production'
    """
    return ejecutar_consulta(query)

def clasificar_y_filtrar_productos(df, pais=None, tipo_energia='ambas'):
    """
    Clasifica cada fila del DataFrame según el tipo de energía (renovable o no renovable)
    y aplica filtros opcionales por país y tipo de energía.

    Parámetros:
    - df: DataFrame con columnas 'Product', 'Country', 'Value', etc.
    - pais: Nombre del país a filtrar (por defecto: None o 'Todos')
    - tipo_energia: 'ambas', 'renovables' o 'no_renovables'

    Retorna:
    - DataFrame filtrado y clasificado, con columna extra 'Energy_Type'.
    """
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




def obtener_emisiones_co2():
    """
    Carga los datos de emisiones de CO₂ desde la tabla:
    'International Energy Agency - CO2 emissions by sector in Colombia'
    """
    query = "SELECT * FROM 'International Energy Agency - CO2 emissions by sector in Colombia'"
    return ejecutar_consulta(query)
