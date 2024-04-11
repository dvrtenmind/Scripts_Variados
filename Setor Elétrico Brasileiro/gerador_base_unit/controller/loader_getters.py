import pandas as pd
from IPython.display import display

    ########################################################################################################################
    # loader

def loadSheets(arquivo):
        # pré-carrega o arquivo excel para podermos extrair o nome das planilhas equivalentes
        xl = pd.ExcelFile(arquivo)

        # salva um objeto de lista contendo os nomes de todas as sheets dentro do arquivo xlsx
        sheetnames = xl.sheet_names

        #instancia o dict que irá receber as instancias de cada uma das abas
        sheets = dict()

        #salva uma instancia de cada aba existente no arquivo
        for planilha in sheetnames:
            sheets[planilha] =pd.read_excel(io = arquivo,sheet_name= planilha)    
        return sheetnames, sheets

    ########################################################################################################################
    # getters

def getModContagem(sheets,setores):
        # extrair a contagem de cada um dos modulos(mcpse) relacionados a cada um dos setores
        modcontagem = dict()
        for setor in setores:
            modcontagem[setor] = (sheets["MOD_CONTAGEM"].loc[sheets["MOD_CONTAGEM"]["SETOR"]==setor])
        return modcontagem

def getModNomes(sheets, setores):
        # extrair dados da sheet de nomeação dos modulos mcpse e salvar esta informação em um objeto arranjos
        modnomes = dict()    
        for setor in setores:
            modnomes[setor] = sheets["MOD_NOMES"].loc[sheets["MOD_NOMES"]["SETOR"]==setor]
        return modnomes    
            
def getEspec(sheets, setores,modcontagem):
        # extrair dados da sheet de especificação de arranjos e salvar em um objeto espec
        espec = dict()
        for setor in setores:
            espec[setor]=dict()
            arranjo_itens = sheets["MOD_ESPEC"].loc[(sheets["MOD_ESPEC"]["SETOR"]==setor)]
            # print(arranjo_itens.loc[0:,"TIPO"].drop_duplicates())
            for arranjo in arranjo_itens.loc[0:,"TIPO"].drop_duplicates():
                espec[setor][arranjo] = arranjo_itens.loc[arranjo_itens["TIPO"]==arranjo]    
        return espec


def getEqps(sheets, setores):
        # extrair todos os modelos de equipamentos e salvar em um array separando por setores
        eqps = dict()
        for setor in setores:
            eqps[setor] = sheets["EQPS"].loc[sheets["EQPS"]["TENSÃO"]==setor]
        return eqps  

def getSubs(sheets, setores):
        # extrair todos os modelos de subequipamentos e salvar em um array contendo os adds    
        subs = sheets["SUBS"]
        return subs

def getAdds(sheets, setores):
        # extrair todos os modelos de add e salvar em um array contendo os adds
        adds = sheets["ADDS"]
        return adds


def printBase(base):
    print("Visualização do arquivo de base: \n")
    for item in base:
        print(item)
        print("---")
        
def save(base, item):
    if len(item)>1:
        print(item)
        for linha in item:
            base.append(linha)
            pause
        else:
            
            pause
            base.append(item)