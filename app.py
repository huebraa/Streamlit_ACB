import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Perfiles por posición
perfiles_posiciones = {
    "Base (PG)": {
        "Pass-First PG": {
            "AST%": 0.30,
            "PPR": 0.30,
            "STL%": 0.15,
            "eFG%": 0.10,
            "ORtg": 0.10
        },
        "Scorer PG": {
            "PTS": 0.40,
            "3P%": 0.25,
            "AST%": 0.10,
            "STL%": 0.10,
            "TOV%": 0.15
        },
        "Two-Way PG": {
            "STL%": 0.30,
            "AST%": 0.20,
            "DRtg": 0.25,
            "TRB%": 0.15,
            "PER": 0.10
        }
    },
    "Escolta (SG)": {
        "Pass-First SG": {
            "AST%": 0.35,
            "PPR": 0.25,
            "STL%": 0.15,
            "eFG%": 0.10,
            "ORtg": 0.15
        },
        "Scorer SG": {
            "PTS": 0.40,
            "3P%": 0.30,
            "eFG%": 0.15,
            "STL%": 0.10,
            "TOV%": 0.05
        },
        "Two-Way SG": {
            "STL%": 0.35,
            "DRtg": 0.25,
            "AST%": 0.15,
            "3P%": 0.10,
            "TOV%": 0.15
        }
    },
    "Alero (SF)": {
        "Playmaking SF": {
            "AST%": 0.30,
            "PPR": 0.30,
            "STL%": 0.15,
            "eFG%": 0.15,
            "ORtg": 0.10
        },
        "Scoring SF": {
            "PTS": 0.40,
            "3P%": 0.30,
            "eFG%": 0.15,
            "STL%": 0.10,
            "TOV%": 0.05
        },
        "Two-Way SF": {
            "STL%": 0.35,
            "DRtg": 0.30,
            "TRB%": 0.15,
            "eFG%": 0.10,
            "TOV%": 0.10
        }
    },
    "Ala-Pívot (PF)": {
        "Stretch PF": {
            "3P%": 0.35,
            "eFG%": 0.30,
            "PTS": 0.20,
            "TRB%": 0.10,
            "TOV%": 0.05
        },
        "Post-Play PF": {
            "TRB%": 0.30,
            "PTS": 0.25,
            "BLK%": 0.20,
            "ORtg": 0.15,
            "STL%": 0.10
        },
        "Two-Way PF": {
            "STL%": 0.25,
            "TRB%": 0.25,
            "DRtg": 0.20,
            "eFG%": 0.15,
            "TOV%": 0.15
        }
    },
    "Pívot (C)": {
        "Defensive C": {
            "BLK%": 0.40,
            "DRtg": 0.30,
            "TRB%": 0.15,
            "TOV%": 0.10,
            "STL%": 0.05
        },
        "Scoring C": {
            "PTS": 0.35,
            "TRB%": 0.25,
            "FG%": 0.20,
            "3P%": 0.10,
            "FT%": 0.10
        },
        "Two-Way C": {
            "STL%": 0.25,
            "BLK%": 0.30,
            "TRB%": 0.25,
            "PTS": 0.10,
            "eFG%": 0.10
        }
    }
}

# Función para calcular los percentiles por posición
def calcular_percentiles_por_posicion(df, posicion):
    # Filtrar los jugadores por la posición
    df_posicion = df[df["Posición"] == posicion]
    
    # Aplicar percentiles sobre las estadísticas para cada jugador
    for col in df.columns:
        if col not in ["Jugador", "Posición", "Minutos"]:  # Excluir columnas no numéricas
            df_posicion[col + "_percentil"] = df_posicion.groupby("Posición")[col].transform(lambda x: pd.qcut(x, 100, labels=False) + 1)
    
    return df_posicion

