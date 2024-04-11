import os
import pandas as pd
from pyproj import Proj

def convert_utm_to_latlon(easting, northing, zone_number, zone_letter):
    utm_proj = Proj(proj='utm', zone=zone_number,
                    ellps='GRS80', south=(zone_letter >= 'N'))
    lon, lat = utm_proj(easting, northing, inverse=True)
    return lat, lon


def convert_to_dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return f"{d}°{m}'{sd}\""


def convert_coordinates(df):
    for index, row in df.iterrows():
        lat, lon = convert_utm_to_latlon(row['X'], row['Y'], 24, 'S')
        df.at[index, 'Latitude'] = lat
        df.at[index, 'Longitude'] = lon
        df.at[index, 'Latitude_DMS'] = convert_to_dms(lat)
        df.at[index, 'Longitude_DMS'] = convert_to_dms(lon)
    return df


# Solicitando o caminho do arquivo de entrada
input_file = input(
    "Por favor, insira o caminho completo para o arquivo CSV de entrada: ")

# Definindo o caminho do arquivo de saída
base_name = os.path.basename(input_file)
dir_name = os.path.dirname(input_file)
output_file = os.path.join(
    dir_name, f"{os.path.splitext(base_name)[0]}_dms.csv")

# Carregar o CSV
df = pd.read_csv(input_file)

# Converter as coordenadas
df = convert_coordinates(df)

# Salvar o DataFrame convertido de volta para um CSV
df.to_csv(output_file, index=False)

print(f"Arquivo salvo com sucesso em: {output_file}")
