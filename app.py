import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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

# Filtrar por Escolta
perfil_escolta = st.sidebar.selectbox("Perfil Escolta (SG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Escolta (SG)"].keys()))

# Filtrar por Alero
perfil_alero = st.sidebar.selectbox("Perfil Alero (SF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Alero (SF)"].keys()))

# Filtrar por Ala-Pívot
perfil_ala_pivot = st.sidebar.selectbox("Perfil Ala-Pívot (PF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Ala-Pívot (PF)"].keys()))

# Filtrar por Pívot
perfil_pivot = st.sidebar.selectbox("Perfil Pívot (C)", ["Selecciona un perfil"] + list(perfiles_posiciones["Pívot (C)"].keys()))

# Mostrar la tabla general de puntuaciones de los perfiles (sin filtros de posición ni perfil)
st.write("Tabla General de Jugadores con sus puntuaciones por perfil:")
perfil_columnas = [col for col in df_filtrado.columns if col not in ["Jugador", "Posición", "Minutos"]]  # Filtrar columnas de puntuaciones
st.write(df_filtrado[["Jugador", "Posición"] + perfil_columnas])

# Mostrar los 5 mejores jugadores para cada posición y perfil seleccionado
# Para Base
if perfil_base != "Selecciona un perfil":
    df_base = df_filtrado[df_filtrado["Posición"] == "Base (PG)"].sort_values(perfil_base, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_base}' en la posición Base (PG):")
    st.write(df_base[["Jugador", "Posición", perfil_base]])

# Para Escolta
if perfil_escolta != "Selecciona un perfil":
    df_escolta = df_filtrado[df_filtrado["Posición"] == "Escolta (SG)"].sort_values(perfil_escolta, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_escolta}' en la posición Escolta (SG):")
    st.write(df_escolta[["Jugador", "Posición", perfil_escolta]])

# Para Alero
if perfil_alero != "Selecciona un perfil":
    df_alero = df_filtrado[df_filtrado["Posición"] == "Alero (SF)"].sort_values(perfil_alero, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_alero}' en la posición Alero (SF):")
    st.write(df_alero[["Jugador", "Posición", perfil_alero]])

# Para Ala-Pívot
if perfil_ala_pivot != "Selecciona un perfil":
    df_ala_pivot = df_filtrado[df_filtrado["Posición"] == "Ala-Pívot (PF)"].sort_values(perfil_ala_pivot, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_ala_pivot}' en la posición Ala-Pívot (PF):")
    st.write(df_ala_pivot[["Jugador", "Posición", perfil_ala_pivot]])

# Para Pívot
if perfil_pivot != "Selecciona un perfil":
    df_pivot = df_filtrado[df_filtrado["Posición"] == "Pívot (C)"].sort_values(perfil_pivot, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_pivot}' en la posición Pívot (C):")
    st.write(df_pivot[["Jugador", "Posición", perfil_pivot]])

# Roles por defecto para cada posición
rol_por_defecto = {
    "Base (PG)": "Two-Way PG",
    "Escolta (SG)": "Scorer SG",
    "Alero (SF)": "Scoring SF",
    "Ala-Pívot (PF)": "Stretch PF",
    "Pívot (C)": "Defensive C"
}

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Roles por defecto para cada posición
rol_por_defecto = {
    "Base (PG)": "Two-Way PG",
    "Escolta (SG)": "Scorer SG",
    "Alero (SF)": "Scoring SF",
    "Ala-Pívot (PF)": "Stretch PF",
    "Pívot (C)": "Defensive C"
}

# Seleccionar por defecto un perfil para cada posición
perfil_base = rol_por_defecto["Base (PG)"]
perfil_escolta = rol_por_defecto["Escolta (SG)"]
perfil_alero = rol_por_defecto["Alero (SF)"]
perfil_ala_pivot = rol_por_defecto["Stretch PF"]
perfil_pivot = rol_por_defecto["Defensive C"]

# Obtener los datos para los mejores jugadores de cada posición y perfil
top5_data = {}

for posicion, perfil in rol_por_defecto.items():
    df_top5 = df_filtrado[df_filtrado["Posición"] == posicion].sort_values(perfil, ascending=False).head(5)
    top5_data[posicion] = (perfil, df_top5[["Jugador", perfil]])

# Dibujar la cancha de baloncesto
def draw_court(ax=None, color="black", lw=2):
    if ax is None:
        ax = plt.gca()

    # Dibujar la cancha
    ax.add_patch(patches.Rectangle((0, 0), 50, 94, linewidth=lw, color=color, fill=False))  # Contorno
    ax.add_patch(patches.Circle((25, 47), 6, linewidth=lw, color=color, fill=False))       # Círculo central
    ax.add_patch(patches.Rectangle((17, 0), 16, 19, linewidth=lw, color=color, fill=False))  # Área pintada abajo
    ax.add_patch(patches.Rectangle((17, 75), 16, 19, linewidth=lw, color=color, fill=False)) # Área pintada arriba
    ax.add_patch(patches.Circle((25, 5.25), 1.5, linewidth=lw, color=color, fill=False))     # Aro abajo
    ax.add_patch(patches.Circle((25, 88.75), 1.5, linewidth=lw, color=color, fill=False))    # Aro arriba

    ax.plot([19, 31], [19, 19], color=color, linewidth=lw)   # Línea libre abajo
    ax.plot([19, 31], [75, 75], color=color, linewidth=lw)   # Línea libre arriba
    ax.plot([25, 25], [0, 94], color=color, linewidth=lw)    # Línea central

    ax.set_xlim(0, 50)
    ax.set_ylim(0, 94)
    ax.set_aspect(1)

# Crear la imagen de la cancha con jugadores posicionados
def crear_imagen_cancha(top5_data):
    fig, ax = plt.subplots(figsize=(8, 15))
    draw_court(ax)

    # Coordenadas aproximadas de cada posición en la cancha
    posiciones_coords = {
        "Base (PG)": (25, 10),
        "Escolta (SG)": (15, 35),
        "Alero (SF)": (35, 35),
        "Ala-Pívot (PF)": (20, 75),
        "Pívot (C)": (30, 75)
    }

    # Colocar los jugadores en sus posiciones
    for posicion, (perfil, datos) in top5_data.items():
        x, y = posiciones_coords[posicion]
        texto = f"{posicion}\n({perfil})\n\n"
        for jugador, puntuacion in zip(datos["Jugador"], datos[perfil]):
            texto += f"{jugador} ({puntuacion:.1f})\n"

        # Agregar texto al gráfico
        ax.text(
            x, y, texto,
            ha="center", va="center",
            fontsize=10, color="black",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.5")
        )

    # Título general
    fig.suptitle(
        "Top Jugadores por Posición",
        fontsize=16,
        weight="bold",
        color="black",
        y=0.92
    )

    return fig

# Crear y mostrar la imagen en Streamlit
fig = crear_imagen_cancha(top5_data)
st.pyplot(fig)


