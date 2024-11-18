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
                [f"{jugador['Jugador']} - {jugador['Perfil Principal']}" for idx, jugador in jugadores_posicion.iterrows()]
            )

            # Colocar la lista en la coordenada correspondiente
            ax.text(x, y, lista_jugadores, ha="center", va="center", fontsize=font_size, color="black", weight='bold')

            # Ajustar la coordenada 'y' para la siguiente posición si hay más de un jugador
            y -= 2  # Ajustar para el siguiente jugador si hay más

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

# Función para obtener el perfil con más puntuación
def obtener_perfil_maximo(row, perfiles):
    """Obtiene el perfil con la puntuación más alta para una fila."""
    puntuaciones = {perfil: row.get(perfil, 0) for perfil in perfiles}
    return max(puntuaciones, key=puntuaciones.get)

# Obtener perfiles con más puntuación por posición
df_filtrado["Perfil Principal"] = df_filtrado.apply(
    lambda row: obtener_perfil_maximo(row, perfiles_posiciones[row["Posición"]].keys()),
    axis=1
)

# Filtro adicional por equipo y posición
st.sidebar.header("Filtrar jugadores por equipo y posición")
# Filtro de equipo
equipo_seleccionado = st.sidebar.selectbox("Selecciona un equipo", ["Todos"] + df["Equipo"].unique().tolist())

if equipo_seleccionado != "Todos":
    mostrar_jugadores_por_posicion(df_filtrado, equipo_seleccionado)

posicion_seleccionada = st.sidebar.selectbox("Selecciona una posición", ["Todos"] + sorted(df_filtrado["Posición"].unique()))

# Aplicar filtros
df_filtrado_equipo_posicion = df_filtrado.copy()
if equipo_seleccionado != "Todos":
    df_filtrado_equipo_posicion = df_filtrado_equipo_posicion[df_filtrado_equipo_posicion["Equipo"] == equipo_seleccionado]
if posicion_seleccionada != "Todos":
    df_filtrado_equipo_posicion = df_filtrado_equipo_posicion[df_filtrado_equipo_posicion["Posición"] == posicion_seleccionada]

# Mostrar resultados de jugadores filtrados en una nueva ventana
if st.button("Mostrar jugadores filtrados por equipo y posición"):
    with st.expander("Resultados Filtrados", expanded=True):
        st.write(f"Jugadores del equipo **{equipo_seleccionado}** en la posición **{posicion_seleccionada}**:")
        st.dataframe(df_filtrado_equipo_posicion[["Jugador", "Equipo", "Posición", "Perfil Principal"]])

# Mantener funcionalidades previas
# Mostrar tabla general
st.write("Tabla General de Jugadores con sus puntuaciones por perfil:")
perfil_columnas = [col for col in df_filtrado.columns if col not in ["Jugador", "Posición", "Minutos", "Equipo", "Perfil Principal"]]
st.write(df_filtrado[["Jugador", "Posición", "Equipo", "Perfil Principal"] + perfil_columnas])

# Mostrar los 5 mejores jugadores para cada posición y perfil seleccionado
# Para Base
perfil_base = st.sidebar.selectbox("Perfil Base (PG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Base (PG)"].keys()))
if perfil_base != "Selecciona un perfil":
    df_base = df_filtrado[df_filtrado["Posición"] == "Base (PG)"].sort_values(perfil_base, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_base}' en la posición Base (PG):")
    st.write(df_base[["Jugador", "Posición", perfil_base]])

# Para Escolta
perfil_escolta = st.sidebar.selectbox("Perfil Escolta (SG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Escolta (SG)"].keys()))
if perfil_escolta != "Selecciona un perfil":
    df_escolta = df_filtrado[df_filtrado["Posición"] == "Escolta (SG)"].sort_values(perfil_escolta, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_escolta}' en la posición Escolta (SG):")
    st.write(df_escolta[["Jugador", "Posición", perfil_escolta]])

# Para Alero
perfil_alero = st.sidebar.selectbox("Perfil Alero (SF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Alero (SF)"].keys()))
if perfil_alero != "Selecciona un perfil":
    df_alero = df_filtrado[df_filtrado["Posición"] == "Alero (SF)"].sort_values(perfil_alero, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_alero}' en la posición Alero (SF):")
    st.write(df_alero[["Jugador", "Posición", perfil_alero]])

# Para Ala-Pívot
perfil_ala_pivot = st.sidebar.selectbox("Perfil Ala-Pívot (PF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Ala-Pívot (PF)"].keys()))
if perfil_ala_pivot != "Selecciona un perfil":
    df_ala_pivot = df_filtrado[df_filtrado["Posición"] == "Ala-Pívot (PF)"].sort_values(perfil_ala_pivot, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_ala_pivot}' en la posición Ala-Pívot (PF):")
    st.write(df_ala_pivot[["Jugador", "Posición", perfil_ala_pivot]])

# Para Pívot
perfil_pivot = st.sidebar.selectbox("Perfil Pívot (C)", ["Selecciona un perfil"] + list(perfiles_posiciones["Pívot (C)"].keys()))
if perfil_pivot != "Selecciona un perfil":
    df_pivot = df_filtrado[df_filtrado["Posición"] == "Pívot (C)"].sort_values(perfil_pivot, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_pivot}' en la posición Pívot (C):")
    st.write(df_pivot[["Jugador", "Posición", perfil_pivot]])
