import pathlib
import sys
import re
import datetime

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
    url = 'https://covid19.min-saude.pt'

    response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        },
    )
    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from covid site. Error %s: $s' % response.status_code, response.text)

    # <a href="https://covid19.min-saude.pt/wp-content/uploads/2022/01/700_DGS_boletim_20220131.pdf" target="_blank">Ponto de Situação (31-01-2022)</a>
    matches = re.search((
        r'wp-content/uploads/[0-9]+/[0-9]+/([0-9]+_DGS_boletim_([0-9]{8})\.pdf)'
    ), response.text, re.MULTILINE | re.IGNORECASE)
    if DEBUG: print(f"matches={matches}")
    latest_date = f"{matches.group(2)[6:8]}-{matches.group(2)[4:6]}-{matches.group(2)[0:4]}"  # DD-MM-YYYY
    if DEBUG: print(f"latest_date={latest_date}")

    return latest_date


if __name__ == '__main__':

    current_data = get_most_recent_covid_file()
    new_data = get_covid_data_from_api()

    current_data = datetime.datetime.strptime(current_data, '%d-%m-%Y')
    new_data = datetime.datetime.strptime(new_data, '%d-%m-%Y')
    if DEBUG: print(f"current_data={current_data} new_data={new_data}")

    try:
        assert new_data <= current_data
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")
