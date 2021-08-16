import pathlib
import sys
import os
import datetime
import requests


def get_most_recent_date():
    data_file = pathlib.Path('data.csv')
    with open(data_file, "r") as file:
        lines = file.readlines()
        last_line = lines[-1]
        # if there's these many commas, it's manual data (no confirmados nor obitos per age)
        if ',,,,,,,,,,,,,,,,,,,,,,,,,,,,' in last_line:
            last_line = lines[-2]

    last_date = last_line.split(',')[0]
    return last_date


def get_data_data_from_api():

    URL = (
        'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID_ARS_PT_HISTORICO_view/FeatureServer/0/query'
        "?f=json&outFields=*&cacheHint=false"
        '&where=1%3d1'
        '&orderByFields=Data_ARS+desc'
        '&resultRecordCount=10000'
    )
    response = requests.get(URL)

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from data endpoint. Error %s: $s' % response.status_code, response.text)

    data =  response.json()

    latest_date = data['features'][0]['attributes']['Data_ARS']
    latest_date = datetime.datetime.utcfromtimestamp(latest_date / 1000)
    latest_date = latest_date.strftime("%d-%m-%Y")
    return latest_date


if __name__ == '__main__':
    last_date = get_most_recent_date()
    latest_date = get_data_data_from_api()

    try:
        assert last_date == latest_date
    except AssertionError:
        # quick hack to remote latest date with manual data if any
        os.system(f'cat data.csv | grep -v -E "^{latest_date}," > data2.csv')
        os.system(f'mv data2.csv data.csv')

        print("TRUE")
        sys.exit()

    print("FALSE")
