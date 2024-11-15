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
    "TS%": "Eficiencia TS",
    "eFG%": "Eficiencia eFG",
    "AST%": "Asistencias %",
    "TOV%": "Pérdidas de balón %",
    "STL%": "Robos %",
    "USG%": "Uso de la posesión",
    "PER": "Eficiencia PER",
}

# Renombrar las columnas
df = df.rename(columns=columnas_espanol)

# Filtrar para la posición de Base (PG)
df_base = df[df["Posición"] == "PG"]

# Pesos asignados a cada estadística para la posición de Base (PG)
pesos = {
    "Asistencias %": 0.25,
    "Uso de la posesión": 0.20,
    "Eficiencia TS": 0.15,
    "Robos %": 0.15,
    "Pérdidas de balón %": 0.10,
    "Eficiencia PER": 0.10,
    "Minutos": 0.05,
}

# Normalizar las estadísticas de cada jugador para calcular un perfil
df_base["Perfil"] = (
    df_base["Asistencias %"] * pesos["Asistencias %"] +
    df_base["Uso de la posesión"] * pesos["Uso de la posesión"] +
    df_base["Eficiencia TS"] * pesos["Eficiencia TS"] +
    df_base["Robos %"] * pesos["Robos %"] +
    df_base["Pérdidas de balón %"] * -pesos["Pérdidas de balón %"] +  # Penalizar pérdidas
    df_base["Eficiencia PER"] * pesos["Eficiencia PER"] +
    df_base["Minutos"] * pesos["Minutos"]
)

# Ordenar a los mejores jugadores basados en el perfil
df_base = df_base.sort_values("Perfil", ascending=False)

# Título de la aplicación
st.title("Perfil de Jugadores - Base (PG)")

# Mostrar los resultados de los jugadores de base ordenados por el perfil
st.write("Los mejores jugadores en la posición de Base (PG) según el perfil:")
st.dataframe(df_base[['Jugador', 'Equipo', 'Perfil', 'Asistencias %', 'Uso de la posesión', 'Eficiencia TS', 'Robos %', 'Pérdidas de balón %', 'Eficiencia PER']])


