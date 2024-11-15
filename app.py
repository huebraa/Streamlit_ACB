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
    "Posición": "Posición"
}

# Renombrar las columnas
df = df.rename(columns=columnas_espanol)

# Título de la aplicación
st.title("Estadísticas de Jugadores - Liga ACB")

# Mostrar las posiciones disponibles al principio
posiciones = df["Posición"].unique()
posicion = st.selectbox("Selecciona una posición:", posiciones)

# Filtro por minutos jugados
min_min = df["Minutos"].astype(float).min()
min_max = df["Minutos"].astype(float).max()
minutos = st.slider("Filtrar por minutos jugados:", 
                    min_value=min_min, 
                    max_value=min_max, 
                    value=(min_min, min_max))

# Aplicar los filtros
df_filtrado = df[(df["Posición"] == posicion) & 
                 (df["Minutos"].astype(float).between(minutos[0], minutos[1]))]

# Mostrar los resultados filtrados
st.write(f"Jugadores en la posición {posicion} con entre {minutos[0]} y {minutos[1]} minutos jugados:")
st.dataframe(df_filtrado)

