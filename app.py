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

# Verificar las primeras filas para asegurarnos de que los datos están cargados correctamente
st.write(df.head())

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
            if stat in row:  # Verificar si la estadística está en la fila
                puntuacion += row[stat] * peso
            else:
                st.write(f"Advertencia: La columna {stat} no se encuentra en la fila del jugador {row['Jugador']}")
        puntuaciones.append(puntuacion)
    return puntuaciones

# Calcular puntuaciones para cada perfil
st.write("Calculando puntuaciones para los perfiles...")

# Añadir una verificación para saber si el cálculo está funcionando
try:
    df_base["Puntuacion Pass-First"] = calcular_puntuacion(df_base, perfil_pass_first)
    df_base["Puntuacion Scorer"] = calcular_puntuacion(df_base, perfil_scorer)
    df_base["Puntuacion Two-Way"] = calcular_puntuacion(df_base, perfil_two_way)
except Exception as e:
    st.write(f"Error calculando las puntuaciones: {e}")

# Mostrar los 5 mejores jugadores según cada perfil (solo mostrar nombre y puntuación)
top_5_pass_first = df_base.nlargest(5, "Puntuacion Pass-First")[["Jugador", "Puntuacion Pass-First"]]
top_5_scorer = df_base.nlargest(5, "Puntuacion Scorer")[["Jugador", "Puntuacion Scorer"]]
top_5_two_way = df_base.nlargest(5, "Puntuacion Two-Way")[["Jugador", "Puntuacion Two-Way"]]

# Mostrar los resultados en la parte principal
st.subheader("Top 5 Jugadores - Pass-First PG")
st.dataframe(top_5_pass_first)

st.subheader("Top 5 Jugadores - Scoring PG")
st.dataframe(top_5_scorer)

st.subheader("Top 5 Jugadores - Two-Way PG")
st.dataframe(top_5_two_way)

# Filtros adicionales ya existentes para la aplicación
posiciones = df["Posición"].unique()
posicion = st.selectbox("Selecciona una posición:", posiciones)

# Mover los filtros de minutos a la barra lateral
st.sidebar.header("Filtrar por minutos jugados")
min_min = df["Minutos"].astype(float).min()
min_max = df["Minutos"].astype(float).max()
minutos = st.sidebar.slider("Filtrar por minutos jugados:", 
                            min_value=min_min, 
                            max_value=min_max, 
                            value=(min_min, min_max))

# Aplicar los filtros
df_filtrado = df[(df["Posición"] == posicion) & 
                 (df["Minutos"].astype(float).between(minutos[0], minutos[1]))]

# Mostrar los resultados filtrados en la sección principal
st.write(f"Jugadores en la posición {posicion} con entre {minutos[0]} y {minutos[1]} minutos jugados:")
st.dataframe(df_filtrado)

