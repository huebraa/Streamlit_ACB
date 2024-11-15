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
}

# Renombrar las columnas
df = df.rename(columns=columnas_espanol)

# Filtro por la posición Base (PG)
df_base = df[df["Posición"] == "PG"]

# Asignar pesos para cada estadística
pesos = {
    "AST%": 0.30,
    "TS%": 0.25,
    "TOV%": -0.20,
    "STL%": 0.15,
    "USG%": 0.10,
}

# Función para calcular el puntaje del jugador
def calcular_puntaje(row, pesos):
    puntaje = (row["AST%"] * pesos["AST%"] +
               row["TS%"] * pesos["TS%"] +
               row["TOV%"] * pesos["TOV%"] +
               row["STL%"] * pesos["STL%"] +
               row["USG%"] * pesos["USG%"])
    return puntaje

# Aplicar la función a cada jugador para calcular su puntaje
df_base["Puntaje"] = df_base.apply(lambda row: calcular_puntaje(row, pesos), axis=1)

# Obtener los 5 mejores jugadores según su puntaje
df_mejores = df_base.nlargest(5, "Puntaje")

# Mostrar los resultados
st.title("Mejores Jugadores Base (PG) según Perfil")

# Muestra los jugadores con su puntaje
st.write("Los 5 mejores jugadores base (PG) según el perfil calculado son:")

# Mostrar tabla de los 5 mejores jugadores
st.dataframe(df_mejores[["Jugador", "Equipo", "TS%", "AST%", "TOV%", "STL%", "USG%", "Puntaje"]])

# Mostrar nombre y puntaje de los 5 mejores jugadores
for index, row in df_mejores.iterrows():
    st.write(f"{row['Jugador']} - Puntaje: {row['Puntaje']:.2f}")
