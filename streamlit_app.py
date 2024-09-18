import streamlit as st
import pandas as pd


st.title("🤾🏻 Estadisticas de la planilla de Balonmano 🤾🏻‍♀️")

# URL del archivo en GitHub (reemplaza por tu URL)
url = "https://raw.githubusercontent.com/SongBuster/planillabalonmano/main/tabla.txt"


# Leer el archivo
@st.cache_data
def load_data(url):
    return pd.read_csv(url, sep='\t')

# Cargar los datos
data = load_data(url)

# Mostrar los primeros datos
st.subheader('Primeras filas del archivo')
st.write(data.head())

# Mostrar un resumen estadístico
st.subheader('Resumen estadístico del archivo')
st.write(data.describe())

# Generar un gráfico de barras de una columna
st.subheader('Gráfico de barras')
column_to_plot = st.selectbox('Selecciona una columna para el gráfico de barras', data.columns)

#fig, ax = plt.subplots()
#sns.barplot(x=data.index, y=data[column_to_plot], ax=ax)
#st.pyplot(fig)
