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

# Definir los pesos para cada perfil
perfil_pass_first = {
    "AST%": 0.30,
    "AST%/USG%": 0.25,
    "STL%": 0.15,
    "eFG%": 0.15,
    "PTS": 0.10,
    "TOV%": 0.05
}

perfil_scorer = {
    "PTS": 0.40,
    "3P%": 0.25,
    "eFG%": 0.15,
    "AST%": 0.10,
    "STL%": 0.05,
    "TOV%": 0.05
}

perfil_two_way = {
    "AST%": 0.25,
    "STL%": 0.25,
    "PTS": 0.15,
    "TRB%": 0.15,
    "eFG%": 0.10,
    "TOV%": 0.10
}

# Función para calcular la puntuación de cada perfil
def calcular_puntuacion(df, perfil):
    puntuaciones = []
    for index, row in df.iterrows():
        puntuacion = 0
        for stat, peso in perfil.items():
            if stat in row:
                puntuacion += row[stat] * peso
        puntuaciones.append(puntuacion)
    return puntuaciones

# Calcular puntuaciones para cada perfil
df_base["Puntuacion Pass-First"] = calcular_puntuacion(df_base, perfil_pass_first)
df_base["Puntuacion Scorer"] = calcular_puntuacion(df_base, perfil_scorer)
df_base["Puntuacion Two-Way"] = calcular_puntuacion(df_base, perfil_two_way)

# Mostrar los 5 mejores jugadores según cada perfil
top_5_pass_first = df_base.nlargest(5, "Puntuacion Pass-First")
top_5_scorer = df_base.nlargest(5, "Puntuacion Scorer")
top_5_two_way = df_base.nlargest(5, "Puntuacion Two-Way")

# Mostrar los resultados
st.subheader("Top 5 Jugadores - Pass-First PG")
st.dataframe(top_5_pass_first)

st.subheader("Top 5 Jugadores - Scoring PG")
st.dataframe(top_5_scorer)

st.subheader("Top 5 Jugadores - Two-Way PG")
st.dataframe(top_5_two_way)
