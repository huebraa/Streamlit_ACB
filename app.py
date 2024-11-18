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


# Función para obtener los 5 mejores jugadores por perfil
def obtener_top_5_jugadores(df, posicion, perfil):
    """Obtiene los 5 mejores jugadores para un perfil en una posición específica"""
    # Ordenar jugadores según la puntuación del perfil y seleccionar los primeros 5
    df_posicion = df[df["Posición"] == posicion]
    df_posicion["Puntuacion"] = df_posicion.apply(lambda row: calcular_puntuacion(row, perfil), axis=1)
    df_posicion = df_posicion.sort_values("Puntuacion", ascending=False).head(5)
    return df_posicion

# Función para mostrar los jugadores de cada posición en un gráfico
def mostrar_top_5_jugadores(df_filtrado, perfil_seleccionado, posicion):
    # Crear figura y configurarla
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')  # Fondo blanco
    ax.set_facecolor('white')  # Fondo blanco
    ax.axis('off')  # Quitar ejes

    # Coordenadas ajustadas para cada posición en una lista simple
    posiciones = {
        "Base (PG)": (5, 1.2),
        "Escolta (SG)": (1.5, 4),
        "Alero (SF)": (8, 4),
        "Ala-Pívot (PF)": (1.5, 5.5),
        "Pívot (C)": (8, 5.5)
    }

    # Tamaño de fuente ajustado a 14
    font_size = 14
    azul_color = '#1f77b4'  # Tono azul

    # Mostrar la lista de los 5 mejores jugadores para cada posición y perfil
    jugadores_top_5 = obtener_top_5_jugadores(df_filtrado, posicion, perfiles_posiciones[posicion][perfil_seleccionado])

    # Título de la posición
    ax.text(0.5, 1.1, f"Top 5 {perfil_seleccionado} en la posición {posicion}", ha="center", va="center", fontsize=16, color="black", weight='bold')

    # Mostrar los jugadores
    lista_jugadores = "\n".join([f"{jugador['Jugador']} - {jugador['Puntuacion']:.2f} puntos" for idx, jugador in jugadores_top_5.iterrows()])
    ax.text(0.5, 0.5, lista_jugadores, ha="center", va="center", fontsize=font_size, color=azul_color, weight='bold')

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

# Filtro de perfil
perfil_seleccionado = st.sidebar.selectbox("Selecciona un perfil", ["Selecciona un perfil"] + list(perfiles_posiciones.get(posicion_seleccionada, {}).keys()))

# Mostrar los top 5 jugadores por perfil si el usuario ha seleccionado un perfil
if perfil_seleccionado != "Selecciona un perfil":
    mostrar_top_5_jugadores(df_filtrado, perfil_seleccionado, posicion_seleccionada)
