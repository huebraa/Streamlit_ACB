import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# URLs para las posiciones
urls_posiciones = {
    "Base (PG)": "https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Advanced_Stats/Qualified/All/per/PG/desc/1/Regular_Season",
    "Escolta (SG)": "https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Advanced_Stats/Qualified/All/per/SG/desc/1/Regular_Season",
    "Alero (SF)": "https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Advanced_Stats/Qualified/All/per/SF/desc/1/Regular_Season",
    "Ala-Pívot (PF)": "https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Advanced_Stats/Qualified/All/per/PF/desc/1/Regular_Season",
    "Pívot (C)": "https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Advanced_Stats/Qualified/All/per/C/desc/1/Regular_Season",
}

# URL para los totales (minutos jugados)
url_totales = "https://basketball.realgm.com/international/league/4/Spanish-ACB/stats/2025/Totals/Qualified/All/per/All/desc/1/Regular_Season"

# Función para extraer datos de una tabla
def extraer_datos(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "tablesaw"})
    rows = table.find_all("tr")
    
    # Procesar encabezados
    columns = [col.text.strip() for col in rows[0].find_all("th")]
    
    # Procesar filas
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        cols = [col.text.strip() for col in cols]
        data.append(cols)
    
    # Crear DataFrame
    return pd.DataFrame(data, columns=columns)

# Extraer datos de todas las posiciones
datos_posiciones = []
for posicion, url in urls_posiciones.items():
    df = extraer_datos(url)
    df["Posición"] = posicion  # Agregar columna de posición
    datos_posiciones.append(df)

# Combinar todos los datos de posiciones
df_posiciones = pd.concat(datos_posiciones, ignore_index=True)

# Extraer datos de totales (minutos jugados)
df_totales = extraer_datos(url_totales)

# Verificar los nombres de las columnas
print("Columnas en df_posiciones:", df_posiciones.columns)
print("Columnas en df_totales:", df_totales.columns)

# Ajustar las columnas de unión según los nombres reales
columna_jugador_posiciones = "Player"  # Cambia si es diferente
columna_equipo_posiciones = "Team"  # Cambia si es diferente
columna_jugador_totales = "Player"  # Cambia si es diferente
columna_equipo_totales = "Team"  # Cambia si es diferente

# Renombrar columnas si es necesario
df_posiciones.rename(
    columns={columna_jugador_posiciones: "Jugador", columna_equipo_posiciones: "Equipo"},
    inplace=True,
)
df_totales.rename(
    columns={columna_jugador_totales: "Jugador", columna_equipo_totales: "Equipo"},
    inplace=True,
)

# Combinar datos por "Jugador" y "Equipo"
df_completo = pd.merge(df_posiciones, df_totales, on=["Jugador", "Equipo"], how="inner")

# Mostrar los datos en Streamlit
st.write(df_completo)

# Añadir selección por posición
posiciones = ["Base (PG)", "Escolta (SG)", "Alero (SF)", "Ala-Pívot (PF)", "Pívot (C)"]
posicion = st.selectbox("Filtrar por posición:", options=posiciones)  # Cambié 'opciones' por 'options'

# Filtrar datos por la posición seleccionada
df_filtrado = df_completo[df_completo["Posición"] == posicion]

# Mostrar datos filtrados por la posición
st.write(df_filtrado)
