import os
import pandas as pd
from pyproj import Proj, transform


def convert_estnort_by_latlon():
    '''
        Converte coordenadas no formato Este e Norte para Latitude e Longitude.
        Formato de arquivo suportado: CSV.

        Colunas do arquivo de entrada (devem ser em UPPERCASE): TORRE, ESTE, NORTE.
            TORRE   -     Identificador.
            ESTE    -     Valor (exemplo: 243530.181) referente a coordenada este.
            NORTE   -     Valor (exemplo: 7798308.853) referente a coordenada norte.
    '''

    # Solicitando o caminho do arquivo de entrada
    input_file = input(
        "Por favor, insira o caminho completo para o arquivo CSV de entrada: ")

    # Definindo o caminho do arquivo de saída
    base_name = os.path.basename(input_file)
    dir_name = os.path.dirname(input_file)
    output_file = os.path.join(
        dir_name, f"{os.path.splitext(base_name)[0]}_latlon.csv")

    # Definindo as projeções
    utm_proj = Proj(proj='utm', zone=24, south=True, ellps='GRS80', units='m')
    latlon_proj = Proj(proj='latlong', datum='WGS84')

    # Lendo os dados de entrada
    data = pd.read_csv(input_file)

    # Realizando a conversão
    latitudes = []
    longitudes = []
    for _, row in data.iterrows():
        lon, lat = transform(utm_proj, latlon_proj, row['ESTE'], row['NORTE'])
        latitudes.append(lat)
        longitudes.append(lon)

    # Adicionando as novas colunas ao DataFrame
    data['LATITUDE'] = latitudes
    data['LONGITUDE'] = longitudes

    # Salvando o DataFrame em um novo arquivo CSV
    data.to_csv(output_file, index=False)

    print(f"Arquivo salvo com sucesso em: {output_file}")


# Chamando a função
convert_estnort_by_latlon()
