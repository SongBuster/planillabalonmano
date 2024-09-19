import requests
import pandas as pd
import base64
import io

GITHUB_TOKEN = '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'
RUTA_FICHERO_GITHUB = 'https://raw.githubusercontent.com/SongBuster/planillabalonmano/main/tabla.txt'


def leer_fichero_etiq(fichero):
    data = {}

    with open(fichero, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        #proceso cada linea
        for line in lines:
            key,value = line.strip().split('==')
            #limpio llaves y espacios
            value = value.strip('{}')
            #divido el valor en partes
            parts = value.split(',')
            # creo un diccionario con los valores
            data[key] = {
                'etiqueta': parts[0],        
                'defecto': parts[1] == 'true',
                'destacado': parts[2] =='true',
                'agrupacion':parts[3]
            }

    return data

def filtrar_por_agrupacion(data, agrupacion_deseada):
    # Filtrar el diccionario por la agrupación deseada
    return [item['etiqueta'] for item in data.values() if item['agrupacion'] == agrupacion_deseada]

def load_data_from_github():
    url = "https://api.github.com/repos/SongBuster/planillabalonmano/contents/tabla.txt?ref=main"
    #headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url)
    print(response.status_code)    
    if response.status_code == 200:
        print(response)
        file_content = response.json()['content']
        decoded_content = base64.b64decode(file_content).decode('utf-8')
        # Convertir el contenido en DataFrame
        data = pd.read_csv(io.StringIO(decoded_content), sep='\t')
        return data
    else:        
        return None