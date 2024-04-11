import csv
import os
from pyproj import Proj


def utm_to_latlon(utm_x, utm_y, zone_number, hemisphere):
    utm_proj = Proj(proj="utm", zone=zone_number,
                    ellps="WGS84", south=(hemisphere == "S"))
    lon, lat = utm_proj(utm_x, utm_y, inverse=True)
    return lat, lon


def decimal_degrees_to_dms(degrees):
    d = int(degrees)
    m = int((degrees - d) * 60)
    s = ((degrees - d) * 60 - m) * 60
    return d, m, s


def convert_csv(input_csv, output_csv):
    with open(input_csv, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames + ['Latitude', 'Longitude']

        with open(output_csv, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                utm_x = float(row['utm_x'])
                utm_y = float(row['utm_y'])
                zone_number = int(row['zone'])
                hemisphere = row['hemisphere']

                lat, lon = utm_to_latlon(utm_x, utm_y, zone_number, hemisphere)
                lat_dms = ':'.join(map(str, decimal_degrees_to_dms(lat)))
                lon_dms = ':'.join(map(str, decimal_degrees_to_dms(lon)))

                row['Latitude'] = lat_dms
                row['Longitude'] =lon_dms

                writer.writerow(row)


input_csv_file = input("Digite o caminho para o CSV a ser convertido")
folder = os.path.dirname(input_csv_file)
filename = os.path.basename(input_csv_file)
output_csv_file = os.path.join(folder, f"{filename}_output.csv")
convert_csv(input_csv_file, output_csv_file)
