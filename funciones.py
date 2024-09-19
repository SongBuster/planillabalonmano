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