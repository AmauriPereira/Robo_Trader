from configuracao import configuracao, configuracao_v2
from datetime import datetime
import time
from funcoes import martingale, stop, payout_only_par

def estratege_mhi_simple(api, bloco, operacao, qtd_martingale):
    conf = configuracao_v2(bloco)
    par = conf["paridade"]
    duracao_candle = int(conf["timeframe"])
    valor = float(conf['valor_entrada'])

    while True:

        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (4.58 <= minutos <= 5) or minutos >= 9.58 else False
        if 4.50 <= minutos < 5 or 9.50 <= minutos < 10:
            print('Hora de entrar?', entrar, '/ Minutos:', minutos)

        if entrar:
            print('\n\nIniciando operação!')
            direcao = False
            print('Verificando cores..', end='')
            velas = api.get_candles(par, 60, 3, time.time())

            velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
            velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
            velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'

            cores = velas[0] + ' ' + velas[1] + ' ' + velas[2]
            print("\ncores :", cores)

            if cores.count("g") > cores.count("r") and cores.count("d") == 0: direcao = "put"
            if cores.count("r") > cores.count("g") and cores.count("d") == 0: direcao = "call"

            if direcao:
                print("Direção:", direcao)
                status, id = api.buy_digital_spot(par, valor, direcao, duracao_candle) if operacao == 1 else api.buy(valor, par, direcao, duracao_candle)

                print("Valor_entrada: ", valor, "::", "Status: ", status,":: id: ",id, "\n")

                for i in range(qtd_martingale):
                    if status:
                        while True:

                            # status, valor = api.check_win_digital_v2(id) if operacao == 1 else api.check_win_v3(id)
                            if operacao == 1:
                                status, valor = api.check_win_digital_v2(id)
                            else:
                                status, valor = api.check_win_v3(id)

                            if status:
                                print('Resultado operação: ', end='')
                                print('WIN /' if valor > 0 else 'LOSS /', round(valor, 2))
                                break
                    else:
                        print('\nERRO AO REALIZAR OPERAÇÃO\n\n')

        time.sleep(1)

def estratege_mhi_modify_user(api, bloco, operacao, qtd_martingale):
    conf = configuracao_v2(bloco)
    par = conf["paridade"]
    duracao_candle = int(conf["timeframe"])
    valor = float(conf['valor_entrada'])
    qtd_martingale += 1
    lucro = 0
    payout = payout_only_par(api, par)

    while True:
        minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
        entrar = True if (minutos >= 4.59 and minutos <= 5) or minutos >= 9.59 else False
        #entrar = True
        cores = []
        valor_entrada=0

        if minutos >= 4.50 and minutos < 5 or minutos >= 9.50 and minutos < 10:
            print('Hora de entrar?', entrar, '/ Minutos:', minutos)

        if entrar == True:

            print('\n\nIniciando operação!')
            direcao = False

            print('Verificando cores.. ', end='')
            velas = api.get_candles(par, 60, 5, time.time())

            velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0][
                'close'] else 'd'
            velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1][
                'close'] else 'd'
            velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2][
                'close'] else 'd'
            velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3][
                'close'] else 'd'
            velas[4] = 'g' if velas[4]['open'] < velas[4]['close'] else 'r' if velas[4]['open'] > velas[4][
                'close'] else 'd'

            for x in range(len(velas)):
                cores.append(velas[x])

            print(cores)

            if cores.count("g") > cores.count("r") and cores.count("d") == 0: direcao = "put"
            if cores.count("r") > cores.count("g") and cores.count("d") == 0: direcao = "call"

            if direcao:
                print('Direção:', direcao)

                for i in range(qtd_martingale):

                    status, id = api.buy_digital_spot(par, valor, direcao, duracao_candle) if operacao == 1 else api.buy(
                        valor, par, direcao, duracao_candle)

                    if status == True:
                        while True:
                            try:
                                status, valor_entrada = api.check_win_digital_v2(id) if operacao == 1 else api.check_win_v3(id)

                            except:
                                status = True
                                valor = 0

                            if status:
                                valor = valor_entrada if valor_entrada > 0 else float('-' + str(abs(valor_entrada)))
                                lucro += round(valor, 2)

                                print('Resultado operação: ', end='')
                                print('WIN /' if valor_entrada > 0 else 'LOSS /', round(valor_entrada, 2), '/',
                                      round(lucro, 2),
                                      ('/ ' + str(i) + ' GALE' if i > 0 else ''))
                                valor_entrada = martingale(valor_entrada, payout)

                                #stop(lucro, stop_gain, stop_loss)

                                break

                        if valor > 0: break

                    else:
                        print('\nErro ao realizar a operacao\n\n')

        time.sleep(1)



