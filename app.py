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

# Definir los pesos para cada perfil
perfil_pass_first = {
    "AST%": 0.2,
    "PPR": 0.40,  # Vamos a calcular esta métrica a partir de AST% y USG%
    "STL%": 0.15,
    "eFG%": 0.15,
    "ORtg": 0.10,
    "TOV%": 0.05
}

perfil_scorer = {
    "ORtg": 0.40,
    "3P%": 0.25,
    "eFG%": 0.15,
    "AST%": 0.10,
    "STL%": 0.05,
    "TOV%": 0.05
}

perfil_two_way = {
    "AST%": 0.15,
    "DRtg": 0.40,
    "STL%": 0.15,
    "TRB%": 0.10,
    "eFG%": 0.10,
    "TOV%": 0.10
}

# Función para calcular la puntuación de cada perfil
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    # Si existe la columna "AST%" y "USG%", calculamos "AST/USG"
    if "AST%" in row and "USG%" in row:
        ast_usg = row["AST%"] / row["USG%"]  # Calcular AST/USG
        row["AST/USG"] = ast_usg  # Asignar esta métrica al dataframe (de forma temporal)
    
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

# Filtro de mínimo de minutos
minutos_minimos = st.sidebar.slider(
    "Selecciona el mínimo de minutos jugados",
    min_value=int(df["Minutos"].min()), 
    max_value=int(df["Minutos"].max()), 
    value=int(df["Minutos"].min()), 
    step=1
)

# Filtrar los jugadores que tengan al menos el mínimo de minutos seleccionados
df = df[df["Minutos"] >= minutos_minimos]

# Filtro para ver por posición (en barra lateral)
posicion_seleccionada = st.sidebar.selectbox("Seleccionar posición", ["Todas las posiciones", "Base (PG)", "Escolta (SG)", "Alero (SF)", "Ala-Pívot (PF)", "Pívot (C)"])

if posicion_seleccionada != "Todas las posiciones":
    df = df[df["Posición"] == posicion_seleccionada]

# Filtro para seleccionar el perfil de jugador
perfil_seleccionado = st.sidebar.selectbox("Seleccionar perfil de jugador", ["Pass-First", "Scorer", "Two-Way"])

# Definir el perfil según la selección
if perfil_seleccionado == "Pass-First":
    perfil = perfil_pass_first
elif perfil_seleccionado == "Scorer":
    perfil = perfil_scorer
else:
    perfil = perfil_two_way

# Calcular las puntuaciones para todos los jugadores
df["Puntuacion"] = df.apply(lambda row: calcular_puntuacion(row, perfil), axis=1)

# Mostrar la tabla general
st.write("Tabla general de jugadores:")
st.write(df[["Jugador", "Posición", "Minutos", "PTS", "Puntuacion"]])

# Mostrar los 5 mejores jugadores según el perfil seleccionado
st.write(f"Los 5 mejores jugadores para el perfil: {perfil_seleccionado}")
df_mejores = df[["Jugador", "Puntuacion", "Minutos"]].sort_values(by="Puntuacion", ascending=False).head(5)
st.write(df_mejores)
