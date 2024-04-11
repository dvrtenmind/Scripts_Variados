from PIL import Image, ImageEnhance
import os
import matplotlib.pyplot as plt

'''
    Auto editor de imagens aplicando configurações pré-definidas.
    Tem como objetivo padronizar diversas imagens em um padrão específico
    de cor/escala que torne possível a correta validação e verificação de
    dados textuais contidos nas imagens.
    
    (Necessita de alteração para cada caso específico de cada grupo de imagens)
    
'''


def editar_imagem(caminho_imagem, pasta_editada):
    # Cria a pasta "editada" se não existir
    if not os.path.exists(pasta_editada):
        os.makedirs(pasta_editada)

    # Obtém o nome do arquivo e a extensão da imagem
    nome_arquivo, extensao = os.path.splitext(os.path.basename(caminho_imagem))

    # Abre a imagem
    imagem = Image.open(caminho_imagem)

    # Aplica as alterações
    gamma = 0.5
    brilho = 0.7
    contraste = 3
    matiz = -13
    saturacao = 1.7

    # Aplica Brilho
    imagem = ImageEnhance.Brightness(imagem).enhance(brilho)

    # Aplica Contraste
    imagem = ImageEnhance.Contrast(imagem).enhance(contraste)

    # Aplica Saturação
    imagem = ImageEnhance.Color(imagem).enhance(saturacao)

    # # Aplica Matiz
    # imagem_matiz = imagem.convert('HSV')
    # h, s, v = imagem_matiz.split()
    # h = h.point(lambda i: (i + matiz) % 256)  # Tratamento do canal de matiz
    # imagem_matiz = Image.merge('HSV', (h, s, v))
    # imagem_matiz = imagem_matiz.convert('RGB')

    # Aplica Gama
    imagem = ImageEnhance.Brightness(
        imagem).enhance(gamma)

    # Exibe a imagem antes de salvar
    plt.imshow(imagem)
    plt.title('Imagem Editada')
    plt.show()

    # Salva a imagem editada na pasta "editada"
    caminho_imagem_editada = os.path.join(
        pasta_editada, f'{nome_arquivo}_editada{extensao}')
    imagem.save(caminho_imagem_editada)

    print(f'Imagem editada salva em: {caminho_imagem_editada}')


if __name__ == "__main__":
    # Caminho da imagem original
    caminho_imagem_original = input(
        'Por favor digite o caminho para a imagem original:\n')

    # Pasta para salvar a imagem editada
    pasta_editada = os.path.join(os.path.dirname(
        caminho_imagem_original), "editada")

    # Edita a imagem
    editar_imagem(caminho_imagem_original, pasta_editada)
