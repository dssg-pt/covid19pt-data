import json
import pathlib
import sys
import re

import requests

DEBUG = len(sys.argv) > 1


def get_most_recent_covid_file():

    pdf_folder = pathlib.Path('dgs-reports-archive/')

    pdf_files = list(pdf_folder.glob('*.pdf'))

    pdf_files.sort(key=lambda p: p.stem, reverse=True)

    last_pdf = str(pdf_files[0])
    if DEBUG: print(f'last_pdf={last_pdf}')
    last_date = last_pdf[-14:-4].replace('_', '-')
    if DEBUG: print(f'last_date={last_date}')

    return last_date


def get_covid_data_from_api():

    url = 'https://covid19.min-saude.pt/relatorio-de-situacao/'

    response = requests.get(url=url)

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from covid site. Error %s: $s' % response.status_code, response.text)

    #if DEBUG: print(response.text)
    matches = re.search(
        (
            r'Relat.rio de Situa..o n.\s*[0-9]+\s*\|'
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
    if DEBUG: print(f"matches={matches}")
    latest_date = f"{matches.group(1)}-{matches.group(2)}-{matches.group(3)}"
    if DEBUG: print(f"latest_date={latest_date}")

    return latest_date


if __name__ == '__main__':

    current_data = get_most_recent_covid_file()

    new_data = get_covid_data_from_api()

    try:
        assert current_data == new_data
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")
