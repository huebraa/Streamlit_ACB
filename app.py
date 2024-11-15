import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar los datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("estadisticas_completas.csv")

# Cargar los datos
df = cargar_datos()

# Validación de columnas necesarias
columnas_necesarias = [
    "MIN", "Posición", "Jugador", "PTS", "AST%", "STL%", "TRB%", "DRtg", 
    "eFG%", "TOV%", "PPR", "PER", "3P%", "FG%", "FT%", "BLK%", "USG%", 
    "ORtg", "ORB%", "DRB%", "FIC", "PF"
]
faltantes = [col for col in columnas_necesarias if col not in df.columns]
if faltantes:
    st.error(f"Faltan las siguientes columnas en los datos: {', '.join(faltantes)}")
    st.stop()

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

# Perfiles por posición (igual que en tu código original)
perfiles_posiciones = { ... }  # Copia aquí el mapeo de perfiles de posiciones

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

# Calcular puntuaciones de los perfiles
for posicion, perfiles in perfiles_posiciones.items():
    for perfil_nombre, perfil in perfiles.items():
        columnas = perfil.keys()
        pesos = perfil.values()
        try:
            df_filtrado[perfil_nombre] = df_filtrado[columnas].mul(pesos).sum(axis=1)
        except KeyError as e:
            st.warning(f"Columna faltante para el perfil '{perfil_nombre}': {e}")

# Selectores en la barra lateral
st.sidebar.header("Selecciona el perfil para cada posición")
perfil_base = st.sidebar.selectbox("Perfil Base (PG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Base (PG)"].keys()))
perfil_escolta = st.sidebar.selectbox("Perfil Escolta (SG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Escolta (SG)"].keys()))
perfil_alero = st.sidebar.selectbox("Perfil Alero (SF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Alero (SF)"].keys()))
perfil_ala_pivot = st.sidebar.selectbox("Perfil Ala-Pívot (PF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Ala-Pívot (PF)"].keys()))
perfil_pivot = st.sidebar.selectbox("Perfil Pívot (C)", ["Selecciona un perfil"] + list(perfiles_posiciones["Pívot (C)"].keys()))

# Mostrar la tabla general ordenable
st.write("Tabla General de Jugadores con sus puntuaciones por perfil:")
st.dataframe(df_filtrado)

# Mostrar los mejores jugadores para cada posición y perfil seleccionado
def mostrar_mejores(df_posicion, perfil, titulo):
    if perfil != "Selecciona un perfil":
        top_jugadores = df_posicion.sort_values(perfil, ascending=False).head(5)
        st.write(f"Los 5 mejores jugadores para el perfil '{perfil}' en la posición {titulo}:")
        st.dataframe(top_jugadores[["Jugador", "Posición", perfil]])

        # Visualización gráfica
        fig, ax = plt.subplots()
        ax.barh(top_jugadores["Jugador"], top_jugadores[perfil], color="skyblue")
        ax.set_xlabel("Puntuación")
        ax.set_title(f"Top 5 jugadores - {perfil}")
        st.pyplot(fig)

# Base
mostrar_mejores(df_filtrado[df_filtrado["Posición"] == "Base (PG)"], perfil_base, "Base (PG)")

# Escolta
mostrar_mejores(df_filtrado[df_filtrado["Posición"] == "Escolta (SG)"], perfil_escolta, "Escolta (SG)")

# Alero
mostrar_mejores(df_filtrado[df_filtrado["Posición"] == "Alero (SF)"], perfil_alero, "Alero (SF)")

# Ala-Pívot
mostrar_mejores(df_filtrado[df_filtrado["Posición"] == "Ala-Pívot (PF)"], perfil_ala_pivot, "Ala-Pívot (PF)")

# Pívot
mostrar_mejores(df_filtrado[df_filtrado["Posición"] == "Pívot (C)"], perfil_pivot, "Pívot (C)")
