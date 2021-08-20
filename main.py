from iqoptionapi.stable_api import IQ_Option
import json, time
from datetime import datetime
from dateutil import tz

# variaveis de entrada dos dados de login
email_iqoption = input("Digite seu Email: ")
senha_iqotption = input("Digite sua Senha: ")

erro_senha = "Você inseriu as credenciais erradas. Verifique se o login / senha estão corretos."
API = IQ_Option(email_iqoption, senha_iqotption)


checar, razao = API.connect()
API.change_balance("PRACTICE") #MODE: "PRACTICE" "REAL"

if checar:
    print("Iniciar seu robo")
    # se ver isso, você pode fechar a rede para teste.
    while True:
        if API.check_connect() == False:  # detectar se o websocket está fechado
            print("Tentar reconectar")
            checar, razao = API.connect()
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


def perfil():
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))

    '''
    		name
    		first_name
    		last_name
    		email
    		city
    		nickname
    		currency
    		currency_char 
    		address
    		created
    		postal_index
    		gender
    		birthdate
    		balance		
    	'''

    return perfil


def timestamp_converter(x):
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

def banca():
	return API.get_balance()

def payout(par, tipo, timeframe=1):
    if tipo == 'turbo':
        a = API.get_all_profit()
        return int(100 * a[par]['turbo'])

    elif tipo == 'digital':

        API.subscribe_strike_list(par, timeframe)
        while True:
            d = API.get_digital_current_profit(par, timeframe)
            if d != False:
                d = int(d)
                break
            time.sleep(1)
        API.unsubscribe_strike_list(par, timeframe)
        return d

"""
par = 'EURUSD'
entrada = 2
direcao = 'call'
timeframe = 1


# Entradas na digital
_, id = API.buy_digital_spot(par, entrada, direcao, timeframe)

if isinstance(id, int):
    while True:
        status, lucro = API.check_win_digital_v2(id)

        if status:
            if lucro > 0:
                print('RESULTADO: WIN / LUCRO: ' + str(round(lucro, 2)))
            else:
                print('RESULTADO: LOSS / LUCRO: -' + str(entrada))
            break

# Entradas na binaria
status, id = API.buy(entrada, par, direcao, timeframe)

if status:
    resultado, lucro = API.check_win_v3(id)

    print('RESULTADO: ' + resultado + ' / LUCRO: ' + str(round(lucro, 2)))
"""



status, historico = API.get_position_history_v2("digital-option",10,0,0,0)

"""
:::::::::::::::: [ MODO DIGITAL ] ::::::::::::::::
FINAL OPERACAO : historico['positions']['close_time']
INICIO OPERACAO: historico['positions']['open_time']
LUCRO          : historico['positions']['close_profit']
ENTRADA        : historico['positions']['invest']
PARIDADE       : historico['positions']['raw_event']['instrument_underlying']
DIRECAO        : historico['positions']['raw_event']['instrument_dir']
VALOR          : historico['positions']['raw_event']['buy_amount']

:::::::::::::::: [ MODO BINARIO ] ::::::::::::::::
MODO TURBO tem as chaves do dict diferentes para a direção da operação(put ou call) 
	e para exibir a paridade, deve ser utilizado:
DIRECAO : historico['positions']['raw_event']['direction']
PARIDADE: historico['positions']['raw_event']['active']
'''



#trecho de codigo retorno todos dados das ordens que foram abertas, seja elas com o LOSS ou WIN
for x in historico['positions']:
    print(json.dumps(x,indent=1))
"""

#trecho de codigo retorna dados formatados das ordem abertas, seja elas com o LOSS ou WIN
for x in historico['positions']:
	print('PAR: '+str(x['raw_event']['instrument_underlying'])+' /  DIRECAO: '+str(x['raw_event']['instrument_dir'])+' / VALOR: '+str(x['invest']))
	print('LUCRO: '+str(x['close_profit'] if x['close_profit'] == 0 else round(x['close_profit']-x['invest'], 2) ) + ' | INICIO OP: '+str(timestamp_converter(x['open_time'] / 1000))+' / FIM OP: '+str(timestamp_converter(x['close_time'] / 1000)))
	print('\n')
"""



#retorno payout das paridades abertas no momento
par = API.get_all_open_time()

for paridade in par['turbo']:
    if par['turbo'][paridade]['open'] == True:
        print('[ TURBO ]: ' + paridade + ' | Payout: ' + str(payout(paridade, 'turbo')))

for paridade in par['digital']:
    if par['digital'][paridade]['open'] == True:
        print('[ DIGITAL ]: ' + paridade + ' | Payout: ' + str(payout(paridade, 'digital')))

# Pegar até 1000 velas #########################
par = 'EURUSD'

vela = API.get_candles(par, 60, 10, time.time())

for velas in vela:
    print('Hora inicio: ' + str(timestamp_converter(velas['from'])) + ' abertura: ' + str(velas['open']))

## Pegar mais de 1000 velas #########################
par = 'EURUSD'

total = []
tempo = time.time()

for i in range(2):
    X = API.get_candles(par, 60, 1000, tempo)
    total = X + total
    tempo = int(X[0]['from']) - 1

for velas in total:
    print(timestamp_converter(velas['from']))

# Pegar velas em tempo real #########################
par = 'EURUSD'

API.start_candles_stream(par, 60, 1)
time.sleep(1)

# Para pegar de apenas uma paridade #################
par = 'USDCHF-OTC'

API.start_mood_stream(par)

while True:
	x = API.get_traders_mood(par)
	print(int(100 * round(x, 2)))
	
	time.sleep(1)
	
API.stop_mood_stream(par)


# Para pegar de multiplas paridades #################
id = dict([(l, u) for u,l in API.get_all_ACTIVES_OPCODE().items()])

API.start_mood_stream('USDCHF-OTC')
API.start_mood_stream('GBPUSD-OTC')

while True:
	x = API.get_all_traders_mood()
	
	for i in x:
		print(id[i]+': '+str(int(100 * round(x[i], 2))), end=' ')
		
	time.sleep(1)
	
API.stop_mood_stream('USDCHF-OTC')
API.stop_mood_stream('GBPUSD-OTC')

"""