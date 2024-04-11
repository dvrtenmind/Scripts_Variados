import csv
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
        fieldnames = reader.fieldnames + ['Latitude Degrees', 'Latitude Minutes',
                                          'Latitude Seconds', 'Longitude Degrees', 'Longitude Minutes', 'Longitude Seconds']

        with open(output_csv, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                utm_x = float(row['utm_x'])
                utm_y = float(row['utm_y'])
                zone_number = int(row['zone'])
                hemisphere = row['hemisphere']

                lat, lon = utm_to_latlon(utm_x, utm_y, zone_number, hemisphere)
                lat_d, lat_m, lat_s = decimal_degrees_to_dms(lat)
                lon_d, lon_m, lon_s = decimal_degrees_to_dms(lon)

                row['Latitude Degrees'] = lat_d
                row['Latitude Minutes'] = lat_m
                row['Latitude Seconds'] = lat_s
                row['Longitude Degrees'] = lon_d
                row['Longitude Minutes'] = lon_m
                row['Longitude Seconds'] = lon_s

                writer.writerow(row)


input_csv_file = "C:\\Users\\User\\Downloads\\input_coordinates2.csv"
output_csv_file = 'output_coordinates22.csv'
convert_csv(input_csv_file, output_csv_file)
