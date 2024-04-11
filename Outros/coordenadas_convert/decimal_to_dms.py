import pandas as pd


def decimal_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = (decimal_degrees - degrees - minutes/60) * 3600
    return degrees, minutes, seconds


def convert_csv(file_name):
    df = pd.read_csv(file_name)
    for col in ['Latitude', 'Longitude']:
        df[col + '_graus'], df[col + '_minutos'], df[col +
                                                     '_segundos'] = zip(*df[col].map(decimal_to_dms))
        df[col + '_dms'] = df[col + '_graus'].astype(str) + ":" + df[col + '_minutos'].astype(
            str) + ":" + df[col + '_segundos'].astype(str)
    df.to_csv(file_name[:-4] + "_dms.csv", index=False)


file_name = input("Digite o nome do arquivo CSV: ")
convert_csv(file_name)
