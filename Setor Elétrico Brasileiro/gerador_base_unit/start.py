import pandas as pd
import os.path
from IPython.display import display
from model.odise import OdiSE
from model.linha import Linha
from controller.loader_getters import *
from controller.verify import *

'''
    Gerador de pré-base de unitização, baseado em planilha modelo
     
'''

# Run

arquivo = input("Digite o caminho até a planilha de geração: ")
caminho, nome = os.path.split(arquivo)
destino = os.path.join(caminho, ("Gerr_"+nome))

sheetnames, sheets = loadSheets(arquivo)

# instancia um objeto de ODI que recebe as informações basicas e comuns a toda ODI
odi = OdiSE(
    nome=sheets["ODI"].loc[2, "VALOR"],
    num=sheets["ODI"].loc[3, "VALOR"],
    cc=sheets["ODI"].loc[0, "VALOR"],
    loc=sheets["ODI"].loc[1, "VALOR"],
    tipo=sheets["ODI"].loc[9, "VALOR"],
    ti=sheets["ODI"].loc[5, "VALOR"],
    cm1=sheets["ODI"].loc[6, "VALOR"],
    cm3=sheets["ODI"].loc[7, "VALOR"],
    setores=sheets["ODI"].loc[4, "VALOR"],
    faseamento=sheets["ODI"].loc[8, "VALOR"])

setores = odi.getSetores()
# print(setores)
modcontagem = getModContagem(sheets, setores)
# print(modcontagem)
modnomes = getModNomes(sheets, setores)
# print(modnomes)
espec = getEspec(sheets, setores, modcontagem)
# for key, value in espec.items():
#     print(key)
#     for nome_arranjo,itens_arranjos in value.items():
#         print(nome_arranjo,"\n",itens_arranjos,"\n+++++++\n")

eqps = getEqps(sheets, setores)
# print(eqps)
subs = getSubs(sheets, setores)
# print(subs)
adds = getAdds(sheets, setores)
# print(adds)
# pré - instancia da base
base = list()

