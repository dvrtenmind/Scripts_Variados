import pandas as pd
from IPython.display import display
from model.linha import Linha

########################################################################################################################
# verificadores
        
def verifObjeto(bayn,objt):
    #valido se o item deve ser aplicado em todos os objetos ou apenas um
    # se objt for diferente de 0 significa que não deve ser cadastrado em todos os objetos
    print("* Verificação de objetos")
    cadastrar = False
    if objt != 0:
        # se objt possuir - significa que deve ser aplicada naquele intervalo especifico de numero x até y
        if "-" in str(objt):
            print("= Encontrado intervalo de aplicação do equipamento")
            splits = objt.split("-")
            for obj in range(int(splits[0]),int(splits[1])):
                if obj == bayn:
                    cadastrar = True
        # se objt possuir virgula significa que deve ser aplicado apenas naqueles objetos especificos, exemplo: objt x e objt y (quando "x,y") 
        elif "," in str(objt):
            print("= Encontrado objetos de aplicação do equipamento")
            for obj in objt.split(","):
                if obj == bayn:
                    cadastrar= True
        else:
        # se objt não possuir nem virgula nem traço mas entrou dentro do for, é porque trata-se de um equipamento de um objeto unico
            print("= Encontrado objeto único de aplicação do equipamento")
            if objt == bayn:
                cadastrar = True        
    else:
    #se objt não entrar no loop do "!=0" significa que é comum a todos
        print("= Equipamento aplicavel a todos os objetos")
        cadastrar=True
    if  cadastrar == True:
        "O equipamento será cadastrado no bay em questão!"
    else:
        "O equipamento não é aplicavel no bay em questão!"
    return cadastrar
    
def verifAdds(inst_eqp,eqp_cad,odi,adds):
    if inst_eqp["ESTRUTURAS ADD"] != "NaN":
        est_adds = inst_eqp["ESTRUTURAS ADD"]
        setor = eqp_cad.tensaoodi
        fase = eqp_cad.fase
        bay = eqp_cad.bay
        if "," not in est_adds:
            inst_add = adds.loc[adds["REFERENCIAÇÃO"] == est_adds]
            linha= newRow(inst_eqp=inst_add,setor=setor,odi=odi,fase=fase,bay=bay)
        else:
            for est_add in est_adds.split(","):
                inst_add = adds.loc[adds["REFERENCIAÇÃO"] == est_add]
                linha= newRow(inst_eqp=est_add,setor=setor,odi=odi,fase=fase,bay=bay)
    else:
        return False
    
########################################################################################################################
# cadastradores
    
def cadTrif(faseamento, obj_cadastro,base):
    obj_cadastro["FASE"]=faseamento
    linha = newRow(obj_cadastro)
    base.append(linha)

def cadMono(faseeqp,faseamento, obj_cadastro,base):
    if faseeqp == 0:
        # se faseeqp == 0, sera cadastrado uma linha para cada uma das fases especificadas na odi (faseamento)
        for fase in faseamento.split("-"):
            obj_cadastro["FASE"]=fase
            base.append(newRow(obj_cadastro))
    elif "-" in faseeqp:
        # se não, se faseeqp possuir "-", divide-se ela pelos "-" e é cadastrada uma instancia para cada uma das partes
        for faseseqp in faseeqp.split("-"):
            obj_cadastro["FASE"]=faseseqp
            base.append(newRow(obj_cadastro))
    else:
        # se não, signfica que é aplicavel em apenas uma fase, logo, o equipamento é cadastrado apenas nesta correspondencia
        obj_cadastro["FASE"]=faseeqp
        base.append(newRow(obj_cadastro))

########################################################################################################################
# Instanciadores

