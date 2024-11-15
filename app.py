import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para cargar los datos
@st.cache_data
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
    # Añadir el resto de posiciones y perfiles como en el código original...
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

# Filtros para cada posición
perfil_base = st.sidebar.selectbox("Perfil Base (PG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Base (PG)"].keys()))
perfil_escolta = st.sidebar.selectbox("Perfil Escolta (SG)", ["Selecciona un perfil"] + list(perfiles_posiciones["Escolta (SG)"].keys()))
perfil_alero = st.sidebar.selectbox("Perfil Alero (SF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Alero (SF)"].keys()))
perfil_ala_pivot = st.sidebar.selectbox("Perfil Ala-Pívot (PF)", ["Selecciona un perfil"] + list(perfiles_posiciones["Ala-Pívot (PF)"].keys()))
perfil_pivot = st.sidebar.selectbox("Perfil Pívot (C)", ["Selecciona un perfil"] + list(perfiles_posiciones["Pívot (C)"].keys()))

# Generar imagen con matplotlib para mostrar los mejores jugadores
def mostrar_mejores_jugadores():
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.axis("off")
    y_pos = 1.0
    
    # Mostrar los mejores jugadores de cada perfil seleccionado
    for posicion, perfil, perfil_col in [
        ("Base (PG)", perfil_base, "Perfil Base"),
        ("Escolta (SG)", perfil_escolta, "Perfil Escolta"),
        ("Alero (SF)", perfil_alero, "Perfil Alero"),
        ("Ala-Pívot (PF)", perfil_ala_pivot, "Perfil Ala-Pívot"),
        ("Pívot (C)", perfil_pivot, "Perfil Pívot")
    ]:
        if perfil != "Selecciona un perfil":
            top_jugadores = df_filtrado[df_filtrado["Posición"] == posicion].sort_values(perfil, ascending=False).head(5)
            ax.text(0.5, y_pos, f"{perfil_col} - {perfil}", ha='center', va='top', weight='bold', fontsize=12, color="brown", transform=ax.transAxes)
            y_pos -= 0.05
            
            for _, row in top_jugadores.iterrows():
                jugador_texto = f"{row['Jugador']} ({row['Posición']}) - {row[perfil]:.2f}"
                ax.text(0.5, y_pos, jugador_texto, ha='center', va='top', fontsize=10, color="black", transform=ax.transAxes)
                y_pos -= 0.03
            y_pos -= 0.05  # Espacio adicional entre posiciones

    st.pyplot(fig)

# Mostrar la tabla visual de los mejores jugadores
mostrar_mejores_jugadores()
