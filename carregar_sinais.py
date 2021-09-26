'''
lista de sinais deve ter o formato:
DATA HORA,PARIDADE,DIRECAO
'''


def carregar_sinais():
    arquivo = open('sinais.txt', encoding='UTF-8')
    lista = arquivo.read()
    arquivo.close

    lista = lista.split('\n')

    for index, a in enumerate(lista):
        if a == '':
            del lista[index]

    return lista


print('\n\n')

lista = carregar_sinais()

for sinal in lista:
    dados = sinal.split(',')

    print(dados[0])
    print(dados[1])
    print(dados[2])
