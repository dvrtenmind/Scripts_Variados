import csv
import os


def decimal_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = (decimal_degrees - degrees - minutes/60) * 3600
    return f"{degrees}:{minutes}:{seconds}"


def convert_csv(file_name):
    # Abrir o arquivo CSV e criar um leitor de CSV
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Adicionar as colunas Latitude_dms e Longitude_dms
    for row in rows:
        for col in ['Latitude', 'Longitude']:
            row[col + '_dms'] = decimal_to_dms(float(row[col]))

    # Escrever os dados de volta para um novo arquivo CSV
    with open(os.path.join(os.path.dirname(file_name), 'saida.csv'), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


file_name = input("Digite o nome do arquivo CSV: ")
convert_csv(file_name)