# para cada um dos setores
for setor in setores:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("CARREGAMENTO INICIADO PARA COM O SETOR "+str(setor))
    # Observo no ModContagem quais os arranjos que teremos e para cada um dos arranjos...
    for linha in modcontagem[setor].to_dict('records'):
        print(modcontagem[setor])
        tipo_arranjo = linha["ARRANJO"]
        print("=================")
        print("ARRANJO DO TIPO "+tipo_arranjo)
        # Salvo em uma variavel os nomes e a sigla dos bays correspondentes
        bays = modnomes[setor].loc[modnomes[setor]["ARRANJO"] == tipo_arranjo, [
            "NUMERO ID", "NOME", "SIGLA"]].to_dict("records")
        print(bays)
        # Para cada um dos bays salvos...
        for bay in bays:
            print("##############################")
            print("BAY "+bay["NOME"])
            # Salvo em uma variavel os equipamentos que aquele bay possui (eqp_in_bay)
            print(setor, "\n", tipo_arranjo)
            eqp_in_bay = espec[setor][tipo_arranjo].to_dict("records")
            print("=================")
            print("CONTEM OS SEGUINTES EQUIPAMENTOS:")
            for eqps_in_bay in eqp_in_bay:
                print(eqps_in_bay["EQUIPAMENTO"])
            print("=================")
            # Para cada um dos equipamentos salvos...
            for eqp_individual in eqp_in_bay:
                print("EQUIPAMENTO EM QUESTÃO: "+eqp_individual["EQUIPAMENTO"])
                # salvo a instancia completa do equipamento (segundo aba eqps)
                iinst_eqp = eqps[setor].loc[(eqps[setor]["REFERENCIAÇÃO"] == eqp_individual["EQUIPAMENTO"]) & (
                    eqps[setor]["VARIAÇÃO"] == eqp_individual["VARIAÇÃO"])].to_dict("records")
                print(iinst_eqp)
                # por alguma razão ainda desconhecida, os dados estão sendo retornados na estrutura list>dict, o que fez
                # com que fosse necessário a utilização de um for, para retirarmos de dentro da lista o dict que contem os dados que queremos
                # como trata-se de uma linha que DEVE retornar uma linha unica, a utilização do for como está sendo feita não foge da lógica,
                # porem ainda assim deve-se tentar entender o porque desta linha estar se comportando diferente das outras semelhantes.
                for i in iinst_eqp:
                    inst_eqp = i
                print("CARREGADO/ENCONTRADO COMO "+inst_eqp["EQUIPAMENTO"])
                print("***INICIANDO CADASTRO***")

                if verifObjeto(bayn=bay["NUMERO ID"], objt=eqp_individual["OBJETOS"]) == True:
                    obj_cadastro = dict([
                        ("inst_eqp", inst_eqp), ("odi", odi), ("bay", bay)
                    ])

                    # verifica forma de cadastro do equipamento
                    if inst_eqp["CADASTRAMENTO"] == 1:
                        print(
                            "** Criado objeto de cadastro, forma de cadastro: monofásico")
                        cadMono(
                            base=base, faseeqp=eqp_individual["FASE"], faseamento=odi.faseamento, obj_cadastro=obj_cadastro)
                    elif inst_eqp["CADASTRAMENTO"] == 0:
                        print(
                            "** Criado objeto de cadastro, forma de cadastro: trifásico")
                        cadTrif(base=base, faseamento=odi.faseamento,
                                obj_cadastro=obj_cadastro)

                    # verifica se existem subequipamentos e cadastra se houver
                    if inst_eqp["SUB_EQP"] != "*":
                        if "," in inst_eqp["SUB_EQP"]:
                            print("### Cadastrando os subequipamentos ###")
                            for subeqp in inst_eqp["SUB_EQP"].split(","):
                                iinst_sub = subs.loc[subs["REFERENCIAÇÃO"] == subeqp].to_dict(
                                    'records')
                                for i in iinst_sub:
                                    inst_sub = i
                                # insere campo "tensão" ao inst_sub, uma vez que ele por padrão não possui
                                sub_cadastro = dict([
                                    ("inst_eqp", inst_sub), ("odi",
                                                             odi), ("bay", bay), ("tensao", setor)
                                ])

                                if int(inst_sub["CADASTRAMENTO"]) == 1:
                                    cadMono(
                                        base=base, faseeqp=eqp_individual["FASE"], faseamento=odi.faseamento, obj_cadastro=sub_cadastro)
                                elif int(inst_sub["CADASTRAMENTO"]) == 0:
                                    cadTrif(
                                        base=base, faseamento=odi.faseamento, obj_cadastro=sub_cadastro)
                        else:
                            print("### Cadastrando o subequipamento ###")
                            subeqp = inst_eqp["SUB_EQP"]
                            iinst_sub = subs.loc[subs["REFERENCIAÇÃO"] == subeqp].to_dict(
                                'records')
                            for i in iinst_sub:
                                inst_sub = i
                            sub_cadastro = dict([
                                ("inst_eqp", inst_sub), ("odi",
                                                         odi), ("bay", bay), ("tensao", setor)
                            ])
                            if int(inst_sub["CADASTRAMENTO"]) == 1:
                                cadMono(
                                    base=base, faseeqp=eqp_individual["FASE"], faseamento=odi.faseamento, obj_cadastro=sub_cadastro)
                            elif int(inst_sub["CADASTRAMENTO"]) == 0:
                                cadTrif(base=base, faseamento=odi.faseamento,
                                        obj_cadastro=sub_cadastro)
                    else:
                        print("### Não possui subequipamentos ###")

                    # verifica se existem estruturas adds e cadastra se houver
                    if inst_eqp["ESTRUTURAS ADD"] != "*":
                        if "," in inst_eqp["ESTRUTURAS ADD"]:
                            print("### Cadastrando as estruturas ###")
                            for addest in inst_eqp["ESTRUTURAS ADD"].split(","):
                                iinst_add = adds.loc[adds["REFERENCIAÇÃO"] == addest].to_dict(
                                    'records')
                                for i in iinst_add:
                                    inst_add = i
                                add_cadastro = dict([
                                    ("inst_eqp", inst_add), ("odi",
                                                             odi), ("bay", bay), ("tensao", setor)
                                ])
                                if inst_eqp["CADASTRAMENTO"] == 1:
                                    cadMono(
                                        base=base, faseeqp=eqp_individual["FASE"], faseamento=odi.faseamento, obj_cadastro=add_cadastro)
                                elif inst_eqp["CADASTRAMENTO"] == 0:
                                    cadTrif(
                                        base=base, faseamento=odi.faseamento, obj_cadastro=add_cadastro)
                        else:
                            print("### Cadastrando a estrutura ###")
                            addest = inst_eqp["ESTRUTURAS ADD"]
                            iinst_add = adds.loc[adds["REFERENCIAÇÃO"] == addest].to_dict(
                                'records')
                            for i in iinst_add:
                                inst_add = i
                            add_cadastro = dict([
                                ("inst_eqp", inst_add), ("odi",
                                                         odi), ("bay", bay), ("tensao", setor)
                            ])
                            if inst_eqp["CADASTRAMENTO"] == 1:
                                cadMono(
                                    base=base, faseeqp=eqp_individual["FASE"], faseamento=odi.faseamento, obj_cadastro=add_cadastro)
                            elif inst_eqp["CADASTRAMENTO"] == 0:
                                cadTrif(base=base, faseamento=odi.faseamento,
                                        obj_cadastro=add_cadastro)
                    else:
                        print("### Não possui estruturas ###")

                print("---")

# printBase(base)
print("\n####################################\n####################################\n")
print("Equipamentos devidamente cadastrados!\nGerando planilha...")
xlsx = newModelo(base)
xlsx.to_excel(destino)
print("\n####################################\n####################################\n")
print("Planilha gerada no caminho: ", destino, "\n")
input("Aperte [ENTER] para encerrrar.")
