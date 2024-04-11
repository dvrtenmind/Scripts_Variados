from zipfile import ZipFile
import pathlib
import shutil
import os

'''
    Script de extração de dados zipados em massa.
'''

# FUNÇÕES ----------------------------------


def verNomes(lista):
    print("[[[NOMES DOS ARQUIVOS]]]")
    for zips in lista:
        print("zip nome:")
        print(zips)
    print("///////////////////")


def gerarCaminho(obj):
    path, item = os.path.split(obj)
    gdb_name, extension = os.path.splitext(item)
    caminho = os.path.join(path, "extraidas", gdb_name)
    return caminho


def extrair(zipp, destino):
    print("################################################################################")
    print("[[EXTRAÇÃO INICIADA]]")
    filename = zipp
    # print("Arquivo: " +str(zipp))
    try:
        with ZipFile(filename, 'r') as zip:
            zip.printdir()
            zip.extractall(path=destino)
            print("Extraido com sucesso")
        return "OK"
    except:
        print("Erro ao extrair")
        return "ERRO"

# EXECUÇÃO ----------------------------------


origem = input("Insira o caminho para as fotos zipadas:\n")
# format_ = input("Qual o formato dos arquivos que devem ser extraidos?")
lista = list(pathlib.Path(origem).glob("**/*.zip"))
# print(lista)

# verNomes(lista)
resultado = dict()
for zipp in lista:
    caminho = gerarCaminho(zipp)
    if os.path.exists(caminho):
        print(caminho+" já foi extraido")
    else:
        resultado[caminho] = extrair(zipp, caminho)
print("----------------------------------------------\nITENS QUE FALHARAM:\n\n")
for item, valor in resultado.items():
    if valor == 'ERRO':
        print(item, "\n")
