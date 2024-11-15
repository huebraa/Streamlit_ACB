import streamlit as st
import pandas as pd

# Función para cargar los datos
@st.cache
def cargar_datos():
    return pd.read_csv("estadisticas_completas.csv")

# Cargar los datos
df = cargar_datos()

# Mapeo de nombres de las columnas para que se vean en español
columnas_espanol = {
    "MIN": "Minutos",
    "Posición": "Posición",
    "TS%": "TS%",
    "eFG%": "eFG%",
    "ORB%": "ORB%",
    "DRB%": "DRB%",
    "TRB%": "TRB%",
    "AST%": "AST%",
    "TOV%": "TOV%",
    "STL%": "STL%",
    "BLK%": "BLK%",
    "USG%": "USG%",
    "PPR": "PPR",
    "PPS": "PPS",
    "ORtg": "ORtg",
    "DRtg": "DRtg",
    "eDiff": "eDiff",
    "FIC": "FIC",
    "PER": "PER",
    "PTS": "PTS",
    "FG%": "FG%",
    "3P%": "3P%",
    "FT%": "FT%",
    "PF": "PF"
}

# Renombrar las columnas
df = df.rename(columns=columnas_espanol)

# Filtrar solo a jugadores en la posición de base (PG)
df_base = df[df["Posición"] == "PG"]

# Ver los primeros registros para asegurarnos de que los datos están cargados correctamente
# st.write(df.head())  # Eliminar esta línea para no mostrar la tabla

# Definir los pesos para el perfil de Base Pass-First (solo como ejemplo)
perfil_pass_first = {
    "AST%": 0.30,
    "AST%/USG%": 0.25,
    "STL%": 0.15,
    "eFG%": 0.15,
    "PTS": 0.10,
    "TOV%": 0.05
}

# Función para calcular la puntuación de un jugador
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    for stat, peso in perfil.items():
        if stat in row:
            puntuacion += row[stat] * peso
    return puntuacion

# Seleccionar un jugador específico para ver su puntuación
jugador_seleccionado = df_base.iloc[0]  # Tomamos el primer jugador de la lista (puedes cambiar el índice si lo prefieres)

# Calcular la puntuación del jugador seleccionado
puntuacion_pass_first = calcular_puntuacion(jugador_seleccionado, perfil_pass_first)

# Mostrar el jugador y su puntuación
st.write(f"Jugador seleccionado: {jugador_seleccionado['Jugador']}")
st.write(f"Puntuación para el perfil Pass-First: {puntuacion_pass_first:.2f}")
