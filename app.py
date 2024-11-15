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

# Función para calcular la puntuación de cada perfil
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    for stat, peso in perfil.items():
        if stat in row:
            try:
                valor = float(row[stat])
                puntuacion += valor * peso
            except ValueError:
                st.write(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row['Jugador']}. Valor: {row[stat]}")
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

# Agregar las puntuaciones para los perfiles de todas las posiciones
for posicion, perfiles in perfiles_posiciones.items():
    for perfil_nombre, perfil in perfiles.items():
        df_filtrado[perfil_nombre] = df_filtrado.apply(lambda row: calcular_puntuacion(row, perfil), axis=1)

# Filtro para ver por posición (en barra lateral)
posicion_seleccionada = st.sidebar.selectbox("Seleccionar posición", ["Todas las posiciones", "Base (PG)", "Escolta (SG)", "Alero (SF)", "Ala-Pívot (PF)", "Pívot (C)"])

# Filtro para ver el perfil de la posición seleccionada (en barra lateral)
perfil_seleccionado = st.sidebar.selectbox("Seleccionar perfil", ["Selecciona un perfil"] + list(perfiles_posiciones.get(posicion_seleccionada, {}).keys()))

# Mostrar la tabla general de puntuaciones de los perfiles (sin filtros de posición ni perfil)
st.write("Tabla General de Jugadores con sus puntuaciones por perfil:")
perfil_columnas = [col for col in df_filtrado.columns if col not in ["Jugador", "Posición", "Minutos"]]  # Filtrar columnas de puntuaciones
st.write(df_filtrado[["Jugador", "Posición"] + perfil_columnas])

# Mostrar los 5 mejores jugadores en la posición seleccionada para el perfil elegido
if posicion_seleccionada != "Todas las posiciones" and perfil_seleccionado != "Selecciona un perfil":
    # Filtrar los jugadores según la posición seleccionada
    df_posicion = df_filtrado[df_filtrado["Posición"] == posicion_seleccionada]

    # Ordenar por la puntuación del perfil seleccionado y mostrar los 5 mejores
    df_mejores = df_posicion.nlargest(5, perfil_seleccionado)[["Jugador", "Posición", perfil_seleccionado]]
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_seleccionado}' en la posición {posicion_seleccionada}:")
    st.write(df_mejores)
