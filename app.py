
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import instaloader

# Lista de cuentas a monitorear
INSTAGRAM_USERS = [
    "ercoenergia",
    "epmestamosahi",
    "celsia_energia",
    "vatiaenergia",
    "enelxcolombia",
    "grupobia_col"
]

# Función de scraping
def scrape_instagram_profiles():
    loader = instaloader.Instaloader()
    data = []

    for username in INSTAGRAM_USERS:
        try:
            profile = instaloader.Profile.from_username(loader.context, username)
            data.append({
                "Cuenta": username,
                "Seguidores": profile.followers,
                "Fecha": datetime.today().strftime('%Y-%m-%d')
            })
        except Exception as e:
            data.append({
                "Cuenta": username,
                "Seguidores": None,
                "Fecha": datetime.today().strftime('%Y-%m-%d'),
                "Error": str(e)
            })

    df = pd.DataFrame(data)
    df.to_csv("instagram_data.csv", index=False)
    return df

# Dashboard
st.set_page_config(page_title="ERCO Social Listening", layout="wide")
st.title("📱 Seguidores en Instagram - ERCO y Competidores")

# Botón de actualización
if st.button("Actualizar seguidores desde Instagram"):
    df = scrape_instagram_profiles()
    st.success("✅ Seguidores actualizados correctamente.")
else:
    try:
        df = pd.read_csv("instagram_data.csv")
    except:
        st.warning("⚠️ Aún no se han cargado datos. Presiona el botón para iniciar.")
        df = pd.DataFrame(columns=["Cuenta", "Seguidores", "Fecha"])

# Mostrar tabla
if not df.empty:
    st.subheader("📊 Tabla de Seguidores")
    st.dataframe(df)

    st.subheader("📉 Comparación de Seguidores")
    fig, ax = plt.subplots()
    ax.bar(df["Cuenta"], df["Seguidores"], color='skyblue')
    plt.xticks(rotation=45)
    plt.ylabel("Seguidores")
    st.pyplot(fig)

