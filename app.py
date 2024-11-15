import streamlit as st
import pandas as pd

# Cargar datos del archivo CSV
@st.cache_data
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

# Perfiles por posición
perfiles_posiciones = {
    "Base (PG)": {
        "Pass-First PG": {"AST%": 0.30, "PPR": 0.30, "STL%": 0.15, "eFG%": 0.10, "ORtg": 0.10},
        "Scorer PG": {"PTS": 0.40, "3P%": 0.25, "AST%": 0.10, "STL%": 0.10, "TOV%": 0.15},
        "Two-Way PG": {"STL%": 0.30, "AST%": 0.20, "DRtg": 0.25, "TRB%": 0.15, "PER": 0.10}
    },
    "Escolta (SG)": {
        "Pass-First SG": {"AST%": 0.35, "PPR": 0.25, "STL%": 0.15, "eFG%": 0.10, "ORtg": 0.15},
        "Scorer SG": {"PTS": 0.40, "3P%": 0.30, "eFG%": 0.15, "STL%": 0.10, "TOV%": 0.05},
        "Two-Way SG": {"STL%": 0.35, "DRtg": 0.25, "AST%": 0.15, "3P%": 0.10, "TOV%": 0.15}
    },
    "Alero (SF)": {
        "Playmaking SF": {"AST%": 0.30, "PPR": 0.30, "STL%": 0.15, "eFG%": 0.15, "ORtg": 0.10},
        "Scoring SF": {"PTS": 0.40, "3P%": 0.30, "eFG%": 0.15, "STL%": 0.10, "TOV%": 0.05},
        "Two-Way SF": {"STL%": 0.35, "DRtg": 0.30, "TRB%": 0.15, "eFG%": 0.10, "TOV%": 0.10}
    },
    "Ala-Pívot (PF)": {
        "Stretch PF": {"3P%": 0.35, "eFG%": 0.30, "PTS": 0.20, "TRB%": 0.10, "TOV%": 0.05},
        "Post-Play PF": {"TRB%": 0.30, "PTS": 0.25, "BLK%": 0.20, "ORtg": 0.15, "STL%": 0.10},
        "Two-Way PF": {"STL%": 0.25, "TRB%": 0.25, "DRtg": 0.20, "eFG%": 0.15, "TOV%": 0.15}
    },
    "Pívot (C)": {
        "Defensive C": {"BLK%": 0.40, "DRtg": 0.30, "TRB%": 0.15, "TOV%": 0.10, "STL%": 0.05},
        "Scoring C": {"PTS": 0.35, "TRB%": 0.25, "FG%": 0.20, "3P%": 0.10, "FT%": 0.10},
        "Two-Way C": {"STL%": 0.25, "BLK%": 0.30, "TRB%": 0.25, "PTS": 0.10, "eFG%": 0.10}
    }
}

# Calcular la puntuación de cada perfil
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    for stat, peso in perfil.items():
        if stat in row:
            puntuacion += row[stat] * peso
    return puntuacion

# Filtros de minutos jugados y perfiles por posición
minutos_minimos = st.sidebar.slider("Mínimo de minutos jugados", min_value=int(df["Minutos"].min()), max_value=int(df["Minutos"].max()), value=900)

# Filtrar datos
df_filtrado = df[df["Minutos"] >= minutos_minimos]

# Seleccionar perfiles por posición
perfil_seleccionado = {}
for posicion in perfiles_posiciones.keys():
    perfil_seleccionado[posicion] = st.sidebar.selectbox(f"Perfil para {posicion}", ["Selecciona un perfil"] + list(perfiles_posiciones[posicion].keys()))

# Calcular y mostrar los mejores jugadores
st.header("24-25 Albanian Kategoria Superiore, Top 5 Players Per Role")

for posicion, perfil in perfil_seleccionado.items():
    if perfil != "Selecciona un perfil":
        perfil_datos = perfiles_posiciones[posicion][perfil]
        df_filtrado[posicion] = df_filtrado.apply(lambda row: calcular_puntuacion(row, perfil_datos), axis=1)
        
        top_5 = df_filtrado[df_filtrado["Posición"] == posicion].sort_values(posicion, ascending=False).head(5)
        
        # Crear una sección para cada posición
        st.subheader(f"{perfil} ({posicion})")
        for idx, row in top_5.iterrows():
            st.write(f"{row['Jugador']} - Score: {round(row[posicion], 1)}")

# Mostrar la imagen de referencia al final
st.image("/mnt/data/image.png", caption="Ejemplo de visualización de jugadores")
