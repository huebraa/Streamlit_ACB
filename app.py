import pandas as pd
import streamlit as st

# Cargar los datos
df = pd.read_csv("estadisticas_completas.csv")

# Añadir los filtros de la barra lateral para filtrar por minutos (minutos jugados)
min_min = df["MIN"].astype(float).min()
min_max = df["MIN"].astype(float).max()

min_filter = st.sidebar.slider("Filtrar por minutos jugados", min_min, min_max, (min_min, min_max))

# Filtrar los datos en función de los minutos seleccionados
df_filtrado = df[(df["MIN"].astype(float) >= min_filter[0]) & (df["MIN"].astype(float) <= min_filter[1])]

# Mostrar los datos filtrados
st.write("Datos filtrados por minutos jugados:", df_filtrado)

# Mostrar estadísticas agregadas para los datos filtrados
st.write(f"Promedio de puntos por jugador: {df_filtrado['PTS'].astype(float).mean():.2f}")
st.write(f"Promedio de asistencias por jugador: {df_filtrado['AST%'].astype(float).mean():.2f}")
st.write(f"Promedio de rebotes por jugador: {df_filtrado['TRB%'].astype(float).mean():.2f}")
st.write(f"Promedio de robos por jugador: {df_filtrado['STL%'].astype(float).mean():.2f}")
st.write(f"Promedio de porcentaje de tiro de campo por jugador: {df_filtrado['eFG%'].astype(float).mean():.2f}")
st.write(f"Promedio de porcentaje de 3 puntos por jugador: {df_filtrado['3P%'].astype(float).mean():.2f}")

# Crear una columna de perfil para el base (PG) con pesos para cada estadística
def calcular_perfil_base(row):
    # Pesos definidos previamente para la posición Base (PG)
    pesos = {
        "AST%": 0.30,           # Asistencias (AST%)
        "USG%": 0.15,           # Uso de balón (USG%)
        "PPR": 0.20,            # Pases por posesión (PPR)
        "STL%": 0.10,           # Robos (STL%)
        "eFG%": 0.10,           # Porcentaje de tiro de campo (eFG%)
        "3P%": 0.10             # Porcentaje de 3 puntos (3P%)
    }
    
    # Calculamos el perfil del jugador para la posición Base (PG)
    perfil = (
        row["AST%"] * pesos["AST%"] +
        row["USG%"] * pesos["USG%"] +
        row["PPR"] * pesos["PPR"] +
        row["STL%"] * pesos["STL%"] +
        row["eFG%"] * pesos["eFG%"] +
        row["3P%"] * pesos["3P%"]
    )
    
    return perfil

# Aplicar el cálculo del perfil para Base (PG)
df["Perfil_Base"] = df.apply(calcular_perfil_base, axis=1)

# Filtrar para mostrar solo los jugadores que son bases (PG)
df_base = df[df["Posición"] == "PG"]

# Ordenar a los jugadores de la posición Base por el perfil calculado
df_base_sorted = df_base.sort_values(by="Perfil_Base", ascending=False)

# Mostrar los mejores jugadores para la posición Base (PG) ordenados por el perfil
st.write("Los mejores jugadores para la posición Base (PG) según el perfil:")
st.dataframe(df_base_sorted[["Jugador", "Perfil_Base", "AST%", "USG%", "PPR", "STL%", "eFG%", "3P%"]])

# Mostrar el perfil completo de los jugadores de la posición Base
st.write("Detalles de los jugadores de la posición Base (PG):")
st.dataframe(df_base_sorted)

# Mostrar el perfil de los jugadores en la posición seleccionada
posiciones = ["PG", "SG", "SF", "PF", "C"]
posicion = st.selectbox("Filtrar por posición:", opciones=posiciones)

# Filtrar los jugadores por la posición seleccionada
df_posicion = df[df["Posición"] == posicion]

# Ordenar los jugadores por el perfil en la posición seleccionada
df_posicion_sorted = df_posicion.sort_values(by="Perfil_Base", ascending=False)

# Mostrar los jugadores filtrados por la posición seleccionada
st.write(f"Los mejores jugadores para la posición {posicion} según el perfil:")
st.dataframe(df_posicion_sorted[["Jugador", "Perfil_Base", "AST%", "USG%", "PPR", "STL%", "eFG%", "3P%"]])
