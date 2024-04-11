import os
import pandas as pd

'''
    Este script é um auxiliar do gerador de relatórios fotográficos (que você
    pode encontrar o código no meu github)
    
    Recebe um XLSX de geração de relatório fotográfico que contenha nos campos 
    de imagem o caminho para as pastas onde devem haver as imagens a serem 
    inseridas no relatório, o script então valida os caminhos e os substitui
    pela primeira imagem que for encontrada nele, facilitando assim o trabalho para
    a geração dos relatórios fotográficos (desde que bem separadas e definidas
    as imagens dentro dos padrões definidos).
    
'''

# Solicite ao usuário o caminho do arquivo
arquivo_excel = input("Por favor, insira o caminho do arquivo Excel: ")

# Leia a planilha 'Data' do arquivo Excel
df = pd.read_excel(arquivo_excel, sheet_name='Data')

# Para cada coluna especificada
for coluna in ['Id Torre', 'Estrutura', 'Levantamento']:
    # Verifique se a coluna existe no DataFrame
    if coluna in df.columns:
        # Para cada item na coluna
        for i, item in enumerate(df[coluna]):
            # Tente abrir o caminho especificado
            try:
                # Obtenha a lista de arquivos no diretório
                arquivos = os.listdir(item)
                # Encontre o primeiro arquivo .JPG
                arquivo_jpg = next(
                    (arquivo for arquivo in arquivos if arquivo.endswith('.JPG')), None)
                # Se um arquivo .JPG foi encontrado
                if arquivo_jpg is not None:
                    # Substitua o item pelo nome do arquivo .JPG
                    df.at[i, coluna] = os.path.join(item, arquivo_jpg)
                else:
                    print(
                        f"Nenhum arquivo .JPG encontrado na linha {i+1} para a coluna '{coluna}'.")
            except FileNotFoundError:
                # Se o caminho não existir, imprima uma mensagem de erro e continue para o próximo item
                print(
                    f"Caminho inválido na linha {i+1} para a coluna '{coluna}'.")
                continue

# Crie um novo arquivo Excel com os dados atualizados
nome_novo_arquivo = os.path.splitext(arquivo_excel)[0] + '_processado.xlsx'
df.to_excel(nome_novo_arquivo, index=False)

print(f"Arquivo processado salvo como {nome_novo_arquivo}")
