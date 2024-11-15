import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Función para descargar los datos de la página web
def descargar_datos(url):
    # Realizamos la solicitud HTTP a la página
    response = requests.get(url)
    
    # Si la solicitud fue exitosa
    if response.status_code == 200:
        # Usamos BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar la tabla de estadísticas (identificada por la clase 'dataTable')
        table = soup.find('table', {'class': 'dataTable'})
        
        # Extraer las filas de la tabla
        rows = table.find_all('tr')
        
        # Extraer los encabezados de las columnas
        headers = [header.text.strip() for header in rows[0].find_all('th')]
        
        # Extraer los datos de cada fila
        data = []
        for row in rows[1:]:
            columns = row.find_all('td')
            if len(columns) > 1:
                data.append([column.text.strip() for column in columns])

        # Convertimos los datos en un DataFrame de pandas
        df = pd.DataFrame(data, columns=headers)
        return df
    else:
        st.error("No se pudo obtener los datos.")
        return pd.DataFrame()

# URLs de las estadísticas de cada posición
url_base = 'https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Advanced_Stats/Qualified/All/per/'

urls_posiciones = {
    'Base (PG)': url_base + 'PG/desc/1/Regular_Season',
    'Escolta (SG)': url_base + 'SG/desc/1/Regular_Season',
    'Alero (SF)': url_base + 'SF/desc/1/Regular_Season',
    'Ala-Pívot (PF)': url_base + 'PF/desc/1/Regular_Season',
    'Pívot (C)': url_base + 'C/desc/1/Regular_Season'
}

# URL para los minutos jugados (Totales)
url_totales = 'https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Totals/Qualified/All/per/All/desc/1/Regular_Season'

# Función para combinar los datos por jugador y equipo
def cargar_datos_completos():
    # Descargar los datos de las posiciones
    df_posiciones = descargar_datos(url_totales)  # Usamos los totales por ahora
    df_minutos = descargar_datos(url_totales)  # Puedes agregar otro dataset si lo tienes
    
    # Aseguramos que los nombres de las columnas coincidan (usaremos 'Player' y 'Team' para combinarlos)
    df_posiciones['Player'] = df_posiciones['Player'].str.strip()
    df_minutos['Player'] = df_minutos['Player'].str.strip()

    # Unir los DataFrames por el nombre del jugador y equipo
    df_completo = pd.merge(df_posiciones, df_minutos, on=['Player', 'Team'], how='inner')
    
    return df_completo

# Crear la aplicación Streamlit
st.title("Estadísticas de Jugadores ACB - 2025")

# Selección de posición
posiciones = ["Base (PG)", "Escolta (SG)", "Alero (SF)", "Ala-Pívot (PF)", "Pívot (C)"]
posicion = st.selectbox("Filtrar por posición:", opciones=posiciones)

# Descargar los datos de la posición seleccionada
df_posicion = descargar_datos(urls_posiciones[posicion])

# Cargar datos completos (posición + minutos)
df_completo = cargar_datos_completos()

# Mostrar los datos de la posición seleccionada
st.subheader(f"Estadísticas de Jugadores - {posicion}")
st.dataframe(df_posicion)

# Mostrar los datos completos con estadísticas combinadas
st.subheader("Estadísticas Combinadas de Jugadores")
st.dataframe(df_completo)

# Opción para filtrar las estadísticas
st.sidebar.header("Filtros de estadísticas")
columnas_filtro = st.sidebar.multiselect("Selecciona las estadísticas a mostrar", df_completo.columns.tolist())

if columnas_filtro:
    st.subheader("Estadísticas Filtradas")
    st.dataframe(df_completo[columnas_filtro])

