import pandas as pd
import streamlit as st

# Cargar los datos
df = pd.read_csv("estadisticas_completas.csv")

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

# Aplicar el cálculo del perfil
df["Perfil_Base"] = df.apply(calcular_perfil_base, axis=1)

# Filtrar para mostrar solo los jugadores que son bases (PG)
df_base = df[df["Posición"] == "PG"]

# Ordenar a los jugadores de la posición Base por el perfil calculado
df_base_sorted = df_base.sort_values(by="Perfil_Base", ascending=False)

# Mostrar los mejores jugadores para la posición Base (PG) ordenados por el perfil
st.title("Perfiles de Jugadores - Posición Base (PG)")
st.write("Los mejores jugadores para la posición Base (PG) según el perfil:")
st.dataframe(df_base_sorted[["Jugador", "Perfil_Base", "AST%", "USG%", "PPR", "STL%", "eFG%", "3P%"]])


