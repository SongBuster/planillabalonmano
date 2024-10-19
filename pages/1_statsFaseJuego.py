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

    filtro1 =df[(df['A_D'] == 'A') & (df['Jugada'].str[:4] == 'LANZ') & (df['Resultado'] == 'GOL')]
    golesNosotros = len(filtro1)

    st.markdown("<b>Agustinos: " + str(golesNosotros) + "</b>", unsafe_allow_html=True)
    filtro2 = df[(df['A_D'] == 'D') & (df['Jugada'].str[:4] == 'LANZ') & (df['Resultado'] == 'GOL RIVAL')]
    st.markdown("<b>Atticgo Elche: " + str(len(filtro2)) + "</b>", unsafe_allow_html=True)

    st.write(df)

