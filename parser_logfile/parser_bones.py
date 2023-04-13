import re


def create_row_dict(text):
    """ Создаёт словарь, содержащий значение колонок. """
    row_dict = {}

    def get_value(pattern, math_sub=None, special_sub=None):
        obj = re.search(pattern, text).group()
        if math_sub:
            obj = obj.split(math_sub)[1]  # Берём число
            obj = re.sub('.', ',', obj)
        if special_sub:
            obj = re.sub(*special_sub, obj)  # Замена нежелательных символов

        return obj

    row_dict['time'] = get_value(r'\d{2}:\d{2}:\d{2}')
    row_dict['coin'] = get_value(r'-[A-Z]*\s', special_sub=['-', ''])
    row_dict['stratname'] = get_value(r'\s<.*?>')
    row_dict['price'] = get_value(r'Ask:.*?\s', math_sub=':')
    row_dict['dbtc'] = get_value(r'dBTC:\s.*?\s', math_sub=':')
    row_dict['dbtc5m'] = get_value(r'dBTC5m:\s.*?\s', math_sub=':')
    row_dict['dbtc1m'] = get_value(r'dBTC1m:\s.*?\s', math_sub=':')
    row_dict['24btc1m'] = get_value(r'24hBTC:\s.*?\s', math_sub=':')
    row_dict['72btc1m'] = get_value(r'72hBTC:\s.*?\s', math_sub=':')
    row_dict['dmarkets'] = get_value(r'dMarkets:\s.*?\s', math_sub=':')
    row_dict['72btc1m24'] = get_value(r'dMarkets24:\s.*?\s', math_sub=':')
    row_dict['depth'] = get_value(r'\bDepth:\s.*?%\s', math_sub=':')
    row_dict['rollback'] = get_value(r'\bR:\s.*?%\s', math_sub=':')
    row_dict['delta'] = get_value(r'\bd:\s.*?%\s', math_sub=':')
    row_dict['24vol'] = get_value(r'\b24vol=\d*', math_sub='=')
    row_dict['hvol'] = get_value(r'\bhvol=\d*', math_sub='=')
    row_dict['h3vol'] = get_value(r'\bh3vol=\d*', math_sub='=')
    row_dict['delta24h'] = get_value(r'\bDelta24h=[\d|[.]]*', math_sub='=')
    row_dict['delta3h'] = get_value(r'\bDelta3h=[\d|[.]]*', math_sub='=')
    row_dict['delta24'] = get_value(r'\bd1h:\s[\d|[.]]*', math_sub=':')

    return row_dict


def create_table_mass(filepath):
    """ Cоздаёт список словарей для записи в таблицу """
    with open(filepath, 'r') as f:
        file = f.read()
        pattern = r'\b\d{2}:\d{2}:\d{2}\s*Signal.*\s\d{2}:\d{2}:\d{2}.*\s\d{2}:\d{2}:\d{2}.*'
        table_mass = re.findall(pattern, file)
        for i in range(0, len(table_mass)):
            table_mass[i] = create_row_dict(table_mass[i])
    return table_mass
