from datetime import datetime
from dateutil import tz
import pandas as pd
from finta import TA
import json
import time
import sys


def perfil(api):
    perfil_new = json.loads(json.dumps(api.get_profile_ansyc()))
    return perfil_new


def timestamp_converter(x):
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))
    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]


def banca(api):
    return api.get_balance()


def verifica_tendencia(api, par, timeframe):
    velas = api.get_candles(par, (int(timeframe) * 60), 20, time.time())

    ultimo = round(velas[0]['close'], 4)
    primeiro = round(velas[-1]['close'], 4)

    diferenca = abs(round(((ultimo - primeiro) / primeiro) * 100, 3))
    tendencia = "CALL" if ultimo < primeiro and diferenca > 0.01 \
                        else "PUT" if ultimo > primeiro and diferenca > 0.01 \
                        else False

    print(tendencia)


def martingale(valor, payout):
    lucro_esperado = valor * payout
    perca = float(valor)

    while True:
        if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
            return round(valor, 2)
            break
        valor += 0.01


def stop(lucro, gain, loss):
    if lucro <= float('-' + str(abs(loss))):
        print('Stop Loss batido!')
        sys.exit()

    if lucro >= float(abs(gain)):
        print('Stop Gain Batido!')
        sys.exit()


def payout_only_par(api, par):
    api.subscribe_strike_list(par, 1)
    while True:
        d = api.get_digital_current_profit(par, 1)
        if d != False:
            d = round(int(d) / 100, 2)
            break
        time.sleep(1)
    api.unsubscribe_strike_list(par, 1)

    return d


def payout_all_par(api, par, tipo, timeframe=1):
    if tipo == 'turbo':
        a = api.get_all_profit()
        return int(100 * a[par]['turbo'])

    elif tipo == 'digital':
        api.subscribe_strike_list(par, timeframe)

        while True:
            d = api.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
            time.sleep(1)
        api.unsubscribe_strike_list(par, timeframe)
        return d


def get_data(api, par, timeframe, periods=200):
    velas = api.get_candles(par, timeframe * 60, periods, time.time())
    df = pd.DataFrame(velas)
    df.rename(columns={'max': 'high', 'min': 'low'}, inplace=True)
    return df


def get_data_padroes(api, par, timeframe, periods=200):
    velas = api.get_candles(par, timeframe * 60, periods, time.time())
    df = pd.DataFrame(velas, columns=['open', 'min', 'max', 'close'])

    df.rename(columns={'max': 'high', 'min': 'low'}, inplace=True)
    return df


def mov_avar_dev(df, periods=20):
    src = TA.SSMA(df, periods)
    calc = df.iloc[-1]["close"] - src.iloc[-1]

    return calc, "green" if calc >= (df.iloc[-2]["close"]-src.iloc[-2]) else "red"


def entrada(api, par, direcao, timeframe):

    print("\n Abrindo operaçao")
    status, id = api.buy_digital_spot(par, direcao, timeframe)

    if status:
        status = False
        while status == False:
            status, lucro = api.check_win_digital_v2(id)
        if lucro > 0:
            print("WIN, Lucro de ", lucro)
        else:
            print("LOSS, Perca de ", lucro)
    else:
        print("Erro ao abrir a operaçao")


def doji_scan(Data):

    for i in range(len(Data)):

        if Data.iloc[i - 1]["open"] < Data.iloc[i - 1]["close"] and Data.iloc[i]["open"] == Data.iloc[i]["close"]:
            print("Vela ",  i, " DOJI DE COMPRA", "\n")
            print("Open: ", Data.iloc[i - 1]["open"], "\n", "Close: ", Data.iloc[i - 1]["close"]
                  )

        if Data.iloc[i - 1]["open"] > Data.iloc[i - 1]["close"] and Data.iloc[i]["open"] == Data.iloc[i]["close"]:
            print("Vela ", i, " DOJI DE VENDA", "\n")
            print("Open: ", Data.iloc[i - 1]["open"], "\n", "Close: ", Data.iloc[i - 1]["close"]
                  )
