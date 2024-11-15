import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Perfiles por posición
perfiles_posiciones = {
    "Base (PG)": {
        "Pass-First PG": {
            "AST%": 0.30,
            "PPR": 0.30,
            "STL%": 0.15,
            "eFG%": 0.15,
            "ORtg": 0.10
        },
        "Scorer PG": {
            "PTS": 0.40,
            "3P%": 0.25,
            "AST%": 0.10,
            "STL%": 0.10,
            "TOV%": 0.15
        },
        "Two-Way PG": {
            "STL%": 0.30,
            "AST%": 0.20,
            "DRtg": 0.25,
            "TRB%": 0.15,
            "PER": 0.10
        }
    },
    "Escolta (SG)": {
        "Pass-First SG": {
            "AST%": 0.35,
            "PPR": 0.25,
            "STL%": 0.15,
            "eFG%": 0.10,
            "ORtg": 0.15
        },
        "Scorer SG": {
            "PTS": 0.40,
            "3P%": 0.30,
            "eFG%": 0.15,
            "STL%": 0.10,
            "TOV%": 0.05
        },
        "Two-Way SG": {
            "STL%": 0.35,
            "DRtg": 0.25,
            "AST%": 0.15,
            "3P%": 0.10,
            "TOV%": 0.15
        }
    },
    "Alero (SF)": {
        "Playmaking SF": {
            "AST%": 0.30,
            "PPR": 0.30,
            "STL%": 0.15,
            "eFG%": 0.15,
            "ORtg": 0.10
        },
        "Scoring SF": {
            "PTS": 0.40,
            "3P%": 0.30,
            "eFG%": 0.15,
            "STL%": 0.10,
            "TOV%": 0.05
        },
        "Two-Way SF": {
            "STL%": 0.35,
            "DRtg": 0.30,
            "TRB%": 0.15,
            "eFG%": 0.10,
            "TOV%": 0.10
        }
    }
}

# Función para calcular percentiles
def calcular_percentiles(df, columnas):
    for columna in columnas:
        if columna in df.columns:
            df[columna + "_pct"] = df[columna].rank(pct=True) * 100
    return df

# Calcular percentiles para todas las estadísticas relevantes
estadisticas = [stat for perfil_dict in perfiles_posiciones.values() for perfil in perfil_dict.values() for stat in perfil.keys()]
df = calcular_percentiles(df, estadisticas)

# Función para calcular la puntuación de cada perfil en términos de percentiles
def calcular_puntuacion_percentil(row, perfil):
    puntuacion = 0
    for stat, peso in perfil.items():
        stat_pct = stat + "_pct"  # Usar la columna de percentiles
        if stat_pct in row:
            puntuacion += row[stat_pct] * peso
    return puntuacion

# Filtro de mínimo de minutos
minutos_minimos = st.sidebar.slider(
    "Selecciona el mínimo de minutos jugados",
    min_value=int(df["Minutos"].min()), 
    max_value=int(df["Minutos"].max()), 
    value=int(df["Minutos"].min()), 
    step=1
)

# Filtrar los jugadores que tengan al menos el mínimo de minutos seleccionados
df_filtrado = df[df["Minutos"] >= minutos_minimos]

# Agregar las puntuaciones para los perfiles de todas las posiciones
for posicion, perfiles in perfiles_posiciones.items():
    for perfil_nombre, perfil in perfiles.items():
        df_filtrado[perfil_nombre] = df_filtrado.apply(lambda row: calcular_puntuacion_percentil(row, perfil), axis=1)

# Filtro para seleccionar la posición y el perfil
posicion_seleccionada = st.sidebar.selectbox("Selecciona una posición", ["Todas"] + list(perfiles_posiciones.keys()))
if posicion_seleccionada != "Todas":
    perfil_seleccionado = st.sidebar.selectbox(
        f"Selecciona un perfil para {posicion_seleccionada}", 
        list(perfiles_posiciones[posicion_seleccionada].keys())
    )

# Mostrar los 5 mejores jugadores como imagen
def mostrar_imagen_top_5(df_filtrado, posicion, perfil):
    # Filtrar por la posición y perfil seleccionado
    df_posicion = df_filtrado[df_filtrado["Posición"] == posicion].sort_values(perfil, ascending=False).head(5)
    
    # Crear la imagen con matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    jugadores = df_posicion["Jugador"]
    puntuaciones = df_posicion[perfil]
    
    # Mostrar la lista como un gráfico
    ax.barh(jugadores, puntuaciones, color='skyblue')
    ax.set_xlabel('Puntuación')
    ax.set_title(f"Top 5 jugadores para el perfil '{perfil}' en la posición {posicion}")
    st.pyplot(fig)

# Mostrar resultados
if posicion_seleccionada != "Todas" and perfil_seleccionado:
    mostrar_imagen_top_5(df_filtrado, posicion_seleccionada, perfil_seleccionado)
