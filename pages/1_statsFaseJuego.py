import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import funciones as fnc
from io import BytesIO

def pintar_pct_absoluto(pct, allvals):
    absolute = int(pct/100.*sum(allvals))
    return f"{pct:.1f}%\n({absolute})"


#st.set_page_config(layout="wide")

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
    #st.title("🤾🏻 Estadisticas de la planilla de Balonmano 🤾🏻‍♀️")
    ult_tiempo = df.tail(1).iloc[0]['Tiempo']

    col1, col2, col3= st.columns([0.15,0.1,0.75])
    with col2:
        st.write(ult_tiempo)
    with col1:    
        if st.button('Actualizar Datos'):
            st.cache_data.clear()            
    with col3:
        pass

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
                <td colspan="2" width="50%" class="header">ATAQUES TOTALES</td>
                <td colspan="2" class="header">DEFENSAS TOTALES</td>
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
                <td colspan="2" width="50%" class="header">ATAQUES POSICIONALES</td>
                <td colspan="2" class="header">DEFENSAS POSICIONALES</td>
            </tr>
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
                <td colspan="2" width="50%" class="header">CONTRAATAQUES / CONTRAGOL</td>
                <td colspan="2" class="header">BALANCES DEFENSIVOS</td>
            </tr>
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

    buf = BytesIO()
    fig.savefig(buf,format="png")
    left_co, center_co, last_co = st.columns([0.1,0.8,0.1])
    with center_co:
        st.image(buf)   


    # grafico combinado ataques (barras y lineas)
    resumen_ataques = ataques.groupby('Fase').agg(
        Ataques=('Tiempo','count'), #numero de ataques por fase
        Goles=('Resultado', lambda x: (x == 'GOL').sum()), # numero de goles por fase        
    ).reset_index()
    resumen_ataques['% Exito'] = (resumen_ataques['Goles']  / resumen_ataques['Ataques']) * 100

    todas_fases_ataque = pd.DataFrame([item['etiqueta'] for item in etiq_atac.values() if item['etiqueta'] != ""])
    todas_fases_ataque.columns = ['Fase']    

    cruce_fases_ataque= pd.merge(todas_fases_ataque, resumen_ataques, on ='Fase', how='left')
    cruce_fases_ataque.fillna(0,inplace=True)
    print(cruce_fases_ataque)
    cruce_fases_ataque = cruce_fases_ataque.sort_values(by='Ataques', ascending=False)
    
    # Crear el gráfico combinado
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Gráfico de barras para los ataques
    bars = ax1.bar(cruce_fases_ataque['Fase'], cruce_fases_ataque['Ataques'], color='lightblue', label='Ataques', alpha=0.7)
    ax1.set_xlabel('Fase')
    ax1.set_ylabel('Número de Ataques', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    for bar in bars:
        yval = bar.get_height()
        if (yval != 0):
            ax1.text(bar.get_x() + bar.get_width()/2, yval - 0.1, f'{yval:.0f}', ha='center', va='center', color='blue')

    # Rotar etiquetas del eje X 45 grados
    plt.xticks(rotation=45, ha='right')

    # Crear un segundo eje para la línea del porcentaje de goles
    ax2 = ax1.twinx()
    ax2.plot(cruce_fases_ataque['Fase'], cruce_fases_ataque['% Exito'], color='green', marker='o', label='% Exito', linestyle='-', linewidth=2)
    ax2.set_ylabel('% Éxito', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.set_ylim(0, 100)


    # Añadir los valores sobre los puntos de la serie de líneas
    for i, (fase, pct, val) in enumerate(zip(cruce_fases_ataque['Fase'], cruce_fases_ataque['% Exito'] , cruce_fases_ataque['Ataques'])):
        if (pct != 0):
            ax2.annotate(f'{pct:.1f}%', (i, pct), textcoords="offset points", xytext=(0, 10), ha='center', color='green')
    


    # Título y leyendas
    plt.title('Número de Ataques y % de Éxito por Fase')
    fig.tight_layout()

    # Mostrar el gráfico
    buf = BytesIO()
    fig.savefig(buf,format="png")
    left_co, center_co, last_co = st.columns([0.1,0.8,0.1])
    with center_co:
        st.image(buf)  
    
    # grafico combinado defensas (barras y lineas)
    resumen_defensas = defensas.groupby('Fase').agg(
        Defensas=('Tiempo','count'), #numero de defensas por fase
        Goles=('Resultado', lambda x: (x == 'GOL RIVAL').sum()), # numero de goles por fase        
    ).reset_index()
    resumen_defensas['% Exito'] = ((resumen_defensas['Defensas'] - resumen_defensas['Goles'])  / resumen_defensas['Defensas']) * 100

    todas_fases_def = pd.DataFrame([item['etiqueta'] for item in etiq_def.values() if item['etiqueta'] != ""])
    todas_fases_def.columns = ['Fase']    

    cruce_fases_def= pd.merge(todas_fases_def, resumen_defensas, on ='Fase', how='left')
    cruce_fases_def.fillna(0,inplace=True)    
    cruce_fases_def = cruce_fases_def.sort_values(by='Defensas', ascending=False)
    
    # Crear el gráfico combinado
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Gráfico de barras para los ataques
    bars = ax1.bar(cruce_fases_ataque['Fase'], cruce_fases_def['Defensas'], color='lightblue', label='Defensas', alpha=0.7)
    ax1.set_xlabel('Fase')
    ax1.set_ylabel('Número de Ataques', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    for bar in bars:
        yval = bar.get_height()
        if (yval != 0):
            ax1.text(bar.get_x() + bar.get_width()/2, yval - 0.1, f'{yval:.0f}', ha='center', va='center', color='blue')

    # Rotar etiquetas del eje X 45 grados
    plt.xticks(rotation=45, ha='right')

    # Crear un segundo eje para la línea del porcentaje de goles
    ax2 = ax1.twinx()
    ax2.plot(cruce_fases_ataque['Fase'], cruce_fases_ataque['% Exito'], color='green', marker='o', label='% Exito', linestyle='-', linewidth=2)
    ax2.set_ylabel('% Éxito', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.set_ylim(0, 100)


    # Añadir los valores sobre los puntos de la serie de líneas
    for i, (fase, pct, val) in enumerate(zip(cruce_fases_ataque['Fase'], cruce_fases_ataque['% Exito'] , cruce_fases_ataque['Ataques'])):
        if (pct != 0):
            ax2.annotate(f'{pct:.1f}%', (i, pct), textcoords="offset points", xytext=(0, 10), ha='center', color='green')
    


    # Título y leyendas
    plt.title('Número de Ataques y % de Éxito por Fase')
    fig.tight_layout()

    # Mostrar el gráfico
    buf = BytesIO()
    fig.savefig(buf,format="png")
    left_co, center_co, last_co = st.columns([0.1,0.8,0.1])
    with center_co:
        st.image(buf)  
