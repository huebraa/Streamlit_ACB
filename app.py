import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Función para cargar los datos
@st.cache_data
def cargar_datos():
    """Carga los datos desde un archivo CSV."""
    return pd.read_csv("estadisticas_acb_con_posicion.csv")

# Cargar los datos
df = cargar_datos()

# Mapeo de nombres de las columnas para que se vean en español
columnas_espanol = {
    "MIN": "Minutos",
    "Posición": "Posición",
    "Equipo": "Equipo",  # Asegúrate de que "Equipo" esté en el CSV
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

perfiles_posiciones = {
    "Base (PG)": {
        "Pass-First PG": {
            "AST%": 0.30,
            "PPR": 0.30,
            "STL%": 0.10,
            "eFG%": 0.05,
            "ORtg": 0.05,
            "Ast/TO": 0.15  # Agregada
        },
        "Scorer PG": {
            "PTS": 0.3,
            "3P%": 0.2,
            "AST%": 0.10,
            "STL%": 0.10,
            "TOV%": 0.15,
            "HOB": 0.20  # Agregada
        },
        "Two-Way PG": {
            "STL%": 0.30,
            "AST%": 0.20,
            "DRtg": 0.25,
            "TRB%": 0.15,
            "Stl/TO": 0.15  # Agregada
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
                st.warning(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row.get('Jugador', 'Desconocido')}. Valor: {row[stat]}")
    return puntuacion


def mostrar_jugadores_por_posicion(df_filtrado, equipo_seleccionado):
    # Filtrar jugadores del equipo seleccionado
    jugadores_equipo = df_filtrado[df_filtrado["Equipo"] == equipo_seleccionado]
    
    # Ordenar los jugadores por puntuación
    jugadores_equipo['Puntuacion'] = jugadores_equipo.apply(lambda row: calcular_puntuacion(row, perfiles_posiciones.get(row['Posición'], {})), axis=1)
    jugadores_equipo = jugadores_equipo.sort_values(by='Puntuacion', ascending=False)

    # Crear figura y configurarla
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')  # Fondo blanco
    ax.set_facecolor('white')  # Fondo blanco
    ax.axis('off')  # Quitar ejes

    # Coordenadas ajustadas para cada posición en una lista simple
    posiciones = {
        "Base (PG)": (5, 1.2),            # Centro abajo
        "Escolta (SG)": (1.5, 4),         # Arriba izquierda
        "Alero (SF)": (8, 4),             # Arriba derecha
        "Ala-Pívot (PF)": (2, 7),         # Centro arriba izquierda
        "Pívot (C)": (9, 7)               # Centro arriba derecha
    }

    # Tamaño de la fuente y color de los textos
    font_size = 10
    azul_color = "#1f77b4"

    # Crear la visualización con los jugadores
    for pos, (x, y) in posiciones.items():
        jugadores_posicion = jugadores_equipo[jugadores_equipo["Posición"] == pos].head(5)
        ax.text(x, y, pos, ha="center", va="center", fontsize=font_size, color="black", weight='bold')

        for idx, jugador in jugadores_posicion.iterrows():
            ax.text(x, y - (idx * 0.3), f"{jugador['Jugador']} - {jugador['Puntuacion']:.2f} puntos", ha="center", va="center", fontsize=font_size, color=azul_color, weight='bold')

    # Mostrar el gráfico
    st.pyplot(fig)


# Filtro adicional por equipo y posición
st.sidebar.header("Filtrar jugadores por equipo y posición")
equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo", ["Todos"] + df["Equipo"].unique().tolist())
posicion_seleccionada = st.sidebar.selectbox("Selecciona una posición", ["Todos"] + sorted(df["Posición"].unique()))

# Filtrar jugadores según el equipo y la posición seleccionados
df_filtrado = df
if equipo_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Equipo"] == equipo_seleccionado]
if posicion_seleccionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Posición"] == posicion_seleccionada]

# Mostrar los jugadores en imagen
mostrar_jugadores_por_posicion(df_filtrado, equipo_seleccionado)