# Función para calcular la puntuación del perfil usando percentiles
def calcular_puntuacion_percentil(row, perfil):
    puntuacion = 0
    for stat, peso in perfil.items():
        percentil_columna = stat + "_percentil"
        if percentil_columna in row:
            try:
                valor = row[percentil_columna]  # Usamos los percentiles
                puntuacion += valor * peso
            except ValueError:
                st.write(f"Advertencia: No se pudo calcular el percentil de {stat} para el jugador {row['Jugador']}. Valor: {row[percentil_columna]}")
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
df_filtrado = df[df["Minutos"] >= minutos_minimos]

# Agregar los percentiles por posición
df_filtrado = df_filtrado.copy()
for posicion in perfiles_posiciones.keys():
    df_filtrado[posicion] = calcular_percentiles_por_posicion(df_filtrado, posicion)

# Agregar las puntuaciones para los perfiles de todas las posiciones
for posicion, perfiles in perfiles_posiciones.items():
    for perfil_nombre, perfil in perfiles.items():
        df_filtrado[perfil_nombre] = df_filtrado.apply(lambda row: calcular_puntuacion_percentil(row, perfil), axis=1)

# Filtro para ver el perfil de la posición seleccionada (en barra lateral)
st.sidebar.header("Selecciona el perfil para cada posición")

# Filtrar por Base
perfil_base = st.sidebar.selectbox("Perfil Base (PG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Base (PG)"].keys()))

# Filtrar por Escolta
perfil_escolta = st.sidebar.selectbox("Perfil Escolta (SG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Escolta (SG)"].keys()))

# Filtrar por Alero
perfil_alero = st.sidebar.selectbox("Perfil Alero (SF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Alero (SF)"].keys()))

# Filtrar por Ala-Pívot
perfil_ala_pivot = st.sidebar.selectbox("Perfil Ala-Pívot (PF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Ala-Pívot (PF)"].keys()))

# Filtrar por Pívot
perfil_pivot = st.sidebar.selectbox("Perfil Pívot (C)", ["Selecciona un perfil"] + list(perfiles_posiciones["Pívot (C)"].keys()))

# Función para mostrar los 5 mejores jugadores como imagen
def mostrar_imagen_top_5(df_filtrado, posicion, perfil):
    # Filtrar por la posición y perfil seleccionado
    df_posicion = df_filtrado[df_filtrado["Posición"] == posicion].sort_values(perfil, ascending=False).head(5)
    
    # Crear la imagen con matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Crear lista de jugadores y puntuaciones
    jugadores = df_posicion["Jugador"]
    puntuaciones = df_posicion[perfil]
    
    # Mostrar la lista como un gráfico
    ax.barh(jugadores, puntuaciones, color='skyblue')
    ax.set_xlabel('Puntuación')
    ax.set_title(f"Top 5 jugadores para el perfil '{perfil}' en la posición {posicion}")
    
    # Mostrar la imagen en Streamlit
    st.pyplot(fig)

# Mostrar la imagen de los 5 mejores para la Base (PG) y su perfil seleccionado
if perfil_base != "Selecciona un perfil":
    mostrar_imagen_top_5(df_filtrado, "Base (PG)", perfil_base)

# Mostrar la imagen de los 5 mejores para la Escolta (SG) y su perfil seleccionado
if perfil_escolta != "Selecciona un perfil":
    mostrar_imagen_top_5(df_filtrado, "Escolta (SG)", perfil_escolta)

# Mostrar la imagen de los 5 mejores para el Alero (SF) y su perfil seleccionado
if perfil_alero != "Selecciona un perfil":
    mostrar_imagen_top_5(df_filtrado, "Alero (SF)", perfil_alero)

# Mostrar la imagen de los 5 mejores para el Ala-Pívot (PF) y su perfil seleccionado
if perfil_ala_pivot != "Selecciona un perfil":
    mostrar_imagen_top_5(df_filtrado, "Ala-Pívot (PF)", perfil_ala_pivot)

# Mostrar la imagen de los 5 mejores para el Pívot (C) y su perfil seleccionado
if perfil_pivot != "Selecciona un perfil":
    mostrar_imagen_top_5(df_filtrado, "Pívot (C)", perfil_pivot)
