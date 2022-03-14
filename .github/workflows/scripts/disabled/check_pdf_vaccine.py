import json
import pathlib
import sys
import re
import datetime

import requests

DEBUG = len(sys.argv) > 1


def get_last_date(lines, exclude_manual=False):
    last_line = lines[-1]
    # if there's these many commas, it's manual data (no confirmados nor obitos per age)
    if not exclude_manual and ',,,,,,,,,,,,,,,,,,,,,,,,,,,,' in last_line:
        return get_last_date(lines[:-1], exclude_manual=exclude_manual)
    return last_line


def get_most_recent_date(exclude_manual=False):
    data_file = pathlib.Path('vacinas_detalhe.csv')
    with open(data_file, "r") as file:
        lines = file.readlines()
        last_line = get_last_date(lines, exclude_manual)

    last_date = last_line.split(',')[0]
    # return last_date
    res = datetime.datetime.strptime(last_date, "%d-%m-%Y")
    return res


def get_vaccine_data_from_api():

    url = 'https://covid19.min-saude.pt/relatorio-de-vacinacao/'

    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        },
    )

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from vaccine endpoint. Error %s: $s' % response.status_code, response.text)

    #if DEBUG: print(response.text)
    matches = re.search(
        (
            r'Relat.rio de Vacina..o\s*[^<]*\s*a\s*'
            r'\s*([0-3][0-9])'
            r'\s*(?:<[^>]+?>)?'
            r'\s*/'
            r'\s*(?:<[^>]+?>)?'
            r'\s*([0-1][0-9])'
            r'\s*/'
            r'\s*(?:<[^>]+?>)?'
            r'\s*(202[0-9])'
            r'\s*[^<]*?</a>'
    ), response.text, re.MULTILINE | re.IGNORECASE)
    #if DEBUG: print(f"matches={matches}")
    latest_date = f"{matches.group(1)}-{matches.group(2)}-{matches.group(3)}"
    # return latest_date
    res = datetime.datetime.strptime(latest_date, "%d-%m-%Y")
    return res



if __name__ == '__main__':

    current_data = get_most_recent_date()
    if DEBUG: print(f"current_data={current_data}")
    current_data = current_data - datetime.timedelta(days=1)

    new_data = get_vaccine_data_from_api()
    if DEBUG: print(f"new_data={new_data}")

    foo = new_data - current_data
    if DEBUG: print(f"foo={foo}")

    foo = new_data == current_data
    if DEBUG: print(f"foo={foo}")

    try:
        assert current_data == new_data
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")
