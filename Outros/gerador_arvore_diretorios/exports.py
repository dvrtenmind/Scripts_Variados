import os
import xlsxwriter
import json


def exp_excel(dirfiles, raiz):
    sheetname = os.path.join(raiz, "mapeamento.xlsx")
    planilha = xlsxwriter.Workbook(sheetname)

    sheet = planilha.add_worksheet("diretorios")
    vazios = planilha.add_worksheet("vazios")
    row = 0
    col = 0
    vrow = 0
    vcol = 0
    num_dir = 0
    for diretorio in dirfiles:
        qtd_arq = len(diretorio)
        if qtd_arq > 1:
            sheet.write(row, col, num_dir)
            col = 2
            sheet.write(row, col, diretorio['nome'])
            col = 3
            sheet.write(row, col, str((qtd_arq-1))+" arquivos")
            row += 1
            col = 1
            n = 0
            while (n < qtd_arq):
                if n != 0:
                    sheet.write(row, col, n)
                    col = 2
                    sheet.write(row, col, diretorio[n])
                    file_name, file_extension = os.path.splitext(diretorio[n])
                    col = 3
                    sheet.write(row, col, file_extension)
                    col = 1
                    row += 1
                n += 1
            col = 0
            num_dir += 1
        else:
            vazios.write(vrow, vcol, diretorio['nome'])
            vrow += 1

    planilha.close()
    print(f"Arquivo exportado em excel no caminho: {sheetname}")


def exp_json(dirfiles, raiz):
    nome_arquivo = os.path.join(raiz, "mapeamento.json")
    with open(nome_arquivo, "w") as arquivo_json:
        json.dump(dirfiles, arquivo_json, indent=4)
    print(f"Arquivo exportado em json no caminho: {nome_arquivo}")


def errors_json(errors, raiz):
    nome_arquivo = os.path.join(raiz, "errors.json")
    with open(nome_arquivo, "w") as arquivo_json:
        json.dump(errors, arquivo_json, indent=4)
    print(f"Logs de erro exportados em json no caminho: {nome_arquivo}")
