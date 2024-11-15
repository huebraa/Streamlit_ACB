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




# Función para generar una lista visual de los 5 mejores jugadores de la posición seleccionada
def generar_lista_imagen(df_filtrado, posicion, perfil):
    # Filtramos los jugadores por posición
    df_filtrado_pos = df_filtrado[df_filtrado["Posición"] == posicion]
    
    # Ordenamos por la puntuación del perfil seleccionado y tomamos los 5 mejores
    df_filtrado_pos = df_filtrado_pos.sort_values(by=f"Puntuacion {perfil}", ascending=False).head(5)
    
    # Creamos una imagen en blanco para la lista
    width, height = 300, 250  # Ajusta el tamaño según lo necesites
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Agregar título
    title = f"Top 5 - {posicion} ({perfil})"
    draw.text((10, 10), title, fill="black")

    # Definir la fuente
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    # Agregar la lista de jugadores
    y_offset = 40  # Espacio entre líneas
    for idx, row in df_filtrado_pos.iterrows():
        texto = f"{row['Jugador']} - {row[f'Puntuacion {perfil}']:.2f}"
        draw.text((10, y_offset), texto, fill="black", font=font)
        y_offset += 20  # Aumentar la distancia entre las líneas

    # Guardamos la imagen en un objeto de bytes para mostrarla en Streamlit
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Mostrar la imagen en Streamlit
    return img_byte_arr

# Filtros para elegir la posición y el perfil
posiciones = ["Base", "Escolta", "Alero", "Ala-Pívot", "Pívot"]
perfiles = ["Pass-First", "Scorer", "Two-Way"]

# Establecer un perfil por defecto para cada posición
perfiles_por_defecto = {
    "Base": "Pass-First",
    "Escolta": "Scorer",
    "Alero": "Two-Way",
    "Ala-Pívot": "Two-Way",
    "Pívot": "Two-Way"
}

# Mostrar la tabla de los 5 mejores para todas las posiciones
st.write("**Quinteto ideal por posición y perfil**")

# Generar y mostrar las imágenes para cada posición
for posicion in posiciones:
    perfil = perfiles_por_defecto[posicion]  # Obtener el perfil predeterminado para la posición
    st.write(f"### {posicion}: {perfil}")
    
    # Generar la imagen
    img_byte_arr = generar_lista_imagen(df, posicion, perfil)
    
    # Mostrar la imagen generada para esa posición
    st.image(img_byte_arr, caption=f"Los 5 mejores jugadores de {posicion} ({perfil})", use_column_width=True)
