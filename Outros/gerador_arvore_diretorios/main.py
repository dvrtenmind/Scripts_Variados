from formules import process
from concurrent.futures import ThreadPoolExecutor

'''
    Script que recebe uma lista de diretórios e para cada
    um deles realiza uma varredura em seus conteudos (arquivos
    e subdiretórios), retornando em formato XLSX as subspastas,
    quantidades de arquivos, extensões e nomes dos arquivos para
    posteriormente estes dados serem analisados.
'''

# raiz = input("Informe o caminho para o diretório: \n")
# process(raiz)

diretorios = [
    r"Z:\Projetos\MSG",
]

with ThreadPoolExecutor(max_workers=None) as executor:
    resultados = list(executor.map(process, diretorios))
