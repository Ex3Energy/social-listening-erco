
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("ERCO Social Listening Dashboard")

# Datos de ejemplo
data = {
    'Fecha': ['2023-01', '2023-02', '2023-03', '2023-04'],
    'Menciones': [120, 150, 170, 130],
    'Sentimiento Positivo (%)': [70, 75, 80, 78]
}

df = pd.DataFrame(data)

# Mostrar tabla
st.subheader("Resumen de Menciones y Sentimiento")
st.dataframe(df)

# Gráfica
st.subheader("Tendencia de Menciones")
fig, ax = plt.subplots()
ax.plot(df['Fecha'], df['Menciones'], marker='o')
ax.set_xlabel("Fecha")
ax.set_ylabel("Menciones")
st.pyplot(fig)
