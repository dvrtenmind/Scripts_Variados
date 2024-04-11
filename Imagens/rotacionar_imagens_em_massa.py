from PIL import Image
import pathlib
import shutil

'''
    Ferramenta utilizada para tratamento em massa de imagens recebidas
    pela equipe de fotografias em campo, necessária para padronização e
    processos de pré-análise que são executados em seguida.
    Mostrou-se mais efetivo do que a tarefa manual de rotacionar imagens.
'''


def direita(path):
    diretorio = path + "\\direita"
    imagens = list(pathlib.Path(diretorio).glob("**/*JPG"))
    # print(diretorio, imagens)
    for img in imagens:
        nome = str(img).split('\\').pop()
        print("Girando " + nome + " para a direita")
        imagem = Image.open(img)
        rotated_image1 = imagem.transpose(Image.Transpose.ROTATE_270)
        rotated_image1.save(path + "\\" + nome)
        print(nome + " girada com sucesso e salva no diretório raiz.")


def esquerda(path):
    diretorio = path + "\\esquerda"
    imagens = list(pathlib.Path(diretorio).glob("**/*jpg"))
    # print(diretorio, imagens)
    for img in imagens:
        nome = str(img).split('\\').pop()
        print("Girando " + nome + " para a esquerda")
        imagem = Image.open(img)
        rotated_image1 = imagem.transpose(Image.Transpose.ROTATE_90)
        rotated_image1.save(path + "\\" + nome)
        print(nome + " girada com sucesso e salva no diretório raiz.")


def cabeca_baixo(path):
    diretorio = path + "\\cabeca_baixo"
    imagens = list(pathlib.Path(diretorio).glob("**/*jpg"))
    print(diretorio, imagens)
    for img in imagens:
        nome = str(img).split('\\').pop()
        # print("Girando "+ nome + " para cima")
        imagem = Image.open(img)
        rotated_image1 = imagem.transpose(Image.Transpose.ROTATE_180)
        rotated_image1.save(path + "\\" + nome)
        print(nome + " girada com sucesso e salva no diretório raiz.")


def reduzir(path, destino):
    diretorio = path
    imagens = list(pathlib.Path(diretorio).glob("**/*JPG"))
    print(diretorio, imagens)
    for img in imagens:
        nome = str(img).split('\\').pop()
        # print("Reduzindo "+ nome + " para 7/% de seu tamanho original")
        imagem = Image.open(img)
        original_size = imagem.size()
        print(original_size)
        # resized_image = imagem.resize()
        # rotated_image1 = imagem.transpose(Image.Transpose.ROTATE_180)
        # rotated_image1.save(path + "\\" + nome)
        # print(nome + " girada com sucesso e salva no diretório raiz.")


origem = (r'\\192.168.1.5\dados\Projetos7 - CLIENTES - 2022\21 - PRJ_ELSC_214_2022_H2M_FURNAS\INVENTÁRIO\FOTOS LUCAS VIANA\ORIGINAIS\SE ADRIANÓPOLIS')
destino = (r'\\192.168.1.5\dados\Projetos7 - CLIENTES - 2022\21 - PRJ_ELSC_214_2022_H2M_FURNAS\INVENTÁRIO\FOTOS LUCAS VIANA\REDUZIDOS')

# direita(origem)
# esquerda(origem)
# cabeca_baixo(origem)
reduzir(origem, destino)
