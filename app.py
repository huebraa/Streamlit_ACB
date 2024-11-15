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
    
    # Iterar sobre cada jugador en el dataframe
    for index, row in df.iterrows():
        puntuacion = 0
        # Iterar sobre cada estadística y su peso
        for stat, peso in perfil.items():
            # Verificar si la estadística existe en el dataframe
            if stat in row:
                # Asegurarse de que el valor es numérico (conversión a float)
                try:
                    valor = float(row[stat])
                    puntuacion += valor * peso
                except ValueError:
                    st.write(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row['Jugador']}. Valor: {row[stat]}")
            else:
                st.write(f"Advertencia: La columna {stat} no se encuentra en la fila del jugador {row['Jugador']}")
        
        # Agregar la puntuación calculada para el jugador
        puntuaciones.append(puntuacion)
    
    return puntuaciones

# Calcular puntuaciones para cada perfil
st.write("Calculando puntuaciones para los perfiles...")

# Crear las columnas de puntuaciones para cada perfil
try:
    df_base["Puntuacion Pass-First"] = calcular_puntuacion(df_base, perfil_pass_first)
    df_base["Puntuacion Scorer"] = calcular_puntuacion(df_base, perfil_scorer)
    df_base["Puntuacion Two-Way"] = calcular_puntuacion(df_base, perfil_two_way)
except Exception as e:
    st.write(f"Error calculando las puntuaciones: {e}")

# Verificar que las puntuaciones se calculan correctamente
st.write("Comprobando las puntuaciones calculadas para algunos jugadores:")
st.write(df_base[["Jugador", "Puntuacion Pass-First", "Puntuacion Scorer", "Puntuacion Two-Way"]].head(10))

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

# Mostrar la tabla completa con las puntuaciones para cada jugador
st.write("Tabla completa con las puntuaciones de los jugadores:")
st.dataframe(df_base[["Jugador", "Posición", "Minutos", "Puntuacion Pass-First", "Puntuacion Scorer", "Puntuacion Two-Way"]])
