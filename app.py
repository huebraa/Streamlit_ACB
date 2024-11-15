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
    # Perfiles para otras posiciones (Escolta, Alero, Ala-pivot, Pivot)...
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

# Calcular puntuaciones de perfiles para todos los jugadores
for posicion, perfiles in perfiles_posiciones.items():
    for perfil_nombre, perfil in perfiles.items():
        df_filtrado[perfil_nombre] = df_filtrado.apply(lambda row: calcular_puntuacion_percentil(row, perfil), axis=1)

# Tabla general con puntuaciones
tabla_general = df_filtrado[["Jugador", "Posición", "Minutos"] + list(perfiles_posiciones["Base (PG)"].keys())].sort_values(by="Minutos", ascending=False)
st.write("Tabla general de jugadores con puntuaciones por perfiles:", tabla_general)

# Filtros para posición y perfil
posicion_seleccionada = st.sidebar.selectbox("Selecciona una posición", ["Todas"] + list(perfiles_posiciones.keys()))
perfil_seleccionado = None
if posicion_seleccionada != "Todas":
    perfil_seleccionado = st.sidebar.selectbox(
        f"Selecciona un perfil para {posicion_seleccionada}",
        list(perfiles_posiciones[posicion_seleccionada].keys())
    )

# Mostrar tabla e imagen con los mejores jugadores según los filtros
if perfil_seleccionado:
    df_perfil = df_filtrado[df_filtrado["Posición"] == posicion_seleccionada].sort_values(perfil_seleccionado, ascending=False).head(5)
    
    st.write(f"Top 5 jugadores en el perfil '{perfil_seleccionado}' para la posición {posicion_seleccionada}:")
    st.write(df_perfil[["Jugador", perfil_seleccionado]])

    # Crear imagen
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(df_perfil["Jugador"], df_perfil[perfil_seleccionado], color='skyblue')
    ax.set_xlabel('Puntuación (Percentil)')
    ax.set_title(f"Top 5 - {perfil_seleccionado} ({posicion_seleccionada})")
    st.pyplot(fig)
