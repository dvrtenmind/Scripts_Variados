import os
import pandas as pd
import geopandas as gpd
from pyproj import CRS
import xlwings as xw

'''
    [CÓDIGO OBSOLETO, UTILIZAR APENAS PARA FINS DE ESTUDO]

    Gerador de arquivo shapefile (shp) padronizado conforme especificações
    da ONS para envio de dados geográfico ao sistema SGBDIT.
    
'''


@xw.func
def salvar_como_shp():
    # Obtenha o workbook e a planilha ativa
    wb = xw.Book.caller()
    sheet = wb.sheets.active

    # Converta a planilha do Excel em um DataFrame do pandas
    df = sheet.range('A1').options(pd.DataFrame, expand='table').value

    # Crie um GeoDataFrame a partir do DataFrame
    # Assegure-se de que 'x' e 'y' são os nomes corretos para suas colunas de coordenadas
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X, df.Y))

    # Defina o sistema de coordenadas para SIRGAS 2000
    gdf = gdf.set_crs('EPSG:4674')

    # Crie uma pasta 'shp' no mesmo diretório do arquivo Excel
    shp_folder = os.path.join(os.path.dirname(wb.fullname), 'shp')
    os.makedirs(shp_folder, exist_ok=True)

    # Salve o GeoDataFrame como um shapefile na pasta 'shp'
    shp_path = os.path.join(shp_folder, f'{sheet.name}.shp')
    gdf.to_file(shp_path)

    return f"Shapefile salvo em {shp_path}"
