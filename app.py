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

# Filtros de posiciones y perfiles generales (Pass-First, Scorer, Two-Way)
perfiles_generales = {
    "Pass-First": {
        "AST%": 0.30,
        "PPR": 0.30,
        "STL%": 0.15,
        "eFG%": 0.10,
        "ORtg": 0.10
    },
    "Scorer": {
        "PTS": 0.40,
        "3P%": 0.25,
        "AST%": 0.10,
        "STL%": 0.10,
        "TOV%": 0.15
    },
    "Two-Way": {
        "STL%": 0.30,
        "AST%": 0.20,
        "DRtg": 0.25,
        "TRB%": 0.15,
        "PER": 0.10
    }
}

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
df = df[df["Minutos"] >= minutos_minimos]

# Filtro para ver por posición (en barra lateral)
posicion_seleccionada = st.sidebar.selectbox("Seleccionar posición", ["Todas las posiciones", "Base (PG)", "Escolta (SG)", "Alero (SF)", "Ala-Pívot (PF)", "Pívot (C)"])

# Filtro para seleccionar un perfil (en barra lateral)
perfil_seleccionado = st.sidebar.selectbox("Seleccionar perfil", ["Pass-First", "Scorer", "Two-Way"])

# Cálculo de puntuaciones para la tabla general (sin filtrar por posición)
df["Puntuacion Pass-First"] = df.apply(lambda row: calcular_puntuacion(row, perfiles_generales["Pass-First"]), axis=1)
df["Puntuacion Scorer"] = df.apply(lambda row: calcular_puntuacion(row, perfiles_generales["Scorer"]), axis=1)
df["Puntuacion Two-Way"] = df.apply(lambda row: calcular_puntuacion(row, perfiles_generales["Two-Way"]), axis=1)

# Mostrar tabla general
st.write("Tabla general de puntuaciones:")
st.write(df[["Jugador", "Posición", "Puntuacion Pass-First", "Puntuacion Scorer", "Puntuacion Two-Way", "Minutos"]].sort_values(by="Puntuacion Pass-First", ascending=False))

# Filtrar por posición seleccionada
if posicion_seleccionada != "Todas las posiciones":
    df_posicion = df[df["Posición"] == posicion_seleccionada]
else:
    df_posicion = df.copy()

# Obtener el perfil seleccionado y calcular puntuaciones específicas para esa posición
if posicion_seleccionada != "Todas las posiciones":
    perfil = perfiles_posiciones.get(posicion_seleccionada, {}).get(perfil_seleccionado, None)
else:
    perfil = perfiles_generales.get(perfil_seleccionado, None)

# Si hay perfil seleccionado, calcular puntuaciones y mostrar los 5 mejores jugadores
if perfil is not None:
    df_posicion["Puntuacion"] = df_posicion.apply(lambda row: calcular_puntuacion(row, perfil), axis=1)
    df_mejores = df_posicion[["Jugador", "Posición", "Puntuacion", "Minutos"]].sort_values(by="Puntuacion", ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil {perfil_seleccionado} en la posición {posicion_seleccionada}:")
    st.write(df_mejores)
else:
    st.write("Selecciona una posición y un perfil para ver los resultados.")
