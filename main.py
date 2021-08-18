from iqoptionapi.stable_api import IQ_Option

#variaveis de entrada dos dados de login
email_iqoption = input("Digite seu Email: ")
senha_iqotption = input("Digite sua Senha: ")

erro_senha="Você inseriu as credenciais erradas. Verifique se o login / senha estão corretos."
API = IQ_Option(email_iqoption, senha_iqotption)

checar, razao = API.connect()
tezte = API.check_connect()

print(checar)
print(tezte)

if checar:
    print("Iniciar seu robo")
    #se ver isso, você pode fechar a rede para teste.
    while True:
        if API.check_connect() == False: #detectar se o websocket está fechado
            print("Tentar reconectar")
            checar, razao = API.connect()
            if checar:
                print("Reconexao com sucesso")
            else:
                if razao == erro_senha :
                    print("Senha Errada")
                else:
                    print("Nao a rede")

else:

    if razao== "Error -2] Nome ou serviço desconhecido":
        print("Nao a rede")
    elif razao==erro_senha:
        print("Senha Errada")




print(A.reset_practice_balance())