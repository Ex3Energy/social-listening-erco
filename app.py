
import streamlit as st
import instaloader
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

# Cargar variables de entorno (credenciales)
load_dotenv()
USERNAME = os.getenv("INSTA_USER")
PASSWORD = os.getenv("INSTA_PASS")

# -------------------------------
# Configuración general del app
# -------------------------------
st.set_page_config(page_title="ERCO Social Listening", layout="wide")
st.title("ERCO Social Listening Dashboard")

# -------------------------------
# Módulo 1: Datos simulados históricos
# -------------------------------
st.subheader("Resumen de Menciones y Sentimiento")

# Datos de ejemplo (simulados)
data = {
    "Fecha": ["2023-01", "2023-02", "2023-03", "2023-04"],
    "Menciones": [120, 150, 170, 130],
    "Sentimiento Positivo (%)": [70, 75, 80, 78]
}
df = pd.DataFrame(data)
st.dataframe(df)

# Gráfica de tendencia de menciones
st.subheader("Tendencia de Menciones")
fig1, ax1 = plt.subplots()
ax1.plot(df["Fecha"], df["Menciones"], marker="o", linestyle="-")
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Menciones")
st.pyplot(fig1)

# -------------------------------
# Módulo 2: Seguidores de Instagram con login
# -------------------------------
st.subheader("Seguidores en Instagram (actualización manual)")

# Cuentas a monitorear
cuentas_instagram = ["ercoenergia", "celsia_energia", "enelcolombia", "empgrupoepm", "vatiaenergia"]

@st.cache_data(show_spinner="Conectando a Instagram...", ttl=3600)
def obtener_seguidores(cuentas):
    L = instaloader.Instaloader()
    try:
        L.login(USERNAME, PASSWORD)
    except Exception as e:
        st.error(f"Error al iniciar sesión en Instagram: {e}")
        return pd.DataFrame()

    seguidores = []
    for cuenta in cuentas:
        try:
            perfil = instaloader.Profile.from_username(L.context, cuenta)
            seguidores.append({"Cuenta": cuenta, "Seguidores": perfil.followers})
        except Exception as e:
            seguidores.append({"Cuenta": cuenta, "Seguidores": None})
            st.warning(f"No se pudo acceder a @{cuenta}: {e}")

    return pd.DataFrame(seguidores)

# Botón manual para actualizar
if st.button("Actualizar Seguidores"):
    df_seguidores = obtener_seguidores(cuentas_instagram)
    st.dataframe(df_seguidores)

    if not df_seguidores["Seguidores"].isnull().all():
        fig2, ax2 = plt.subplots()
        ax2.bar(df_seguidores["Cuenta"], df_seguidores["Seguidores"], color="mediumseagreen")
        ax2.set_ylabel("Seguidores")
        ax2.set_title("Comparativo de Seguidores en Instagram")
        st.pyplot(fig2)
    else:
        st.warning("No hay datos válidos para graficar seguidores.")

