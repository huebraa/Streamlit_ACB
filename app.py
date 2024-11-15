import pandas as pd

# Cargar datos
df = pd.read_csv("estadisticas_completas.csv")

# Renombrar las columnas a español si no se ha hecho
columnas_espanol = {
    "MIN": "Minutos",
    "AST%": "Asistencias",
    "USG%": "Uso",
    "PPR": "Pases_por_posicion",
    "STL%": "Robos",
    "eFG%": "Porcentaje_Tiro_Campo",
    "3P%": "Porcentaje_3P"
}

df = df.rename(columns=columnas_espanol)

# Crear una columna de perfil para el base (PG) con pesos para cada estadística
def calcular_perfil_base(row):
    # Pesos definidos previamente
    pesos = {
        "Asistencias": 0.30,
        "Uso": 0.15,
        "Pases_por_posicion": 0.20,
        "Robos": 0.10,
        "Porcentaje_Tiro_Campo": 0.10,
        "Porcentaje_3P": 0.10
    }
    
    # Calculamos el perfil del jugador para la posición Base (PG)
    perfil = (
        row["Asistencias"] * pesos["Asistencias"] +
        row["Uso"] * pesos["Uso"] +
        row["Pases_por_posicion"] * pesos["Pases_por_posicion"] +
        row["Robos"] * pesos["Robos"] +
        row["Porcentaje_Tiro_Campo"] * pesos["Porcentaje_Tiro_Campo"] +
        row["Porcentaje_3P"] * pesos["Porcentaje_3P"]
    )
    
    return perfil

# Aplicar el cálculo del perfil
df["Perfil_Base"] = df.apply(calcular_perfil_base, axis=1)

# Mostrar los mejores jugadores para la posición Base (PG) ordenados por el perfil
df_base = df[df["Posición"] == "PG"]
df_base_sorted = df_base.sort_values(by="Perfil_Base", ascending=False)

# Mostrar los primeros jugadores
st.write("Los mejores jugadores para la posición Base (PG) según el perfil:")
st.dataframe(df_base_sorted[["Jugador", "Perfil_Base", "Asistencias", "Uso", "Pases_por_posicion", "Robos", "Porcentaje_Tiro_Campo", "Porcentaje_3P"]])

