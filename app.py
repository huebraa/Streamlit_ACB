import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar los datos
@st.cache_data
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

# Perfiles por posición (simplificado aquí para ejemplo)
perfiles_posiciones = {
    "Base (PG)": {
        "Pass-First PG": {"AST%": 0.30, "PPR": 0.30, "STL%": 0.15, "eFG%": 0.10, "ORtg": 0.10},
        "Scorer PG": {"PTS": 0.40, "3P%": 0.25, "AST%": 0.10, "STL%": 0.10, "TOV%": 0.15}
    },
    "Escolta (SG)": {
        "Pass-First SG": {"AST%": 0.35, "PPR": 0.25, "STL%": 0.15, "eFG%": 0.10, "ORtg": 0.15},
        "Scorer SG": {"PTS": 0.40, "3P%": 0.30, "eFG%": 0.15, "STL%": 0.10, "TOV%": 0.05}
    }
    # Otros perfiles para las posiciones se agregan de forma similar
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

# Mostrar tabla general de puntuaciones de los perfiles
st.write("Tabla General de Jugadores con sus puntuaciones por perfil:")
perfil_columnas = [col for col in df_filtrado.columns if col not in ["Jugador", "Posición", "Minutos"]]  # Filtrar columnas de puntuaciones
st.dataframe(df_filtrado[["Jugador", "Posición"] + perfil_columnas])

# Mejorar la elección de perfiles y permitir comparaciones entre varios perfiles
st.sidebar.header("Selecciona los perfiles para comparar")

# Permitir seleccionar múltiples perfiles por posición
perfil_base = st.sidebar.multiselect("Selecciona los perfiles para Base (PG)", list(perfiles_posiciones["Base (PG)"].keys()))
perfil_escolta = st.sidebar.multiselect("Selecciona los perfiles para Escolta (SG)", list(perfiles_posiciones["Escolta (SG)"].keys()))

# Crear un gráfico comparativo para los jugadores seleccionados
if perfil_base or perfil_escolta:
    fig, ax = plt.subplots(figsize=(10, 6))

    # Filtrar los perfiles seleccionados para cada posición
    for perfil in perfil_base:
        df_base = df_filtrado[df_filtrado["Posición"] == "Base (PG)"].sort_values(perfil, ascending=False).head(5)
        ax.barh(df_base["Jugador"], df_base[perfil], label=f"Base - {perfil}")

    for perfil in perfil_escolta:
        df_escolta = df_filtrado[df_filtrado["Posición"] == "Escolta (SG)"].sort_values(perfil, ascending=False).head(5)
        ax.barh(df_escolta["Jugador"], df_escolta[perfil], label=f"Escolta - {perfil}")

    ax.set_xlabel("Puntuación")
    ax.set_title("Comparación de Puntuaciones por Perfil")
    ax.legend()
    st.pyplot(fig)

# Mostrar los 5 mejores jugadores para cada perfil seleccionado
if perfil_base:
    st.write(f"Los 5 mejores jugadores para los perfiles seleccionados en la posición Base (PG):")
    df_base = df_filtrado[df_filtrado["Posición"] == "Base (PG)"].sort_values(perfil_base[0], ascending=False).head(5)
    st.write(df_base[["Jugador", "Posición"] + perfil_base])

if perfil_escolta:
    st.write(f"Los 5 mejores jugadores para los perfiles seleccionados en la posición Escolta (SG):")
    df_escolta = df_filtrado[df_filtrado["Posición"] == "Escolta (SG)"].sort_values(perfil_escolta[0], ascending=False).head(5)
    st.write(df_escolta[["Jugador", "Posición"] + perfil_escolta])
