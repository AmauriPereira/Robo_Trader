"""
Robo criado para realizar trader utilizando a estrategia MHI. O codigo e de origem do canal iqcoding, e foi aperfeiçoado
por Amauri Pereira.

"""
from builtins import list

from conexao import conexao_iqoption
from configuracao import valida_insert_data_block, insert_data_block
from estrategias import estratege_mhi_simple, estratege_mhi_modify_user

print("+-------------------------+")
print("|         Contas          |")
print("+-------------------------+")
print("|     [1] - Real          |")
print("|     [2] - Demo          |")
print("+-------------------------+")

#Valida se opcao digitada eh valida.
while True:
    try:
        id_tipo_conta = int(input("Informe o tipo de conta da IqOption: "))

        if 0 < id_tipo_conta < 3:
            if id_tipo_conta == 1:
                #tipo_conta = "REAL"
                tipo_conta = "PRACTICE"
            else:
                tipo_conta = "PRACTICE"
            break
    except:
        print('\n Opçao invalida')


#Chama a funçao conexao_iqotion estabelecendo conexao com a plantaforma IQOPTION
api = conexao_iqoption(tipo_conta, "", "")
par = api.get_all_open_time()

#Escolhe em qual tipo deseja operar, binaria ou Digital
while True:
    try:

        print("+-------------------------+")
        print("|     Tipo de Opçoes      |")
        print("+-------------------------+")
        print("|     [1] - Digital       |")
        print("|     [2] - Binaria       |")
        print("+-------------------------+")
        operacao = int(input("\n Deseja operar: "))

        if 0 < operacao < 3:
            if operacao == 1:
                operar = "digital"
            else:
                operar = "turbo"

            break
    except:
        print('\n Opçao invalida')

print("+------------------------------------+")
print("|      Paridades disponiveis         |")
print("+------------------------------------+")

i = 0
for paridade in par[operar]:
    if par[operar][paridade]['open']:
        print("| ", i+1, " - " + operar + ': ' + paridade, "           |")
        i = i+1
print("+------------------------------------+")

paridade = input("Informe uma paridade: ").upper()

retorno_validacao = valida_insert_data_block(paridade)

if not retorno_validacao:
    insert_data_block(paridade, 1, 1)

#estratege_mhi_simple_modify(api, paridade, operar, 1)
#estratege_mhi_simple(api, paridade, operar, 0)
#estratege_mhi_complex(api, paridade,2, operar,1,10,10,2)

estratege_mhi_modify_user(api, paridade, operar, 0)
