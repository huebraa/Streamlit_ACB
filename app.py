import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    # (Agregar los demás perfiles aquí de la misma manera)
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
                st.warning(f"Advertencia: No se pudo convertir el valor de {stat} para el jugador {row['Jugador']}. Valor: {row[stat]}")
    return puntuacion

# Filtro de mínimo de minutos
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

# Selección del rol y perfil predeterminado (Base PG - Pass-First PG)
posicion_predeterminada = "Base (PG)"
perfil_predeterminado = "Pass-First PG"

# Selección del jugador con la mejor puntuación en el perfil predeterminado
jugador_top = df_filtrado[df_filtrado["Posición"] == posicion_predeterminada].sort_values(perfil_predeterminado, ascending=False).iloc[0]

# Métricas relevantes para el perfil
perfil_metrica = perfiles_posiciones[posicion_predeterminada][perfil_predeterminado]
metricas = list(perfil_metrica.keys())
pesos = list(perfil_metrica.values())
valores = [jugador_top[metrica] for metrica in metricas]

# Crear radar plot
def radar_chart(metrics, values, title, weights=None):
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    
    # Asegurar el cierre del radar plot
    values += values[:1]
    angles += angles[:1]

    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2, label="Jugador")
    
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], color='gray', fontsize=10)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=12)
    
    if weights:
        for i, weight in enumerate(weights):
            ax.text(angles[i], values[i] + 5, f"{weight:.2f}", fontsize=10, ha='center', va='center', color='red')

    ax.set_title(title, fontsize=15, pad=20)
    plt.legend()
    plt.show()

# Generar gráfico para el jugador seleccionado
radar_chart(
    metrics=metricas,
    values=valores,
    title=f"Perfil {perfil_predeterminado} - {jugador_top['Jugador']}",
    weights=pesos
)

# Mostrar tabla de puntuaciones
st.write("Tabla General de Jugadores con sus puntuaciones por perfil:")
perfil_columnas = [col for col in df_filtrado.columns if col not in ["Jugador", "Posición", "Minutos"]]  # Filtrar columnas de puntuaciones
st.write(df_filtrado[["Jugador", "Posición"] + perfil_columnas])

# Mostrar los 5 mejores jugadores para cada posición y perfil seleccionado
# Para Base
if perfil_predeterminado != "Selecciona un perfil":
    df_base = df_filtrado[df_filtrado["Posición"] == posicion_predeterminada].sort_values(perfil_predeterminada, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_predeterminada}' en la posición Base (PG):")
    st.write(df_base[["Jugador", "Posición", perfil_predeterminada]])
