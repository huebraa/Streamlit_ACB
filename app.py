import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Función para cargar los datos
@st.cache_data(ttl=3600)
def cargar_datos():
    """Carga los datos desde un archivo CSV."""
    return pd.read_csv("estadisticas_acb_con_posicion.csv")

# Cargar los datos
df = cargar_datos()

# Validar que el CSV tenga las columnas esperadas
columnas_espanol = {
    "MIN": "Minutos",
    "Posición": "Posición",
    "Equipo": "Equipo",
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
}

# Renombrar las columnas si están presentes
expected_columns = set(columnas_espanol.keys())
if not expected_columns.issubset(df.columns):
    st.error(f"Faltan columnas esperadas en el archivo CSV: {expected_columns - set(df.columns)}")
else:
    df = df.rename(columns=columnas_espanol)

# Configuración para perfiles de posición
perfiles_posiciones = {
    "Base (PG)": {
        "Pass-First PG": {"AST%": 0.25, "PPR": 0.4, "TS%": 0.10, "eFG%": 0.05, "ORtg": 0.05, "Ast/TO": 0.15},
        "Scorer PG": {"PTS": 0.25, "ORtg": 0.5, "HOB": 0.25},
        "Defensive PG": {"STL%": 0.15, "Stl/TO": 0.15, "DRtg": 0.5, "TRB%": 0.15, "BLK%": 0.15},
    },
    "Escolta (SG)": {
        "Pass-First SG": {"AST%": 0.35, "PPR": 0.25, "STL%": 0.15, "eFG%": 0.10, "ORtg": 0.15},
        "Scorer SG": {"PTS": 0.40, "3P%": 0.30, "eFG%": 0.15, "STL%": 0.10, "TOV%": 0.05},
        "Two-Way SG": {"STL%": 0.35, "DRtg": 0.25, "AST%": 0.15, "3P%": 0.10, "TOV%": 0.15},
    },
    "Alero (SF)": {
        "Playmaking SF": {"AST%": 0.30, "PPR": 0.30, "STL%": 0.15, "eFG%": 0.15, "ORtg": 0.10},
        "Scoring SF": {"PTS": 0.40, "3P%": 0.30, "eFG%": 0.15, "STL%": 0.10, "TOV%": 0.05},
        "Two-Way SF": {"STL%": 0.35, "DRtg": 0.30, "TRB%": 0.15, "eFG%": 0.10, "TOV%": 0.10},
    },
    "Ala-Pívot (PF)": {
        "Stretch PF": {"3P%": 0.35, "eFG%": 0.30, "PTS": 0.20, "TRB%": 0.10, "TOV%": 0.05},
        "Post-Play PF": {"TRB%": 0.30, "PTS": 0.25, "BLK%": 0.20, "ORtg": 0.15, "STL%": 0.10},
        "Two-Way PF": {"STL%": 0.25, "TRB%": 0.25, "DRtg": 0.20, "eFG%": 0.15, "TOV%": 0.15},
    },
    "Pívot (C)": {
        "Defensive C": {"BLK%": 0.40, "DRtg": 0.30, "TRB%": 0.15, "TOV%": 0.10, "STL%": 0.05},
        "Scoring C": {"PTS": 0.35, "TRB%": 0.25, "FG%": 0.20, "3P%": 0.10, "FT%": 0.10},
        "Two-Way C": {"STL%": 0.25, "BLK%": 0.30, "TRB%": 0.25, "PTS": 0.10, "eFG%": 0.10},
    },
}

# Definir las estadísticas inversas
estadisticas_inversas = {"DRtg", "TOV%", "PF"}

# Normalización de estadísticas a percentiles por posición
estadisticas_relevantes = set(
    stat for perfiles in perfiles_posiciones.values() for perfil in perfiles.values() for stat in perfil.keys()
)

for stat in estadisticas_relevantes:
    if stat in df:
        min_stat = df.groupby("Posición")[stat].transform('min')
        max_stat = df.groupby("Posición")[stat].transform('max')
        if min_stat.equals(max_stat):  # Manejar valores constantes
            df[stat] = 50  # Percentil medio si los valores son constantes
        elif stat in estadisticas_inversas:
            df[stat] = ((max_stat - df[stat]) / (max_stat - min_stat)) * 100
        else:
            df[stat] = ((df[stat] - min_stat) / (max_stat - min_stat)) * 100

# Filtrar por mínimo de minutos jugados
minutos_minimos = st.sidebar.slider(
    "Selecciona el mínimo de minutos jugados",
    min_value=int(df["Minutos"].min()),
    max_value=int(df["Minutos"].max()),
    value=int(df["Minutos"].min()),
    step=1
)
df_filtrado = df[df["Minutos"] >= minutos_minimos]

# Calcular puntuaciones para cada perfil
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    for stat, peso in perfil.items():
        if stat in row:
            try:
                puntuacion += float(row[stat]) * peso
            except ValueError:
                st.warning(f"No se pudo convertir {stat} en puntuación.")
    return puntuacion

for posicion, perfiles in perfiles_posiciones.items():
    for perfil_nombre, perfil in perfiles.items():
        if perfil_nombre not in df_filtrado.columns:
            df_filtrado[perfil_nombre] = df_filtrado.apply(lambda row: calcular_puntuacion(row, perfil), axis=1)

# Función para mostrar gráficos
def mostrar_grafico(df_filtrado):
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(df_filtrado["Jugador"], df_filtrado["PTS"])
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al mostrar gráfico: {e}")

st.write("Datos filtrados:")
st.dataframe(df_filtrado)

# Mostrar gráfico
mostrar_grafico(df_filtrado)
