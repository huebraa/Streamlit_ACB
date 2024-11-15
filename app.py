import streamlit as st
import pandas as pd

# Cargar datos
@st.cache
def cargar_datos():
    return pd.read_csv("estadisticas_acb.csv")

datos = cargar_datos()

# Título de la aplicación
st.title("Estadísticas Avanzadas - Liga ACB")

# Mostrar los datos
st.write("Datos de jugadores:")
st.dataframe(datos)

# Filtro por posición
posiciones = datos['Posición'].unique() if 'Posición' in datos.columns else []
posicion = st.selectbox("Filtrar por posición:", opciones=posiciones)

if posicion:
    datos_filtrados = datos[datos['Posición'] == posicion]
    st.write(f"Jugadores en la posición: {posicion}")
    st.dataframe(datos_filtrados)
