import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🤾🏻 Estadisticas de la planilla de Balonmano 🤾🏻‍♀️")

# URL del archivo en GitHub (reemplaza por tu URL)
url = "https://raw.githubusercontent.com/SongBuster/planillabalonmano/main/tabla.txt"


# Leer el archivo
@st.cache_data
def load_data(url):
    return pd.read_csv(url, sep='\t')

# Cargar los datos
data = load_data(url)

# Mostrar la tabla completa
st.subheader('Datos completos del partido')
st.write(data)

# Resumen: Conteo de acciones por jugador
st.subheader('Conteo de acciones por jugador')
acciones_por_jugador = data['Jugador'].value_counts()
st.bar_chart(acciones_por_jugador)

# Resumen: Total de goles y fallos
st.subheader('Resumen de goles y fallos')
resultados = data['Resultado'].value_counts()
st.write(resultados)

# Gráfico de barras: Goles por jugador
st.subheader('Goles por jugador')
goles_por_jugador = data[data['Resultado'] == 'GOL']['Jugador'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=goles_por_jugador.index, y=goles_por_jugador.values, ax=ax)
ax.set_ylabel('Cantidad de Goles')
ax.set_xlabel('Jugador')
st.pyplot(fig)

# Gráfico de línea: Evolución del marcador (Nos vs. Ellos)
st.subheader('Evolución del marcador')
fig, ax = plt.subplots()
ax.plot(data['Tiempo'], data['Nos'], label="Nos")
ax.plot(data['Tiempo'], data['Ellos'], label="Ellos", color='red')
ax.set_ylabel('Marcador')
ax.set_xlabel('Tiempo')
ax.legend()
st.pyplot(fig)