def newModelo(itens):
    base_modelo = [
        "IDUC-ID","DÍGITO SEQUENCIAL","DATA INVENTÁRIO","CONTRATO DE CONCESSÃO","LOCALIZAÇÃO",
        "NOME DA ODI","TENSÃO","NUMERO DA ODI","TIPO DA SE", "TI","DESCRIÇÃO-TI","CM - DIGITO 1",
        "CM1-SIGLA","DESCRIÇÃO LOCAL DE INSTALAÇÃO","CM - DIGITO 2","CM2-SIGLA","DESCRIÇÃO/COMPOSIÇÃO",
        "CM - DIGITO 3","CM3-SIGLA","DESCRIÇÃO ARRANJO FÍSICO","CM","UC","DESCRIÇÃO UC","UC + A1",
        "DESCRIÇÃO UC+A1","A1","A2","A3","A4","A5","A6","TABELA A2","TABELA A3","TABELA A4","TABELA A5",
        "TABELA A6","VALOR A2","VALOR A3","VALOR A4","VALOR A5","VALOR A6","CÓDIGO DA UAR","UC + UAR",
        "DESCRIÇÃO UAR","CODIFICAÇÃO","IDUC","BAY/LOCALIZAÇÃO","ID MODULO","ID RECEITA","NOME SIGET",
        "SIGLA EQP","TAG","TAG+FASE","EQUIPAMENTO-BAY-FASE","QUANTIDADE","UNIDADE",
        "ANO DE FABRICAÇÃO","FABRICANTE","LOCAL DE INSTALAÇÃO","MODELO / TIPO","NR SÉRIE","TENSÃO NOMINAL",
        "FASE","DESCRIÇÃO AUTOMATICA","DESCRIÇÃO DO EQUIPAMENTO","ENTRADA DE OPERAÇÃO","DATA DE IMOBILIZAÇÃO",
        "TAXA DEPRECIAÇÃO","VU - VIDA UTIL","FOTO 1","FOTO 2","FOTO 3","UAR/UC","NUM_H2M","NUM_INV (INV ANTERIOR)",
        "NUM_INV (GERADO)",
    ]
    base = pd.DataFrame(itens,columns=base_modelo)
    return base


