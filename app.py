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

# Calcular las puntuaciones para todos los jugadores
df["Puntuacion Pass-First"] = df.apply(lambda row: calcular_puntuacion(row, perfil_pass_first), axis=1)
df["Puntuacion Scorer"] = df.apply(lambda row: calcular_puntuacion(row, perfil_scorer), axis=1)
df["Puntuacion Two-Way"] = df.apply(lambda row: calcular_puntuacion(row, perfil_two_way), axis=1)

# Mostrar los datos con las puntuaciones calculadas
st.write(f"Puntuaciones de los jugadores para la posición: {posicion_seleccionada}")
df_mostrar = df[["Jugador", "Puntuacion Pass-First", "Puntuacion Scorer", "Puntuacion Two-Way", "Minutos"]]
df_mostrar = df_mostrar.sort_values(by="Puntuacion Pass-First", ascending=False)

# Mostrar la tabla de puntuaciones
st.write(df_mostrar)

# Mostrar los 5 mejores jugadores según el perfil elegido en un recuadro con fondo gris
if posicion_seleccionada != "Todas las posiciones":
    perfil_seleccionado = st.sidebar.selectbox("Seleccionar perfil", ["Pass-First", "Scorer", "Two-Way"])

    if perfil_seleccionado == "Pass-First":
        df_top = df[["Jugador", "Puntuacion Pass-First", "Posición"]].sort_values(by="Puntuacion Pass-First", ascending=False).head(5)
        st.markdown("<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'><h4>Top 5 - Pass-First</h4></div>", unsafe_allow_html=True)
        st.write(df_top)
    elif perfil_seleccionado == "Scorer":
        df_top = df[["Jugador", "Puntuacion Scorer", "Posición"]].sort_values(by="Puntuacion Scorer", ascending=False).head(5)
        st.markdown("<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'><h4>Top 5 - Scorer</h4></div>", unsafe_allow_html=True)
        st.write(df_top)
    elif perfil_seleccionado == "Two-Way":
        df_top = df[["Jugador", "Puntuacion Two-Way", "Posición"]].sort_values(by="Puntuacion Two-Way", ascending=False).head(5)
        st.markdown("<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'><h4>Top 5 - Two-Way</h4></div>", unsafe_allow_html=True)
        st.write(df_top)
