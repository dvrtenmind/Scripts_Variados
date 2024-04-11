import pandas as pd
import pyproj
from pyproj import Proj, Transformer
import math


def decimal_to_dms(deg):
    # Função para converter graus decimais para DMS (graus, minutos, segundos)
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


def dms_to_decimal(d, m, s):
    # Função para converter DMS para graus decimais
    dd = d + float(m)/60 + float(s)/(60*60)
    return dd


def utm_to_decimal(x, y, zone):
    # Função para converter UTM para graus decimais
    utm_proj = Proj(proj='utm', zone=zone, ellps='GRS80')
    lon, lat = utm_proj(x, y, inverse=True)
    return lat, lon


def decimal_to_utm(lat, lon, zone):
    # Função para converter graus decimais para UTM
    utm_proj = Proj(proj='utm', zone=zone, ellps='GRS80')
    x, y = utm_proj(lon, lat)
    return x, y


def convert_coordinates(input_file, output_file, input_format, output_format):
    # Função para ler o arquivo CSV e realizar as conversões
    df = pd.read_csv(input_file)
    for index, row in df.iterrows():
        if input_format == 'latlon' and output_format == 'dms':
            df.at[index, 'Latitude_DMS'] = decimal_to_dms(row['Latitude'])
            df.at[index, 'Longitude_DMS'] = decimal_to_dms(row['Longitude'])
        elif input_format == 'latlon' and output_format == 'utm':
            df.at[index, 'X'], df.at[index, 'Y'] = decimal_to_utm(
                row['Latitude'], row['Longitude'], 23)
        elif input_format == 'dms' and output_format == 'latlon':
            df.at[index, 'Latitude'] = dms_to_decimal(
                row['Latitude_Deg'], row['Latitude_Min'], row['Latitude_Sec'])
            df.at[index, 'Longitude'] = dms_to_decimal(
                row['Longitude_Deg'], row['Longitude_Min'], row['Longitude_Sec'])
        elif input_format == 'dms' and output_format == 'utm':
            lat = dms_to_decimal(row['Latitude_Deg'],
                                 row['Latitude_Min'], row['Latitude_Sec'])
            lon = dms_to_decimal(row['Longitude_Deg'],
                                 row['Longitude_Min'], row['Longitude_Sec'])
            df.at[index, 'X'], df.at[index, 'Y'] = decimal_to_utm(lat, lon, 23)
        elif input_format == 'utm' and output_format == 'latlon':
            df.at[index, 'Latitude'], df.at[index,
                                            'Longitude'] = utm_to_decimal(row['X'], row['Y'], 23)
        elif input_format == 'utm' and output_format == 'dms':
            lat, lon = utm_to_decimal(row['X'], row['Y'], 23)
            df.at[index, 'Latitude_DMS'] = decimal_to_dms(lat)
            df.at[index, 'Longitude_DMS'] = decimal_to_dms(lon)
    df.to_csv(output_file, index=False)


# Solicitar ao usuário o formato de entrada e saída
input_format = input(
    "Por favor, insira o formato de entrada (latlon, dms, utm): ")
output_format = input(
    "Por favor, insira o formato de saída (latlon, dms, utm): ")
input_file = input("Insira o caminho para o arquivo a ser convertido:\n")
output_file = (input_file[:-4] + "_convertido.csv")
# Chamar a função de conversão
convert_coordinates(input_file,
                    output_file, input_format, output_format)
