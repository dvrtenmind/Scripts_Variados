import os
import shutil
'''
    Script simples com a finalidade de mover imagens de um tipo específico 
    de um caminho para o outro, é utilizado em alternativa a opção de mover
    do próprio explorador de arquivos do windows e se mostrou mais efetiva
    em casos onde é necessária esta movimentação em massa.
    Também pode ser utilizado como subferramenta para tarefas de re-organização
    de diretórios.
'''
# Diretório de origem das fotos
source_dir = input("Digite o caminho de origem: ")

# Diretório de destino para as fotos copiadas
dest_dir = input("Digite o caminho final: ")

# Cria o diretório de destino caso não exista
os.makedirs(dest_dir, exist_ok=True)

# Iterar sobre todas as pastas e subpastas do diretório de origem
for subdir, dirs, files in os.walk(source_dir):
    # Copiar cada arquivo na pasta atual
    for file in files:
        # Verificar se o arquivo é uma foto (por exemplo, formato .jpg)
        filename, extension = os.path.splitext(file)
        if extension.upper() in ['.JPG', '.JPEG', '.PNG']:
            # Construir o caminho completo do arquivo de origem e destino
            src_path = os.path.join(subdir, file)
            dest_path = os.path.join(dest_dir, file)
            # Copiar o arquivo para o diretório de destino
            shutil.copy2(src_path, dest_path)
            print(file + " copiado para novo caminho.")
print("\n...\nFim de operação.")
