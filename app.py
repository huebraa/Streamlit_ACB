import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

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

# Definir los pesos para cada perfil
perfil_pass_first = {
    "AST%": 0.2,
    "PPR": 0.40,  # Vamos a calcular esta métrica a partir de AST% y USG%
    "STL%": 0.15,
    "eFG%": 0.15,
    "ORtg": 0.10,
    "TOV%": 0.05
}

perfil_scorer = {
    "ORtg": 0.40,
    "3P%": 0.25,
    "eFG%": 0.15,
    "AST%": 0.10,
    "STL%": 0.05,
    "TOV%": 0.05
}

perfil_two_way = {
    "AST%": 0.15,
    "DRtg": 0.40,
    "STL%": 0.15,
    "TRB%": 0.10,
    "eFG%": 0.10,
    "TOV%": 0.10
}

# Función para calcular la puntuación de cada perfil
def calcular_puntuacion(row, perfil):
    puntuacion = 0
    # Si existe la columna "AST%" y "USG%", calculamos "AST/USG"
    if "AST%" in row and "USG%" in row:
        ast_usg = row["AST%"] / row["USG%"]  # Calcular AST/USG
        row["AST/USG"] = ast_usg  # Asignar esta métrica al dataframe (de forma temporal)
    
    # Iterar sobre cada estadística y su peso
    for stat, peso in perfil.items():
        # Verificar si la estadística existe en el dataframe
        if stat in row:
            try:
                valor = float(row[stat])
                puntuacion += valor * peso
            except ValueError:
                st.write(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row['Jugador']}. Valor: {row[stat]}")
        else:
            st.write(f"Advertencia: La columna {stat} no se encuentra en la fila del jugador {row['Jugador']}")
    
    return puntuacion

# Calcular las puntuaciones para todos los jugadores
df["Puntuacion Pass-First"] = df.apply(lambda row: calcular_puntuacion(row, perfil_pass_first), axis=1)
df["Puntuacion Scorer"] = df.apply(lambda row: calcular_puntuacion(row, perfil_scorer), axis=1)
df["Puntuacion Two-Way"] = df.apply(lambda row: calcular_puntuacion(row, perfil_two_way), axis=1)

# Función para generar una lista visual de los 5 mejores jugadores de la posición seleccionada
def generar_lista_imagen(df_filtrado, posicion, perfil):
    # Filtramos los jugadores por posición
    df_filtrado_pos = df_filtrado[df_filtrado["Posición"] == posicion]
    
    # Ordenamos por la puntuación del perfil seleccionado y tomamos los 5 mejores
    df_filtrado_pos = df_filtrado_pos.sort_values(by=f"Puntuacion {perfil}", ascending=False).head(5)
    
    # Creamos una imagen en blanco para la lista
    width, height = 600, 250  # Ajusta el tamaño según lo necesites
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
    st.image(img_byte_arr, caption=f"Los 5 mejores jugadores de {posicion} ({perfil})", use_column_width=True)

# Filtros para elegir la posición y el perfil
posiciones = ["Base", "Escolta", "Alero", "Ala-Pívot", "Pívot"]
perfil_seleccionado = st.selectbox("Selecciona un perfil", ["Pass-First", "Scorer", "Two-Way"])
posicion_seleccionada = st.selectbox("Selecciona una posición", posiciones)

# Mostrar la lista de los 5 mejores jugadores por posición y perfil
generar_lista_imagen(df, posicion_seleccionada, perfil_seleccionado)
