import pandas as pd
import xml.etree.ElementTree as ET
import os

'''
    Gerador de Perfil de torre para adição no arquivo XML do SIGET
    (Envio obrigatório recorrente exigido pela ONS atras do 'Duto')
'''

# Solicitar ao usuário o caminho do arquivo CSV
caminho_csv = input("Por favor, insira o caminho do arquivo CSV: ")

# Carregar os dados do CSV
df = pd.read_csv(caminho_csv)

# Criar o elemento raiz
perfil = ET.Element('PERFIL')

# Iterar sobre cada linha do DataFrame
for _, row in df.iterrows():
    # Criar o elemento TORRE
    torre = ET.SubElement(perfil, 'TORRE')
    torre.set('NUMERO_TORRE', str(row['num_est']))

    # Criar os elementos de dados
    ET.SubElement(
        torre, 'LATITUDE').text = f"{row['latitude_h']}:{row['latitude_m']}:{row['latitude_s']}"
    ET.SubElement(
        torre, 'LONGITUDE').text = f"{row['longitude_h']}:{row['longitude_m']}:{row['longitude_s']}"
    ET.SubElement(torre, 'TIPOESTRUTURA').text = str(row['tipo_torre_num'])
    ET.SubElement(torre, 'LEVTOPO').text = str(row['levant_topog'])
    ET.SubElement(torre, 'FUNDACAO').text = str(row['fundacao'])
    ET.SubElement(torre, 'MONTAGEM').text = str(row['montagem'])
    ET.SubElement(torre, 'LANCAMENTO').text = str(row['lancamento'])

# Criar a árvore XML e salvar no arquivo
tree = ET.ElementTree(perfil)

# Obter o diretório do arquivo CSV
diretorio = os.path.dirname(caminho_csv)

# Salvar o arquivo XML no mesmo diretório do arquivo CSV
tree.write(os.path.join(diretorio, 'saida.xml'))
