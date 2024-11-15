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

# Función para dibujar la cancha
def dibujar_canchabasket():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    cancha = patches.Rectangle((0, 0), 28, 15, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(cancha)
    
    linea_media = plt.Line2D([14, 14], [0, 15], color='black', linewidth=2)
    ax.add_line(linea_media)
    
    circulo_central = patches.Circle((14, 7.5), 1, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(circulo_central)
    
    arco_3p = patches.Arc((14, 7.5), 14, 14, theta1=0, theta2=180, color="black", linewidth=2)
    ax.add_patch(arco_3p)
    
    area_tiro_libre_izq = patches.Rectangle((1, 3), 3, 5.5, linewidth=2, edgecolor='black', facecolor='none')
    area_tiro_libre_der = patches.Rectangle((24, 3), 3, 5.5, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(area_tiro_libre_izq)
    ax.add_patch(area_tiro_libre_der)
    
    tiro_libre_izq = patches.Circle((4, 6.5), 0.75, linewidth=2, edgecolor='black', facecolor='none')
    tiro_libre_der = patches.Circle((24, 6.5), 0.75, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(tiro_libre_izq)
    ax.add_patch(tiro_libre_der)
    
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 15)
    ax.set_title("Media Cancha de Baloncesto")
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig, ax

# Mostrar la cancha de baloncesto
fig, ax = dibujar_canchabasket()

# Mostrar las posiciones disponibles
posiciones = df["Posición"].unique()
posicion = st.selectbox("Selecciona una posición:", posiciones)

# Filtrar los jugadores por posición
df_filtrado = df[df["Posición"] == posicion]

# Asignar una posición a los jugadores en la cancha (simplemente los colocamos en líneas horizontales según el peso)
for i, jugador in df_filtrado.iterrows():
    x = 7  # Default horizontal position (could adjust depending on the player)
    y = 7.5  # Default vertical position (middle of the court)
    
    # Asignamos la posición en la cancha (dependiendo de la posición del jugador y peso)
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

