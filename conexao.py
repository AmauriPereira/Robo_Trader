from iqoptionapi.stable_api import IQ_Option
import time


def conexao_iqoption(tipo_conta, email, senha):

    erro_senha = "Você inseriu as credenciais erradas. Verifique se o login / senha estão corretos."
    api = IQ_Option(email, senha)

    #Se a conexao for estabecida com sucesso, sera retornado True/None, caso nao for estabelecida com sucesso retorna False,reason.
    checar, razao = api.connect()

    # tipo_conta: "REAL" "PRACTICE"
    api.change_balance(tipo_conta)

    if checar:
        print("Conexao estabelecida com sucesso!")
        # se ver isso, você pode fechar a rede para teste.
        while True:
            if not api.check_connect():  # detectar se o websocket está fechado
                print("Tentando reconexao!")
                checar, razao = api.connect()
                if checar:
                    print("Reconexao com sucesso")
                else:
                    if razao == erro_senha:
                        print("Senha Errada")
                    else:
                        print("Nao a rede")
            break
            time.sleep(1)

    else:

        if razao == "Error -2] Nome ou serviço desconhecido":
            print("Nao a rede")
        elif razao == erro_senha:
            print("Senha Errada")

    return api

