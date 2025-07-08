
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import instaloader

st.set_page_config(page_title="ERCO Social Listening Dashboard", layout="wide")
st.title("ERCO Social Listening Dashboard")

# Simulamos menciones y sentimiento
data = {
    "Fecha": ["2023-01", "2023-02", "2023-03", "2023-04"],
    "Menciones": [120, 150, 170, 130],
    "Sentimiento Positivo (%)": [70, 75, 80, 78]
}
df_sentimiento = pd.DataFrame(data)
st.subheader("Resumen de Menciones y Sentimiento")
st.dataframe(df_sentimiento)

# Tendencia
st.subheader("Tendencia de Menciones")
fig1, ax1 = plt.subplots()
ax1.plot(df_sentimiento["Fecha"], df_sentimiento["Menciones"], marker="o")
plt.ylabel("Menciones")
st.pyplot(fig1)

# Scraping Instagram (manual)
st.subheader("Seguidores en Instagram (actualización manual)")

if st.button("Actualizar Seguidores"):
    cuentas = ["ercoenergia", "celsia_energia", "enelcolombia", "empgrupoepm", "vatiaenergia"]
    L = instaloader.Instaloader()
    seguidores = []
    for cuenta in cuentas:
        try:
            perfil = instaloader.Profile.from_username(L.context, cuenta)
            seguidores.append(perfil.followers)
        except Exception as e:
            seguidores.append(None)
    df = pd.DataFrame({
        "Cuenta": cuentas,
        "Seguidores": seguidores
    })

    st.dataframe(df)

    # Limpiar valores nulos o no numéricos
    df_clean = df[pd.to_numeric(df["Seguidores"], errors='coerce').notnull()]
    df_clean["Seguidores"] = df_clean["Seguidores"].astype(int)

    # Verificamos si hay datos válidos
    if not df_clean.empty:
        fig, ax = plt.subplots()
        ax.bar(df_clean["Cuenta"], df_clean["Seguidores"], color='skyblue')
        plt.xticks(rotation=45)
        plt.ylabel("Seguidores")
        st.pyplot(fig)
    else:
        st.warning("No hay datos válidos para graficar seguidores.")

