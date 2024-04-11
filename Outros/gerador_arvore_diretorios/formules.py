import os
from exports import exp_excel, errors_json

# armazenará o nome de todos os diretorios
dirs = list()
# armazenará os arquivos de todos os diretorios
dirfiles = list()
errors = list()


def listdirs(rootdir):
    try:
        listagem = os.listdir(rootdir)
    except OSError as e:
        errors.append([f"Ocorreu um erro ao listar o diretório: {e}", rootdir])
        print(f"Ocorreu um erro ao listar o diretório: {e}")
    else:
        for file in listagem:
            d = os.path.join(rootdir, file)
            if os.path.isdir(d):
                print("+", end="")
                dirs.append(d)
                listdirs(d)
            else:
                print(".", end="")


def getFiles(diretorio):
    result = dict()
    result['nome'] = diretorio
    n = 1
    try:
        for file in os.listdir(diretorio):
            try:
                arquivo = os.path.join(diretorio, file)
                if os.path.isfile(arquivo):
                    result[n] = file
                    n += 1
                    print("+", end="")
            except OSError as e:
                errors.append([
                    f"Ocorreu um erro ao verificar arquivo: {e}",
                    arquivo
                ])
                print("?", end="")
                None
    except OSError as e:
        errors.append([
            f"Ocorreu um erro ao verificar arquivos dentro do diretorio: {e}",
            diretorio
        ])
        print("???")
    return result


def process(raiz):
    listdirs(raiz)
    for diretorio in dirs:
        print("\nlistando arquivos em diretorio\n")
        dirfiles.append(getFiles(diretorio))

    print("Todos os diretórios verificados")
    try:
        print("Erros:")
        for item in errors:
            print(item[0], "  -  ", item[1])
    except OSError as e:
        print(e)
    try:
        exp_excel(dirfiles, raiz)
        errors_json(errors, raiz)
    except OSError as e:
        print(e)
        input("Erro ao exportar")
    # input("Pressione [enter] para fechar")
