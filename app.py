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
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    # Iterar sobre cada estadística y su peso
    for stat, peso in perfil.items():
        # Verificar si la estadística existe en el dataframe
        if stat in row:
            try:
                valor = float(row[stat])
                puntuacion += valor * peso
            except ValueError:
                st.write(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row['Jugador']}. Valor: {row[stat]}")
        else:
            st.write(f"Advertencia: La columna {stat} no se encuentra en la fila del jugador {row['Jugador']}")
    
    return puntuacion

# Calcular las puntuaciones para los jugadores de la posición base (PG)
df_base["Puntuacion Pass-First"] = df_base.apply(lambda row: calcular_puntuacion(row, perfil_pass_first), axis=1)
df_base["Puntuacion Scorer"] = df_base.apply(lambda row: calcular_puntuacion(row, perfil_scorer), axis=1)
df_base["Puntuacion Two-Way"] = df_base.apply(lambda row: calcular_puntuacion(row, perfil_two_way), axis=1)

# Mostrar las puntuaciones calculadas para todos los bases
st.write("Puntuaciones para todos los jugadores de la posición Base (PG) según los perfiles:")
st.write(df_base[["Jugador", "Puntuacion Pass-First", "Puntuacion Scorer", "Puntuacion Two-Way"]])
