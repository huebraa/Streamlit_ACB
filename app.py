import streamlit as st
import pandas as pd

# Función para cargar los datos
@st.cache
def cargar_datos():
    return pd.read_csv("estadisticas_completas.csv")

# Cargar los datos
df = cargar_datos()

# Verificar los nombres de las columnas para debug
st.write("Columnas del DataFrame:", df.columns)

# Título de la aplicación
st.title("Estadísticas Avanzadas - Liga ACB")

# Mostrar los primeros registros
st.write("Visualizando las estadísticas de los jugadores:")
st.dataframe(df.head())  # Mostrar las primeras filas para verificar los datos

# Filtro por posición
posiciones = df["Posición"].unique()
posicion = st.selectbox("Selecciona una posición:", posiciones)

# Filtro por minutos jugados (usando la columna correcta 'MIN')
min_min = df["MIN"].astype(float).min()  # Cambiado a 'MIN'
min_max = df["MIN"].astype(float).max()  # Cambiado a 'MIN'
minutos = st.slider("Filtrar por minutos jugados:", 
                    min_value=min_min, 
                    max_value=min_max, 
                    value=(min_min, min_max))

# Aplicar los filtros
df_filtrado = df[(df["Posición"] == posicion) & 
                 (df["MIN"].astype(float).between(minutos[0], minutos[1]))]  # Cambiado a 'MIN'

# Mostrar los resultados filtrados
st.write(f"Jugadores en la posición {posicion} con entre {minutos[0]} y {minutos[1]} minutos jugados:")
st.dataframe(df_filtrado)

# Mostrar estadísticas agregadas
st.write("Estadísticas agregadas:")
st.write(f"Promedio de puntos por jugador: {df_filtrado['Puntos'].astype(float).mean():.2f}")
st.write(f"Promedio de rebotes por jugador: {df_filtrado['Rebotes'].astype(float).mean():.2f}")
st.write(f"Promedio de asistencias por jugador: {df_filtrado['Asistencias'].astype(float).mean():.2f}")

