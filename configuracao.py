import configparser


def configuracao():
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')

    return {'paridade': arquivo.get('MHI', 'paridade'), 'valor_entrada': arquivo.get('MHI', 'entrada'),
            'timeframe': arquivo.get('MHI', 'timeframe')}


# printa as informaçoes contida no arquivo config.txt
# print(configuracao())

def configuracao_v2(bloco):
    arquivo = configparser.RawConfigParser()
    arquivo.read('config.txt')
    #print("Paridades no arquivo config.txt ->", arquivo.sections())

    return {'paridade': arquivo.get(bloco, 'paridade'), 'valor_entrada': arquivo.get(bloco, 'valor_entrada'),
            'timeframe': arquivo.get(bloco, 'timeframe')}


def insert_data_block(paridade, valor, timeframe):
    config = configparser.ConfigParser()
    config.read("config.txt")
    print(config.sections())

    config.add_section(paridade)
    config.set(paridade, 'paridade', paridade)
    config.set(paridade, 'valor_entrada', str(valor))
    config.set(paridade, 'timeframe', str(timeframe))

    with open('config.txt', 'w') as configfile:
        config.write(configfile)

    configfile.close()
    return True

def valida_insert_data_block(paridade):
    config = configparser.ConfigParser()
    config.read("config.txt")
    for section in config.sections():
        if section == paridade:
            return True
            break

    return False
