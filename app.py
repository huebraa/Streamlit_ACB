import streamlit as st
import pandas as pd

# Función para cargar los datos
@st.cache
def cargar_datos():
    return pd.read_csv("estadisticas_completas.csv")

# Cargar los datos
df = cargar_datos()

# Verificar y mostrar los nombres de las columnas
st.write("Columnas del DataFrame:")
st.write(df.columns)

# Renombrar las columnas para que se vean en español (Asegúrate de que los nombres son correctos)
columnas_espanol = {
    "MIN": "Minutos",
    "Posición": "Posición",
    "Puntos": "Puntos",
    "Asistencias": "Asistencias",
    "Robos": "Robos",
    "REB": "Rebotes",
    "TS%": "Eficiencia de tiro"
}

df = df.rename(columns=columnas_espanol)

# Título de la aplicación
st.title("Perfil del Jugador - Base (PG)")

# Filtro por la posición "Base"
df_base = df[df["Posición"] == "Base"]

# Verificar si la columna "Asistencias" está presente
if "Asistencias" in df_base.columns:
    # Calcular Asistencias por minuto
    df_base["Asistencias por minuto"] = df_base["Asistencias"] / df_base["Minutos"]
else:
    st.write("La columna 'Asistencias' no está presente en los datos.")

# Definir pesos para cada estadística
pesos = {
    "Asistencias": 0.30,
    "Puntos": 0.20,
    "Asistencias por minuto": 0.15,
    "Robos": 0.15,
    "Eficiencia de tiro": 0.10,
    "Minutos": 0.05,
    "Rebotes": 0.05
}

# Calcular puntaje ponderado para cada jugador si la columna de asistencias está presente
if "Asistencias por minuto" in df_base.columns:
    df_base["Puntaje"] = (
        df_base["Asistencias"] * pesos["Asistencias"] +
        df_base["Puntos"] * pesos["Puntos"] +
        df_base["Asistencias por minuto"] * pesos["Asistencias por minuto"] +
        df_base["Robos"] * pesos["Robos"] +
        df_base["Eficiencia de tiro"] * pesos["Eficiencia de tiro"] +
        df_base["Minutos"] * pesos["Minutos"] +
        df_base["Rebotes"] * pesos["Rebotes"]
    )

    # Mostrar los jugadores con el puntaje más alto
    st.write("Jugadores destacados en la posición de Base (PG) según su perfil:")
    df_base = df_base.sort_values(by="Puntaje", ascending=False)
    st.dataframe(df_base[['Jugador', 'Puntaje']])

    # Mostrar los primeros jugadores con puntaje alto
    st.write("Top 5 jugadores con el mejor perfil de Base:")
    st.dataframe(df_base[['Jugador', 'Puntaje']].head())
else:
    st.write("No se pudo calcular el perfil de base debido a la falta de las columnas necesarias.")
