import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.title("🤾🏻 Estadisticas de la planilla de Balonmano 🤾🏻‍♀️")

# URL del archivo en GitHub (reemplaza por tu URL)
url = "https://raw.githubusercontent.com/SongBuster/planillabalonmano/main/tabla.txt"


# Leer el archivo
@st.cache_data
def load_data(url):
    return pd.read_csv(url, sep='\t')

# Cargar los datos
df = load_data(url)
# Filtrar ataques y defensas
ataques = df[df['A/D'] == 'A']
defensas = df[df['A/D'] == 'D']
# Contar goles y no goles
num_ataques = ataques.shape[0]
goles_ataque = ataques[ataques["Resultado"] == "GOL"].shape[0]
no_goles_ataque = ataques[ataques["Resultado"] != "GOL"].shape[0]
pct_goles_ataque = (goles_ataque / num_ataques) * 100 if num_ataques > 0 else 0
num_defensas = defensas.shape[0]
goles_defensa = defensas[defensas["Resultado"] == "GOL RIVAL"].shape[0]
no_goles_defensa = defensas[defensas["Resultado"] != "GOL RIVAL"].shape[0]
pct_goles_defensa = (goles_defensa / num_defensas) * 100 if num_defensas > 0 else 0


st.markdown("## Resumen Estadístico")
html ="""
    <style>
        table {
            width: 100%;
            margin: 0 auto;
            border-collapse: collapse;
        }
        .dataframe td {
            text-align: left; /* Alineación por defecto a la izquierda */
        }
        .dataframe .derecha {
            text-align: right; /* Alineación específica a la derecha */
        }        
        .dataframe .bold {
            font-weight: bold;
        }

    </style>
    <html>
        <table border="1" class="dataframe">
        <tr>
            <td>Número de ataques:</td>
            <td class="derecha">{num_ataques}</td>
            <td>Número de defensas:</td>
            <td class="derecha">{num_defensas}</td>
        </tr>
        <tr>
            <td>Número de ataques en gol:</td>
            <td class="derecha">{num_ataques_gol}</td>
            <td>Número de defensas con gol rival:</td>
            <td class="derecha">{num_defensas_gol}</td>
        </tr>
        <tr class="bold">
            <td>% de ataques en gol:</td>
            <td class="derecha">{pct_ataques_gol}</td>
            <td>% de defensas con gol rival:</td>
            <td class="derecha">{pct_defensas_gol}</td>
        </tr>
        </table>
        <table>
        <tr>
            <td>Número de ataques posicionales:</td>
            <td class="derecha">{num_ataques}</td>
            <td>Número de defensas posicionales:</td>
            <td class="derecha">{num_defensas}</td>
        </tr>
        <tr>
            <td>Número de ataques en gol:</td>
            <td class="derecha">{num_ataques_gol}</td>
            <td>Número de defensas con gol rival:</td>
            <td class="derecha">{num_defensas_gol}</td>
        </tr>
        <tr class="bold">
            <td>% de ataques en gol:</td>
            <td class="derecha">{pct_ataques_gol}</td>
            <td>% de defensas con gol rival:</td>
            <td class="derecha">{pct_defensas_gol}</td>
        </tr>
        </table>
    </html>
"""

html = html.replace("{num_ataques}",f"{num_ataques}");
html = html.replace("{num_defensas}",f"{num_defensas}");
html = html.replace("{num_ataques_gol}",f"{goles_ataque}");
html = html.replace("{num_defensas_gol}",f"{goles_defensa}");
html = html.replace("{pct_ataques_gol}",f"{pct_goles_ataque:.2f}%");
html = html.replace("{pct_defensas_gol}",f"{pct_goles_defensa:.2f}%");

st.markdown(html, unsafe_allow_html=True)

# Grafico de tarta: Ataques totales (posesiones)
def pintar_pct_absoluto(pct, allvals):
    absolute = int(pct/100.*sum(allvals))
    return f"{pct:.1f}%\n({absolute})"

fig, ax = plt.subplots(1,2,figsize=(8,4))

# Datos para el gráfico de tarta de ataques
labels_ataque = ['Ataques en NO GOL', 'Ataques en GOL']
sizes_ataque = [no_goles_ataque, goles_ataque]
colors_ataque = plt.get_cmap('Oranges')(np.linspace(0.2, 0.7, len(sizes_ataque)))
ax[0].pie(sizes_ataque, colors=colors_ataque, autopct=lambda pct: pintar_pct_absoluto(pct , sizes_ataque), startangle=90)
ax[0].set_title('Ataques Totales (Posesiones)')
ax[0].axis('equal')
# Datos para el gráfico de tarta de defensas
labels_defensa = ['Defensas con GOL RIVAL', 'Defensas con NO GOL RIVAL']
sizes_defensa = [goles_defensa, no_goles_defensa]
colors_defensa = plt.get_cmap('Greens')(np.linspace(0.2, 0.7, len(sizes_defensa)))
ax[1].pie(sizes_defensa,  colors=colors_defensa, autopct=lambda pct: pintar_pct_absoluto(pct , sizes_defensa), startangle=90)
ax[1].set_title('Defensas Totales (Posesiones)')
ax[1].axis('equal')
# Agregar leyendas
fig.legend(labels_ataque, loc='lower left', bbox_to_anchor=(0.1, 0.1), title="Ataques")
fig.legend(labels_defensa, loc='lower right', bbox_to_anchor=(0.9, 0.1), title="Defensas")


st.pyplot(plt)
