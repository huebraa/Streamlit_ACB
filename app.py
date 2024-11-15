import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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
    "Posición": "Posición"
}

# Renombrar las columnas
df = df.rename(columns=columnas_espanol)

# Función para dibujar la cancha de baloncesto
def dibujar_canchabasket():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Crear la cancha
    cancha = patches.Rectangle((0, 0), 28, 15, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(cancha)
    
    # Línea de medio campo
    linea_media = plt.Line2D([14, 14], [0, 15], color='black', linewidth=2)
    ax.add_line(linea_media)
    
    # Círculo central
    circulo_central = patches.Circle((14, 7.5), 1, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(circulo_central)
    
    # Arco de 3 puntos
    arco_3p = patches.Arc((14, 7.5), 14, 14, theta1=0, theta2=180, color="black", linewidth=2)
    ax.add_patch(arco_3p)
    
    # Áreas de tiro libre
    area_tiro_libre_izq = patches.Rectangle((1, 3), 3, 5.5, linewidth=2, edgecolor='black', facecolor='none')
    area_tiro_libre_der = patches.Rectangle((24, 3), 3, 5.5, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(area_tiro_libre_izq)
    ax.add_patch(area_tiro_libre_der)
    
    # Círculos de tiro libre
    tiro_libre_izq = patches.Circle((4, 6.5), 0.75, linewidth=2, edgecolor='black', facecolor='none')
    tiro_libre_der = patches.Circle((24, 6.5), 0.75, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(tiro_libre_izq)
    ax.add_patch(tiro_libre_der)
    
    # Ajustes visuales
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 15)
    ax.set_title("Media Cancha de Baloncesto")
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig, ax

# Mostrar la cancha de baloncesto
fig, ax = dibujar_canchabasket()

# Título de la aplicación
st.title("Estadísticas de Jugadores - Liga ACB")

# Mostrar las posiciones disponibles
posiciones = df["Posición"].unique()
posicion = st.selectbox("Selecciona una posición:", posiciones)

# Filtrar los jugadores por la posición seleccionada
df_filtrado = df[df["Posición"] == posicion]

# Asignar una posición a los jugadores en la cancha (según el perfil)
for i, jugador in df_filtrado.iterrows():
    x = 7  # Posición horizontal por defecto (puedes ajustarlo más adelante)
    y = 7.5  # Posición vertical por defecto (centro de la cancha)
    
    # Asignamos la posición en la cancha (dependiendo de la posición del jugador)
    if jugador['Posición'] == 'Base':
        x = 4  # Base en la parte superior
    elif jugador['Posición'] == 'Escolta':
        x = 10  # Escolta en el medio
    elif jugador['Posición'] == 'Alero':
        x = 14  # Alero en el centro
    elif jugador['Posición'] == 'Ala-Pívot':
        x = 18  # Ala-Pívot más cerca de la canasta
    elif jugador['Posición'] == 'Pívot':
        x = 24  # Pívot cerca de la canasta

    # Agregar a los jugadores en la cancha como puntos
    ax.plot(x, y, 'o', markersize=12, label=jugador['Posición'])

# Mostrar la cancha con los jugadores
st.pyplot(fig)

# Ahora que mostramos la cancha con los jugadores, podemos permitir que el usuario elija pesos para el perfil de los jugadores.

# Aquí puedes agregar un control para que el usuario seleccione el peso de cada estadística (por ejemplo, puntos, rebotes, asistencias, etc.)
peso_puntos = st.slider("Peso de los puntos:", 0.0, 1.0, 0.5)
peso_rebotes = st.slider("Peso de los rebotes:", 0.0, 1.0, 0.5)
peso_asistencias = st.slider("Peso de las asistencias:", 0.0, 1.0, 0.5)

# Estos pesos se pueden usar luego para crear un perfil de jugador más detallado según el gusto del usuario
