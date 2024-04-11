import pandas as pd
from pyproj import Proj, transform
import os

def convert_coordinates():
    input_file = input("Digite o caminho para o arquivo a ser convertido: ")
    operation = input("Digite o tipo de conversão ('utm_to_latlon' ou 'latlon_to_utm'): ")

    df = pd.read_csv(input_file)

    if operation == 'utm_to_latlon':
        in_proj = Proj(init='epsg:31982')  # Isso é para UTM zona 22S no SIRGAS 2000. Modifique conforme necessário.
        out_proj = Proj(init='epsg:4674')  # Isso é para SIRGAS 2000.
        df['Latitude'], df['Longitude'] = transform(in_proj, out_proj, df['X UTM'].tolist(), df['Y UTM'].tolist())
        output_file = os.path.splitext(input_file)[0] + "_convertido_latlon.csv"
    elif operation == 'latlon_to_utm':
        in_proj = Proj(init='epsg:4674')  # Isso é para SIRGAS 2000.
        out_proj = Proj(init='epsg:31982')  # Isso é para UTM zona 22S no SIRGAS 2000. Modifique conforme necessário.
        df['X UTM'], df['Y UTM'] = transform(in_proj, out_proj, df['Latitude'].tolist(), df['Longitude'].tolist())
        output_file = os.path.splitext(input_file)[0] + "_convertido_utm.csv"
    else:
        print("Operação inválida. Use 'utm_to_latlon' ou 'latlon_to_utm'.")
        return

    df.to_csv(output_file, index=False)
    print(f"Arquivo salvo como {output_file}")

# Exemplo de uso
convert_coordinates()
