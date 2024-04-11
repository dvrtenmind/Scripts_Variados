import pandas as pd

'''

    [PROTÓTIPO APENAS PARA REFERÊNCIA, CÓDIGO NÃO FINALIZADO]

    Gerador de balancete mensal padronizado (BMP) através de modelo
    pré-definido de planilha.
'''


def ler_planilha_excel(caminho, sheet_name, col_types=None):
    # Lê a planilha do Excel
    if col_types is not None:
        df = pd.read_excel(caminho, sheet_name=sheet_name,
                           dtype=col_types)
    else:
        df = pd.read_excel(
            caminho, sheet_name=sheet_name)

    return df


def identificar_contas_aneel(df_cliente, df_de_para):
    # Mescla as planilhas com base na correspondência entre conta_cliente e conta_aneel
    resultado = pd.merge(df_cliente, df_de_para,
                         left_on='CONTA CLIENTE', right_on='CONTA CLIENTE', how='inner')

    # Seleciona as colunas desejadas
    colunas_selecionadas = ['CONTA CLIENTE', 'CONTA ANEEL',
                            'SALDO INICIAL', 'DEBITO', 'CREDITO', 'SALDO FINAL']
    resultado = resultado[colunas_selecionadas]

    return resultado


def contas_validas(df1, df2):
    # Obtém uma lista de valores únicos da coluna 'conta_aneel' de df2
    valores_conta_aneel_df2 = df2['CONTA ANEEL'].unique()

    # Filtra as linhas de df1 onde 'conta_aneel' está presente em valores_conta_aneel_df2
    df1_filtrado = df1[df1['CONTA ANEEL'].isin(valores_conta_aneel_df2)]

    return df1_filtrado


def soma_e_comparacao(dataframe):
    # Calcula a soma das colunas 'saldo_inicial', 'saldo_final', 'débito' e 'crédito'
    soma_saldo_inicial = dataframe['SALDO INICIAL'].sum()
    soma_saldo_final = dataframe['SALDO FINAL'].sum()
    soma_debito = dataframe['DEBITO'].sum()
    soma_credito = dataframe['CREDITO'].sum()

    return soma_saldo_inicial, soma_saldo_final, soma_debito, soma_credito


def comparacao(dataframe):
    # Chama a função para calcular as somas
    soma_saldo_inicial, soma_saldo_final, soma_debito, soma_credito = soma_e_comparacao(
        dataframe)

    # Verifica se as somas são iguais
    if soma_saldo_inicial == soma_saldo_final:
        print("Soma de saldo inicial é igual a soma de saldo final!")
    else:
        print("ERRO!\nSoma de saldo inicial não é igual a soma de saldo final!")

    if soma_debito == soma_credito:
        print("Soma de debito é igual a soma de credito!")
    else:
        print("ERRO!\nSoma de saldo inicial não é igual a soma de saldo final!")


def definir_debito_credito(dataframe):
    # Adiciona a coluna 'D/C Inicial' com base no valor de 'saldo_inicial'
    dataframe['D/C Inicial'] = ['D' if valor >
                                0 else 'C' for valor in dataframe['SALDO INICIAL']]

    # Adiciona a coluna 'D/C Final' com base no valor de 'saldo_final'
    dataframe['D/C Final'] = ['D' if valor >
                              0 else 'C' for valor in dataframe['SALDO FINAL']]

    return dataframe


def remover_linhas_vazias_completas(dataframe):
    # Remove as linhas em que todas as colunas especificadas estejam vazias
    dataframe_sem_vazios = dataframe.dropna(
        subset=['SALDO INICIAL', 'SALDO FINAL', 'DEBITO', 'CREDITO'], how='all')

    return dataframe_sem_vazios


def salvar_dataframe_para_excel(dataframe, caminho, nome_arquivo):
    try:
        caminho_completo = f"{caminho}/{nome_arquivo}.xlsx"
        dataframe.to_excel(caminho_completo, index=False)
        print(f"DataFrame salvo com sucesso em {caminho_completo}")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o DataFrame: {e}")


def formatar_valores_texto(dataframe):
    # Função para formatar um valor como texto com apóstrofo e remover '-'
    def formatar_com_apostrofo(valor):
        if isinstance(valor, (int, float)):
            valor = str(valor)
        if valor.startswith('-'):
            return "'" + valor[1:]
        return "'" + valor if valor else ''

    # Aplica a função de formatação às colunas desejadas, ignorando células vazias
    colunas = ['SALDO INICIAL', 'SALDO FINAL', 'DEBITO', 'CREDITO']
    dataframe[colunas] = dataframe[colunas].applymap(
        lambda x: formatar_com_apostrofo(x) if pd.notna(x) else x)

    return dataframe


if __name__ == "__main__":

    # Defina os caminhos para as planilhas
    planilha_cliente = r"C:\Users\User\Documents\ELSCSHAMMAH\bmp\ABRIL 2023\BMP ABR 2023 - AMAPAR_11.09.2023.xlsx"
    planilha_de_para = r"C:\Users\User\Documents\ELSCSHAMMAH\bmp\de_para\DE_PARA - AMAPAR - JUNHO.xlsx"
    planilha_contas_validas = r"C:\Users\User\Documents\ELSCSHAMMAH\bmp\contas_validas\validas.xlsx"

    # Lendo planilha cliente
    tipos_de_dados = {'CONTA CLIENTE': str, 'NOMENCLATURA': str, 'SALDO INICIAL': float,
                      'DEBITO': float, 'CREDITO': float, 'SALDO FINAL': float}
    sheet_name = 'Plan1'
    df_cliente = ler_planilha_excel(
        planilha_cliente, sheet_name, tipos_de_dados)

    # Lendo planilha de_para
    tipos_de_dados = {'CONTA CLIENTE': str, 'DESCRICAO CLIENTE': str, 'CONTA ANEEL': str,
                      'DESCRICAO ANEEL': str}
    sheet_name = 'DE PARA'
    df_de_para = ler_planilha_excel(
        planilha_de_para, sheet_name, tipos_de_dados)

    # Lendo planilha contas_validas
    tipos_de_dados = {'CONTA ANEEL': str}
    sheet_name = 'Plan1'
    df_validas = ler_planilha_excel(
        planilha_contas_validas, sheet_name, tipos_de_dados)

    # Verifique se os DataFrames foram lidos com sucesso
    if df_cliente is not None and df_de_para is not None:
        # Identifica contas da Aneel
        obj = identificar_contas_aneel(df_cliente, df_de_para)

    # Encontra apenas os itens a serem considerados no BMP
    obj = contas_validas(obj, df_validas)

    # Verifica se os valores batem
    comparacao(obj)

    # Definie valores das colunas D/C
    obj = definir_debito_credito(obj)

    # Elimina linhas vazias
    obj = remover_linhas_vazias_completas(obj)

    # Formata como texto
    obj = formatar_valores_texto(obj)

    # Salva resultado em planilha
    path = r"C:\Users\User\Documents\ELSCSHAMMAH\bmp\JULHO 2023\gerado"
    salvar_dataframe_para_excel(obj, path, "BMP")
