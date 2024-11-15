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

# Filtro por minutos jugados (ajustar según el nombre de la columna)
try:
    min_min = df["Minutos"].astype(float).min()  # Cambiar a df["MIN"] si el nombre es otro
    min_max = df["Minutos"].astype(float).max()  # Cambiar a df["MIN"] si el nombre es otro
except KeyError:
    st.error("La columna 'Minutos' no se encuentra en el DataFrame. Verifica el scraping.")
    st.stop()

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

# Mostrar estadísticas agregadas
st.write("Estadísticas agregadas:")
st.write(f"Promedio de puntos por jugador: {df_filtrado['Puntos'].astype(float).mean():.2f}")
st.write(f"Promedio de rebotes por jugador: {df_filtrado['Rebotes'].astype(float).mean():.2f}")
st.write(f"Promedio de asistencias por jugador: {df_filtrado['Asistencias'].astype(float).mean():.2f}")


