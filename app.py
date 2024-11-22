
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
    "PF": "PF",
    "TS%" : "TS%",
}

# Renombrar las columnas
df = df.rename(columns=columnas_espanol)

perfiles_posiciones = {
"Base (PG)": {
"Pass-First PG": {
"AST%": 0.25,
"PPR": 0.4,
"TS%": 0.10,
"eFG%": 0.05,
"ORtg": 0.05,
"Ast/TO": 0.15  # Agregada
},
"Scorer PG": {
"PTS": 0.25,
"ORtg": 0.5,
"HOB": 0.25  # Agregada
},
"Defensive PG": {
"STL%": 0.15,
"Stl/TO": 0.15,
"DRtg": 0.5,
"TRB%": 0.15,
"BLK%": 0.15  # Agregada
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


# Definir las estadísticas que deben ser tratadas de manera inversa
estadisticas_inversas = {"DRtg", "TOV%", "PF"}  # Agrega todas las estadísticas que son inversas

# Normalización de estadísticas a percentiles por posición
estadisticas_relevantes = set(
    stat for perfiles in perfiles_posiciones.values() for perfil in perfiles.values() for stat in perfil.keys()
)



# Calcular percentiles dentro de cada posición para las estadísticas relevantes
for stat in estadisticas_relevantes:
    if stat in df:  # Asegúrate de que la estadística está en el DataFrame
        
        # Calcular el valor mínimo y máximo de cada estadística dentro de cada posición
        min_stat = df.groupby("Posición")[stat].transform('min')
        max_stat = df.groupby("Posición")[stat].transform('max')
        
        # Si la estadística es inversa, aplicamos la fórmula de percentil inverso
        if stat in estadisticas_inversas:
            df[stat] = ((max_stat - df[stat]) / (max_stat - min_stat)) * 100
        else:
            # Si no es inversa, aplicamos la fórmula de percentil normal
            df[stat] = ((df[stat] - min_stat) / (max_stat - min_stat)) * 100



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




def mostrar_jugadores_por_posiciones_y_perfiles(df_filtrado, perfiles_seleccionados, max_jugadores):
    """
    Muestra jugadores destacados organizados por posición en una imagen,
    según los perfiles seleccionados para cada posición.
    """
    # URL de la imagen de fondo en GitHub (esto es un ejemplo)
    url_imagen = 'https://github.com/huebraa/Streamlit_ACB/edit/main/app.py#L9C23:~:text=estadisticas_acb_con_posicion.csv-,pista,-%2Dacb.png'

    # Cargar la imagen de fondo
    img_fondo = mpimg.imread(url_imagen)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img_fondo, aspect='auto', extent=[0, 10, 0, 10])  # Ajustar la imagen al tamaño de la gráfica
    ax.axis('off')  # Quitar ejes

    # Coordenadas ajustadas para cada posición
    posiciones_coordenadas = {
        "Base (PG)": (5, 1.2),            # Centro abajo
        "Escolta (SG)": (2, 3),         # Arriba izquierda
        "Alero (SF)": (7.5, 3.5),             # Arriba derecha
        "Ala-Pívot (PF)": (2.5, 4.5),     # Arriba izquierda más alto
        "Pívot (C)": (6, 5.5)             # Arriba derecha más alto
    }

    # Tamaño de fuente y color
    font_size = 44
    azul_color = '#1f77b4'

    # Recorrer cada posición seleccionada y mostrar jugadores
    for posicion, (x, y) in posiciones_coordenadas.items():
        perfil_seleccionado = perfiles_seleccionados.get(posicion)
        
        # Si se ha seleccionado un perfil para esta posición
        if perfil_seleccionado and perfil_seleccionado != "Selecciona un perfil":
            # Filtrar y ordenar jugadores por el perfil seleccionado
            jugadores_posicion = (
                df_filtrado[df_filtrado["Posición"] == posicion]
                .sort_values(perfil_seleccionado, ascending=False)
                .head(max_jugadores)  # Ajuste dinámico del número de jugadores
            )

            # Título de la posición
            ax.text(x, y + 0.1, f"{posicion} - {perfil_seleccionado}", 
                    ha="center", va="center", fontsize=44, color="black", weight='bold')

            # Lista de jugadores
            if not jugadores_posicion.empty:
                lista_jugadores = "\n".join(
                    [f"{jugador['Jugador']} ({jugador[perfil_seleccionado]:.2f})"
                     for idx, jugador in jugadores_posicion.iterrows()]
                )
                ax.text(x, y, lista_jugadores, ha="center", va="top", fontsize=font_size, color=azul_color)
            else:
                ax.text(x, y, "Sin jugadores destacados", ha="center", va="top", fontsize=font_size, color="gray")

    # Título general centrado arriba
    ax.text(5, 9, "Jugadores destacados por posición y perfil seleccionado", 
            ha="center", va="center", fontsize=24, color="black", weight='bold')

    # Mostrar imagen
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

import matplotlib.pyplot as plt

def mostrar_jugadores_por_posiciones_y_perfiles(df_filtrado, perfiles_seleccionados, max_jugadores):
    """
    Muestra jugadores destacados organizados por posición en una imagen,
    según los perfiles seleccionados para cada posición.
    """
    # Crear figura
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('white')  # Fondo blanco
    ax.set_facecolor('white')  # Fondo blanco
    ax.axis('off')  # Quitar ejes

    # Coordenadas ajustadas para cada posición
    posiciones_coordenadas = {
        "Base (PG)": (5, 1.2),            # Centro abajo
        "Escolta (SG)": (2, 3),         # Arriba izquierda
        "Alero (SF)": (7.5, 3.5),             # Arriba derecha
        "Ala-Pívot (PF)": (2.5, 4.5),     # Arriba izquierda más alto
        "Pívot (C)": (6, 5.5)             # Arriba derecha más alto
    }

    # Tamaño de fuente y color
    font_size = 44
    azul_color = '#1f77b4'

    # Recorrer cada posición seleccionada y mostrar jugadores
    for posicion, (x, y) in posiciones_coordenadas.items():
        perfil_seleccionado = perfiles_seleccionados.get(posicion)
        
        # Si se ha seleccionado un perfil para esta posición
        if perfil_seleccionado and perfil_seleccionado != "Selecciona un perfil":
            # Filtrar y ordenar jugadores por el perfil seleccionado
            jugadores_posicion = (
                df_filtrado[df_filtrado["Posición"] == posicion]
                .sort_values(perfil_seleccionado, ascending=False)
                .head(max_jugadores)  # Ajuste dinámico del número de jugadores
            )

            # Título de la posición
            ax.text(x, y + 0.1, f"{posicion} - {perfil_seleccionado}", 
                    ha="center", va="center", fontsize=44, color="black", weight='bold')

            # Lista de jugadores
            if not jugadores_posicion.empty:
                lista_jugadores = "\n".join(
                    [f"{jugador['Jugador']} ({jugador[perfil_seleccionado]:.2f})"
                     for idx, jugador in jugadores_posicion.iterrows()]
                )
                ax.text(x, y, lista_jugadores, ha="center", va="top", fontsize=font_size, color=azul_color)
            else:
                ax.text(x, y, "Sin jugadores destacados", ha="center", va="top", fontsize=font_size, color="gray")

    # Título general centrado arriba
    ax.text(5, 9, "Jugadores destacados por posición y perfil seleccionado", 
            ha="center", va="center", fontsize=24, color="black", weight='bold')

    # Mostrar imagen
    st.pyplot(fig)

# Configurar slider para seleccionar el número de jugadores destacados
st.sidebar.header("Opciones adicionales")
max_jugadores = st.sidebar.slider(
    "Número de jugadores destacados por posición",
    min_value=1,
    max_value=10,
    value=5,
    step=1
)

# Selección de perfiles desde la barra lateral (con valores por defecto)
perfiles_seleccionados = {}
st.sidebar.header("Selecciona un perfil para cada posición")
for posicion, perfiles in perfiles_posiciones.items():
    perfiles_seleccionados[posicion] = st.sidebar.selectbox(
        f"Perfil {posicion}",
        list(perfiles.keys()),  # Seleccionar el primer perfil por defecto
    )




# Mostrar jugadores por posición según perfiles seleccionados y número máximo
mostrar_jugadores_por_posiciones_y_perfiles(df_filtrado, perfiles_seleccionados, max_jugadores)
