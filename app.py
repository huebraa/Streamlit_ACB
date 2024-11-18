import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar y procesar los datos
@st.cache
def cargar_datos():
    # Cargar archivo CSV
    file_path = "estadisticas_completas.csv"
    data = pd.read_csv(file_path)
    
    # Mapeo de columnas
    columnas_a_renombrar = {
        "MIN": "Minutos",
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
        "PF": "PF",
        "Posición": "Posición"
    }
    data.rename(columns=columnas_a_renombrar, inplace=True)
    
    # Filtrar columnas relevantes
    columnas_relevantes = list(columnas_a_renombrar.values())
    data = data[columnas_relevantes]
    return data

# Cargar datos
df = cargar_datos()

# Perfiles por posición
perfiles_posiciones = {
    "Base (PG)": {
        "Pass-First PG": {"AST%": 0.30, "PPR": 0.30, "STL%": 0.15, "eFG%": 0.10, "ORtg": 0.10},
        "Scorer PG": {"PTS": 0.40, "3P%": 0.25, "AST%": 0.10, "STL%": 0.10, "TOV%": 0.15},
        "Two-Way PG": {"STL%": 0.30, "AST%": 0.20, "DRtg": 0.25, "TRB%": 0.15, "PER": 0.10},
    },
    # Otros perfiles...
    "Escolta (SG)": {
        "Pass-First SG": {"AST%": 0.35, "PPR": 0.25, "STL%": 0.15, "eFG%": 0.10, "ORtg": 0.15},
        "Scorer SG": {"PTS": 0.40, "3P%": 0.30, "eFG%": 0.15, "STL%": 0.10, "TOV%": 0.05},
        "Two-Way SG": {"STL%": 0.35, "DRtg": 0.25, "AST%": 0.15, "3P%": 0.10, "TOV%": 0.15},
    },
    # Otros perfiles...
    "Pívot (C)": {
        "Defensive C": {"BLK%": 0.40, "DRtg": 0.30, "TRB%": 0.15, "TOV%": 0.10, "STL%": 0.05},
        "Scoring C": {"PTS": 0.35, "TRB%": 0.25, "FG%": 0.20, "3P%": 0.10, "FT%": 0.10},
        "Two-Way C": {"STL%": 0.25, "BLK%": 0.30, "TRB%": 0.25, "PTS": 0.10, "eFG%": 0.10},
    }
}

# Normalización de estadísticas a percentiles por posición
estadisticas_relevantes = set(
    stat for perfiles in perfiles_posiciones.values() for perfil in perfiles.values() for stat in perfil.keys()
)

# Calcular percentiles dentro de cada posición
for stat in estadisticas_relevantes:
    if stat in df:  # Asegúrate de que la estadística está en el DataFrame
        df[stat] = df.groupby("Posición")[stat].rank(pct=True) * 100

# Función para calcular la puntuación de cada perfil
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    for stat, peso in perfil.items():
        if stat in row:
            try:
                valor = float(row[stat])
                puntuacion += valor * peso
            except ValueError:
                st.warning(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row['Jugador']}. Valor: {row[stat]}")
    return puntuacion

# Filtrado por mínimo de minutos
minutos_minimos = st.sidebar.slider(
    "Selecciona el mínimo de minutos jugados",
    min_value=int(df["Minutos"].min()),
    max_value=int(df["Minutos"].max()),
    value=int(df["Minutos"].min()),
    step=1
)

df_filtrado = df[df["Minutos"] >= minutos_minimos]

# Agregar las puntuaciones para los perfiles de todas las posiciones
for posicion, perfiles in perfiles_posiciones.items():
    for perfil_nombre, perfil in perfiles.items():
        df_filtrado[perfil_nombre] = df_filtrado.apply(lambda row: calcular_puntuacion(row, perfil), axis=1)

# Filtro para ver el perfil de la posición seleccionada (en barra lateral)
st.sidebar.header("Selecciona el perfil para cada posición")

# Filtrar por Base
perfil_base = st.sidebar.selectbox("Perfil Base (PG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Base (PG)"].keys()))

# Mostrar los 5 mejores jugadores para cada posición y perfil seleccionado
if perfil_base != "Selecciona un perfil":
    df_base = df_filtrado[df_filtrado["Posición"] == "Base (PG)"].sort_values(perfil_base, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_base}' en la posición Base (PG):")
    st.write(df_base[["Jugador", "Posición", perfil_base]])
