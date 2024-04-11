import requests
import json

'''
    Obtem estabelecimentos de informática num raio especifico de Kms
    sobre uma localizaçãoo pré-definida, por meio da API do Google Maps
'''


def obter_estabelecimentos_informatica(localizacao, raio_km):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": localizacao,
        "radius": raio_km * 1000,
        "type": "electronics_store",
        "keyword": "informatica",
        "key": ""
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        estabelecimentos = data["results"]
        for estabelecimento in estabelecimentos:
            place_id = estabelecimento["place_id"]
            detalhes = obter_detalhes_estabelecimento(place_id)
            if detalhes:
                for chave, valor in detalhes.items():
                    print(f"{chave}:\n {valor}")
                    print("-------------------------")
            else:
                print("Não foi possível obter os detalhes do estabelecimento.")
            print("#########################################################")
    else:
        print("Erro ao obter os estabelecimentos.")


def obter_detalhes_estabelecimento(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": ""
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        detalhes = data["result"]
        return detalhes
    else:
        return None


# Exemplo de uso
# localizacao = "-22.8558, -47.2178" # Centro Hortolândia
localizacao = "-22.9071, -47.0632"  # Centro Campinas
raio_km = 10  # Exemplo de raio de 10 km

obter_estabelecimentos_informatica(localizacao, raio_km)