def newRow(obj_cadastro):
    print("Especificado Centro Modular")
    # validação da forma de cadastro do cm
    if str(obj_cadastro["inst_eqp"]["EQUIPAMENTO"]) == "P_CARRIER":
        cm2 = 1
    else:
        cm2 = 2
        
    # validação se existe ["setor"] e ["tensao"], em casos como sub_eqps ou adds, esta chave existe, em casos como equipamentos principais fica implicito
    if "tensao" in obj_cadastro:
        inst = ("SETOR "+str(obj_cadastro["tensao"]))
    else:
        inst = ("SETOR "+ str(obj_cadastro["inst_eqp"]["TENSÃO"])) 
        
    if "tensao" in obj_cadastro:
        tensao = obj_cadastro["tensao"]
    else:
        tensao = obj_cadastro["inst_eqp"]["TENSÃO"] 
    
    # criação do objeto de linha que será cadastrado 
    linha = {
        "IDUC-ID":"@@@=[@Iduc]",
        "DÍGITO SEQUENCIAL":"",
        "DATA INVENTÁRIO":"",
        "CONTRATO DE CONCESSÃO":obj_cadastro["odi"].cc,
        "LOCALIZAÇÃO":obj_cadastro["odi"].loc,
        "NOME DA ODI":obj_cadastro["odi"].nome,
        "TENSÃO":obj_cadastro["odi"].setores, 
        "NUMERO DA ODI":obj_cadastro["odi"].num,
        "TIPO DA SE":obj_cadastro["odi"].tipo, 
        "TI":obj_cadastro["odi"].ti,
        "DESCRIÇÃO-TI":"@@@=PROCV(J2;TI!$A$1:$B$52;2;)",
        "CM - DIGITO 1":obj_cadastro["odi"].cm1,
        "CM1-SIGLA":"@@@=PROCV([@[CM - DIGITO 1]];CM!$A$2:$C$5;2;)",
        "DESCRIÇÃO LOCAL DE INSTALAÇÃO":"@@@=PROCV([@[CM - DIGITO 1]];CM!$A$2:$C$5;3;)",
        "CM - DIGITO 2":cm2,
        "CM2-SIGLA":"@@@=PROCV([@[CM - DIGITO 2]];'CM2'!$A$2:$C$11;2;)",
        "DESCRIÇÃO/COMPOSIÇÃO":"@@@=PROCV([@[CM - DIGITO 2]];'CM2'!$A$2:$C$11;3;)",
        "CM - DIGITO 3":obj_cadastro["odi"].cm3,
        "CM3-SIGLA":"@@@=PROCV([@[CM - DIGITO 3]];'CM3'!$A$2:$C$7;2;)",
        "DESCRIÇÃO ARRANJO FÍSICO":"@@@=PROCV([@[CM - DIGITO 3]];'CM3'!$A$2:$C$7;3;)",
        "CM":"@@@=[@[CM - DIGITO 1]]&[@[CM - DIGITO 2]]&[@[CM - DIGITO 3]]",
        "UC":obj_cadastro["inst_eqp"]["UC"],
        "DESCRIÇÃO UC":"@@@=PROCV([@UC];TUC!$A$2:$B$106;2;)",
        "UC + A1":'@@@=[@UC]&"."&[@A1]',
        "DESCRIÇÃO UC+A1":"@@@=PROCV([@UC];TUC!$A$2:$B$106;2;)",
        "A1":obj_cadastro["inst_eqp"]["A1"],
        "A2":obj_cadastro["inst_eqp"]["A2"],
        "A3":obj_cadastro["inst_eqp"]["A3"],
        "A4":obj_cadastro["inst_eqp"]["A4"],
        "A5":obj_cadastro["inst_eqp"]["A5"],
        "A6":obj_cadastro["inst_eqp"]["A6"],
        "TABELA A2":"@@@=PROCV([@[UC + A1]];'UCS+A1'!$A$2:$I$221;5;)",
        "TABELA A3":"@@@=PROCV([@[UC + A1]];'UCS+A1'!$A$2:$I$221;6;)",
        "TABELA A4":"@@@=PROCV([@[UC + A1]];'UCS+A1'!$A$2:$I$221;7;)",
        "TABELA A5":"@@@=PROCV(W2;'UCS+A1'!$A$2:$I$221;8;)",
        "TABELA A6":"@@@=PROCV([@[UC + A1]];'UCS+A1'!$A$2:$I$221;9;)",
        "VALOR A2":"",
        "VALOR A3":"",
        "VALOR A4":"",
        "VALOR A5":"",
        "VALOR A6":"",
        "CÓDIGO DA UAR":obj_cadastro["inst_eqp"]["UAR"],
        "UC + UAR":"@@@=[@UC]&[@[CÓDIGO DA UAR]]",
        "DESCRIÇÃO UAR":"@@@=PROCV([@[UC + UAR]];UAR!$A$2:$H$1268;3;)",
        "CODIFICAÇÃO":"",
        "IDUC":'@@@=[@[UC + A1]]&"."&[@[DÍGITO SEQUENCIAL]]',
        "BAY/LOCALIZAÇÃO":obj_cadastro["bay"]["SIGLA"],
        "ID MODULO":"",
        "ID RECEITA ":"",
        "NOME SIGET":"",
        "SIGLA EQP":obj_cadastro["inst_eqp"]["REFERENCIAÇÃO"],
        "TAG":obj_cadastro["inst_eqp"]["TAG"],
        "TAG+FASE":'@@@=[@TAG]&"-"&[@FASE]',
        "EQUIPAMENTO-BAY-FASE":'@@@=[@[SIGLA EQP]]&"-"&[@[BAY/LOCALIZAÇÃO]]&"-"&[@FASE]',
        "QUANTIDADE":1,
        "UNIDADE":"UNIDADE",
        "ANO DE FABRICAÇÃO":obj_cadastro["inst_eqp"]["ANO"],
        "FABRICANTE":obj_cadastro["inst_eqp"]["FABRICANTE"],
        "LOCAL DE INSTALAÇÃO": inst, 
        "MODELO / TIPO":obj_cadastro["inst_eqp"]["MODELO"],
        "NR SÉRIE":obj_cadastro["inst_eqp"]["NR_SERIE"], 
        "TENSÃO NOMINAL":tensao,
        "FASE":obj_cadastro["FASE"],
        "DESCRIÇÃO AUTOMATICA":'@@@=[@[DESCRIÇÃO DO EQUIPAMENTO]]&" LOCALIZADO NO "&[@[BAY/LOCALIZAÇÃO]]&" TAG "&[@[TAG+FASE]]',
        "DESCRIÇÃO DO EQUIPAMENTO":obj_cadastro["inst_eqp"]["NOME"],
        "ENTRADA DE OPERAÇÃO":"",
        "DATA DE IMOBILIZAÇÃO":"",
        "TAXA DEPRECIAÇÃO":"@@@=PROCV([@[UC + A1]];'TX - RN 674-2015 BSBOYS'!C:F;4;FALSO)",
        "VU - VIDA UTIL":"@@@=PROCV([@[UC + A1]];'TX - RN 674-2015 BSBOYS'!C:F;3;FALSO)",
        "FOTO 1":"DSCN",
        "FOTO 2":"DSCN",
        "FOTO 3":"DSCN",
        "UAR/UC":"@@@=PROCV([@[UC + UAR]];uc_uar_definição!A:C;3;FALSO)",
        "NUM_H2M":"@@@=PROCV([@[IDUC-ID]];NUM_H2M!A:B;2;FALSO)",
        "NUM_INV (INV ANTERIOR)":"",
        "NUM_INV (GERADO)":"@@@=PROCV([@[IDUC-ID]];NUM_INV!B:C;2;FALSO)",
        }
    print("***Equipamento cadastrado com sucesso!!***")
    
    return linha