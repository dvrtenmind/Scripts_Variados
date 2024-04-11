import subprocess
import psutil
import json
import time
import os
import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

'''
    Script criado para auxiliar na padronização e documentação das maquinas
    de rede coorporativa.
    Padroniza nomenclaturas de computadores seguindo padrão guiado por nome 
    de usuário (padrão previamente estabelecido) e obtem informações relevantes
    referentes a máquina para correta identificação da mesma nos controles 
    internos do setor de tecnologia.
'''


def get_powershell():
    enable_command = "DISM /Online /Enable-Feature /FeatureName:MicrosoftWindowsPowerShellV2"
    subprocess.run(enable_command, shell=True)
    time.sleep(5)
    os.system("cls")


def select_func():
    list = {
        '001': 'User 1',
        '002': 'User 2',
        '003': 'User 3',
        '004': 'User 4',
    }
    message = ""
    for key, value in list.items():
        message += f"{key} - {value}\n"
    print("Por favor informe o numero que corresponde ao seu id de funcionario (com 3 dígitos):")
    number = input((message+"\n\nR:"))
    for key, value in list.items():
        if number == key:
            os.system("cls")
            return {'id': key, 'nome': value}
    os.system("cls")
    print("Desculpe não entendi sua resposta, por favor tente novamente!\n\n")
    return select_func()


def change_name(new_name):
    powershell_command = f'Rename-Computer -NewName "{new_name}" -Force'
    os.system(f'powershell.exe -Command "{powershell_command}"')


def get_network_info():
    network_info = {}
    interfaces = psutil.net_if_addrs()

    for interface, addrs in interfaces.items():
        network_info[interface] = {}
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                network_info[interface]['mac'] = addr.address
    return network_info


def save_network_info(path, name, machine_name, data):
    try:
        path_file = f"{path}\{name}_{machine_name}.json"
        json_data = json.dumps(data, indent=4)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path_file, "w") as arquivo_json:
            arquivo_json.write(json_data)
        print("-------------\nColetado!\n-------------")
        return path_file
    except WindowsError as e:
        print("-------------\nDesculpe ocorreu um erro\n-------------")
        print(e)


def sendind_infos(path_file):
    # Configurações do servidor SMTP do seu domínio
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Porta SMTP específica do seu servidor
    smtp_user = 'email@gmail.com'
    smtp_password = 'jmdk aswi qrkz ozmn'

    # Criar uma mensagem
    subject = "NETWORK INFO"
    from_email = smtp_user
    to_email = "ti@elsc.com.br"
    message_text = "Email Automatico"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_text, 'plain'))

    # Abrir e anexar o arquivo ao email
    with open(path_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{path_file.split("/")[-1]}"',
        )
        msg.attach(part)

    # Iniciar a conexão com o servidor SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Habilitar a criptografia TLS
        server.login(smtp_user, smtp_password)

        # Enviar o e-mail
        server.sendmail(from_email, to_email, msg.as_string())
        print("-------------\Enviado!\n-------------")

    except Exception as e:
        print("-------------\nDesculpe ocorreu um erro\n-------------")
        print(e)

    finally:
        # Encerrar a conexão com o servidor SMTP
        server.quit()


def clear_arquive(path_file):
    try:
        os.remove(path_file)
        print("-------------\Finalizado!\n-------------")
    except OSError as e:
        print("-------------\nDesculpe ocorreu um erro\n-------------")
        print(e)


def aviso():
    print("\n\n\n-----------------\nPOR FAVOR NÃO FECHE O PROGRAMA ATÉ QUE ELE PEÇA PARA FECHAR\n-----------------\n")
    print("Isto pode demorar um pouco...")
    time.sleep(3)
    os.system("cls")


if __name__ == "__main__":
    aviso()
    get_powershell()
    func = select_func()
    machine_name = f"ELSC{func['id']}"
    change_name(machine_name)
    network_info = get_network_info()
    path = r"C:\Network_info"
    path_file = save_network_info(
        path, func['nome'], machine_name, network_info)
    sendind_infos(path_file)
    clear_arquive(path_file)
    input("'Enter' para fechar")
