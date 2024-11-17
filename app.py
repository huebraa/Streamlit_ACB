import matplotlib.pyplot as plt

# Función para generar y mostrar una imagen con los 5 mejores jugadores
def mostrar_top5_imagen(df, posicion, perfil, titulo):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis("off")  # Quitar los ejes
    ax.set_title(titulo, fontsize=16, weight="bold")

    # Crear tabla dentro del gráfico
    tabla = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center"
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.auto_set_column_width(col=list(range(len(df.columns))))  # Ajustar columnas

    # Mostrar la imagen en Streamlit
    st.pyplot(fig)

# Mostrar los 5 mejores jugadores para cada posición y perfil seleccionado en forma de imagen
if perfil_base != "Selecciona un perfil":
    df_base = df_filtrado[df_filtrado["Posición"] == "Base (PG)"].sort_values(perfil_base, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_base}' en la posición Base (PG):")
    mostrar_top5_imagen(df_base[["Jugador", "Posición", perfil_base]], "Base (PG)", perfil_base, f"Top 5 Base (PG) - {perfil_base}")

if perfil_escolta != "Selecciona un perfil":
    df_escolta = df_filtrado[df_filtrado["Posición"] == "Escolta (SG)"].sort_values(perfil_escolta, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_escolta}' en la posición Escolta (SG):")
    mostrar_top5_imagen(df_escolta[["Jugador", "Posición", perfil_escolta]], "Escolta (SG)", perfil_escolta, f"Top 5 Escolta (SG) - {perfil_escolta}")

if perfil_alero != "Selecciona un perfil":
    df_alero = df_filtrado[df_filtrado["Posición"] == "Alero (SF)"].sort_values(perfil_alero, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_alero}' en la posición Alero (SF):")
    mostrar_top5_imagen(df_alero[["Jugador", "Posición", perfil_alero]], "Alero (SF)", perfil_alero, f"Top 5 Alero (SF) - {perfil_alero}")

if perfil_ala_pivot != "Selecciona un perfil":
    df_ala_pivot = df_filtrado[df_filtrado["Posición"] == "Ala-Pívot (PF)"].sort_values(perfil_ala_pivot, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_ala_pivot}' en la posición Ala-Pívot (PF):")
    mostrar_top5_imagen(df_ala_pivot[["Jugador", "Posición", perfil_ala_pivot]], "Ala-Pívot (PF)", perfil_ala_pivot, f"Top 5 Ala-Pívot (PF) - {perfil_ala_pivot}")

if perfil_pivot != "Selecciona un perfil":
    df_pivot = df_filtrado[df_filtrado["Posición"] == "Pívot (C)"].sort_values(perfil_pivot, ascending=False).head(5)
    st.write(f"Los 5 mejores jugadores para el perfil '{perfil_pivot}' en la posición Pívot (C):")
    mostrar_top5_imagen(df_pivot[["Jugador", "Posición", perfil_pivot]], "Pívot (C)", perfil_pivot, f"Top 5 Pívot (C) - {perfil_pivot}")
