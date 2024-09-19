import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import funciones as fnc

def pintar_pct_absoluto(pct, allvals):
    absolute = int(pct/100.*sum(allvals))
    return f"{pct:.1f}%\n({absolute})"




# URL del archivo en GitHub (reemplaza por tu URL)
url = "https://raw.githubusercontent.com/SongBuster/planillabalonmano/main/tabla.txt"


# Leer el archivo

def load_data(url):
    return pd.read_csv(url, sep='\t')

# Cargar los datos
df = fnc.load_data_from_github()
if df.empty:
    st.write("No se pudo encontrar el fichero de datos.")
else:
        
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

    etiq_atac = fnc.leer_fichero_etiq('AtaqueFaseJuego.etiqs')
    etiq_atac_posicional = fnc.filtrar_por_agrupacion(etiq_atac,"POSICIONAL")
    df_posicional = ataques[ataques['Fase'].isin(etiq_atac_posicional)]
    num_ataques_posicional = df_posicional.shape[0]
    goles_ataque_posicional = df_posicional[df_posicional["Resultado"] == "GOL"].shape[0]
    etiq_contras = fnc.filtrar_por_agrupacion(etiq_atac,"CONTRA")
    df_contras = ataques[ataques['Fase'].isin(etiq_contras)]
    num_contras = df_contras.shape[0]
    goles_contras = df_contras[df_contras["Resultado"] == "GOL"].shape[0]

    etiq_def = fnc.leer_fichero_etiq('DefensaFaseJuego.etiqs')
    etiq_def_posicional = fnc.filtrar_por_agrupacion(etiq_def,"POSICIONAL")
    df_def_posicional = defensas[defensas['Fase'].isin(etiq_def_posicional)]
    num_def_posicional = df_def_posicional.shape[0]
    goles_def_posicional = df_def_posicional[df_def_posicional["Resultado"] == "GOL RIVAL"].shape[0]
    etiq_balance = fnc.filtrar_por_agrupacion(etiq_def,"CONTRA")
    df_balance = defensas[defensas['Fase'].isin(etiq_balance)]
    num_balances = df_balance.shape[0]
    goles_balances = df_balance[df_balance["Resultado"] == "GOL RIVAL"].shape[0]

    st.cache_data(ttl=60)
    st.title("🤾🏻 Estadisticas de la planilla de Balonmano 🤾🏻‍♀️")
    ult_tiempo = df.tail(1).iloc[0]['Tiempo']

    col1, col2, col3= st.columns([1,1,1])
    with col1:
        st.write(ult_tiempo)
    with col2:    
        if st.button('Actualizar Datos'):
            st.cache_data.clear()            
    with col3:
        pass


    st.markdown("## Resumen Estadístico")
    html ="""
        <style>
            table {
                width: 90%;
                margin: 0 auto;
                border-collapse: collapse;
            }
            .dataframe td {
                text-align: left; /* Alineación por defecto a la izquierda */
                width: 40%;
            }
            .dataframe .derecha {
                text-align: right; /* Alineación específica a la derecha */
                width: 10%;
            }        
            .dataframe .bold {
                font-weight: bold;
            }
            .dataframe .header {
                font-weight: bold;
                text-align: center;
            }

        </style>
        <html>
            <table border="1" class="dataframe">
            <tr>
                <td colspan="2" width="50%" class="header">ATAQUES</td>
                <td colspan="2" class="header">DEFENSAS</td>
            </tr>
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
            <table class="dataframe">
            <tr>
                <td>Número de ataques posicionales:</td>
                <td class="derecha">{num_ataques_posicional}</td>
                <td>Número de defensas posicionales:</td>
                <td class="derecha">{num_def_posicional}</td>
            </tr>
            <tr>
                <td>% ataques posicionales:</td>
                <td class="derecha">{pct_ataques_pos}</td>
                <td>% defensas posicionales:</td>
                <td class="derecha">{pct_def_pos}</td>
            </tr>
            <tr>
                <td>Goles en ataques posicionales:</td>
                <td class="derecha">{goles_ataque_posicional}</td>
                <td>Gol rival en defensas posicionales:</td>
                <td class="derecha">{goles_def_posicional}</td>
            </tr>
            <tr>
                <td>% gol en ataques posicionales:</td>
                <td class="derecha">{pct_ataques_pos_gol}</td>
                <td>% gol rival en defensas posicionales:</td>
                <td class="derecha">{pct_def_pos_gol}</td>
            </tr>
            </table>
            <table class="dataframe">
            <tr>
                <td>Número de contraataques/cg:</td>
                <td class="derecha">{num_contras}</td>
                <td>Número de balances ct/cg:</td>
                <td class="derecha">{num_balances}</td>
            </tr>
            <tr>
                <td>% contraataques/cg:</td>
                <td class="derecha">{pct_contras}</td>
                <td>% balances ct/cg:</td>
                <td class="derecha">{pct_balances}</td>
            </tr>
            <tr>
                <td>Goles en contraataques/cg:</td>
                <td class="derecha">{goles_contras}</td>
                <td>Gol rival balances ct/cg:</td>
                <td class="derecha">{goles_balances}</td>
            </tr>
            <tr>
                <td>% gol en contraataques/cg:</td>
                <td class="derecha">{pct_contras_gol}</td>
                <td>% gol rival balances ct/cg:</td>
                <td class="derecha">{pct_balances_gol}</td>
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
    html = html.replace("{num_ataques_posicional}",f"{num_ataques_posicional}");
    html = html.replace("{pct_ataques_pos}",f"{num_ataques_posicional/num_ataques*100 if num_ataques > 0 else 0:.2f}%");
    html = html.replace("{goles_ataque_posicional}",f"{goles_ataque_posicional}");
    html = html.replace("{pct_ataques_pos_gol}",f"{goles_ataque_posicional/num_ataques_posicional*100 if num_ataques_posicional > 0 else 0:.2f}%");
    html = html.replace("{num_def_posicional}",f"{num_def_posicional}");
    html = html.replace("{pct_def_pos}",f"{num_def_posicional/num_defensas*100 if num_defensas > 0 else 0:.2f}%");
    html = html.replace("{goles_def_posicional}",f"{goles_def_posicional}");
    html = html.replace("{pct_def_pos_gol}",f"{goles_def_posicional/num_def_posicional*100 if num_def_posicional > 0 else 0:.2f}%");
    html = html.replace("{num_contras}",f"{num_contras}");
    html = html.replace("{pct_contras}",f"{num_contras/num_ataques*100 if num_ataques > 0 else 0:.2f}%");
    html = html.replace("{goles_contras}",f"{goles_contras}");
    html = html.replace("{pct_contras_gol}",f"{goles_contras/num_contras*100 if num_contras > 0 else 0:.2f}%");
    html = html.replace("{num_balances}",f"{num_balances}");
    html = html.replace("{pct_balances}",f"{num_balances/num_defensas*100 if num_defensas > 0 else 0:.2f}%");
    html = html.replace("{goles_balances}",f"{goles_balances}");
    html = html.replace("{pct_balances_gol}",f"{goles_balances/num_balances*100 if num_balances > 0 else 0:.2f}%");

    st.markdown(html, unsafe_allow_html=True)

    # Grafico de tarta: Ataques totales (posesiones)

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
