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
                valor = float(row[stat]) if isinstance(row[stat], (int, float)) else 0  # Verifica que sea numérico
                puntuacion += valor * peso
            except ValueError:
                st.warning(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row.get('Jugador', 'Desconocido')}. Valor: {row[stat]}")
    return puntuacion

# Función para obtener el perfil con mayor puntuación
def obtener_perfil_maximo(row, perfiles):
    """Obtiene el perfil con la puntuación más alta para una fila."""
    puntuaciones = {perfil: row.get(perfil, 0) for perfil in perfiles}
    return max(puntuaciones, key=puntuaciones.get)

# Mostrar jugadores por posición
def mostrar_jugadores_por_posicion(df_filtrado, equipo_seleccionado):
    # Filtrar jugadores del equipo seleccionado
    jugadores_equipo = df_filtrado[df_filtrado["Equipo"] == equipo_seleccionado]
    
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
        "Ala-Pívot (PF)": (1.5, 5.5),     # Arriba izquierda más alto
        "Pívot (C)": (8, 5.5)             # Arriba derecha más alto
    }

    # Tamaño de fuente ajustado a 44
    font_size = 44
    azul_color = '#1f77b4'  # Tono azul

    # Recorrer cada posición y mostrar los jugadores
    for posicion, (x, y) in posiciones.items():
        # Título de la posición
        ax.text(x, y + 0.2, posicion, ha="center", va="center", fontsize=font_size, color="black", weight='bold')

        # Obtener los jugadores de esta posición
        jugadores_posicion = jugadores_equipo[jugadores_equipo["Posición"] == posicion]
        if not jugadores_posicion.empty:
            # Obtener el perfil con mayor puntuación para cada jugador
            jugadores_posicion["Perfil Principal"] = jugadores_posicion.apply(
                lambda row: obtener_perfil_maximo(row, perfiles_posiciones[row["Posición"]].keys()),
                axis=1
            )
            
            # Mostrar los jugadores en formato de lista minimalista
            lista_jugadores = "\n".join(
                [f"{jugador['Jugador']} - {jugador['Perfil Principal']} - #{jugador.get('Ranking Liga', 'N/A')}" 
                 for idx, jugador in jugadores_posicion.iterrows()]
            )

            # Colocar la lista en la coordenada correspondiente
            ax.text(x, y, lista_jugadores, ha="center", va="center", fontsize=font_size, color=azul_color, weight='bold')

            # Ajustar la coordenada 'y' para la siguiente posición si hay más de un jugador
            y -= 2  # Ajustar para el siguiente jugador si hay más

        else:
            # Si no hay jugadores, mostrar un mensaje
            ax.text(x, y, "Sin jugadores en esta posición", ha="center", va="center", fontsize=font_size, color="red", weight='bold')
            y -= 2

    # Título general
    ax.set_title(f"Jugadores del equipo {equipo_seleccionado} por posición", fontsize=20, color="black", weight='bold')

    # Mostrar
    st.pyplot(fig)

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

# Filtrar por equipo
st.sidebar.header("Filtrar jugadores por equipo y posición")
equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo", ["Todos"] + df["Equipo"].unique().tolist())

if equipo_seleccionado != "Todos":
    mostrar_jugadores_por_posicion(df_filtrado, equipo_seleccionado)
else:
    for equipo in df["Equipo"].unique():
        mostrar_jugadores_por_posicion(df_filtrado, equipo)
