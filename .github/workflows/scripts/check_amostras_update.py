import json
import pathlib
import sys
import datetime
import requests


def get_most_recent_date():
    data_file = pathlib.Path('amostras.csv')
    with open(data_file, "r") as file:
        last_line = file.readlines()[-1]
    #print(f'last_line=\'{last_line}\'')
    last_date = last_line.split(',')[0]
    #print(f'last_date=\'{last_date}\'')
    #last_date = datetime.datetime.strptime(last_date, "%d-%m-%Y")
    #print(f'last_date=\'{last_date}\'')
    return last_date


def get_data_data_from_api():

    URL = (
        "https://services5.arcgis.com/eoFbezv6KiXqcnKq/arcgis/rest/services/Covid19_Amostras/FeatureServer/0/query"
        #"https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/Covid19_Amostras_Temporario/FeatureServer/0/query"
        "?where=Total_Amostras__Ac+%3E+0"
        "&orderByFields=Data_do_Relatorio+desc"
        "&f=pjson&outFields=*&cacheHint=false"
    )
    # print(f"Loading from '{URL}'")
    response = requests.get(URL)

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from data endpoint. Error %s: $s' % response.status_code, response.text)

    data =  response.json()

    latest_date = data['features'][0]['attributes']['Data_do_Relatorio']
    if latest_date == 1672444800000:
        latest_date = 1640822400000 + 86400000 # 2021-12-31
    #print(f'latest_date=\'{latest_date}\'')
    latest_date = datetime.datetime.utcfromtimestamp(latest_date / 1000)
    #print(f'latest_date=\'{latest_date}\'')
    latest_date = latest_date.strftime("%d-%m-%Y")
    #print(f'latest_date=\'{latest_date}\'')
    return latest_date


if __name__ == '__main__':

    last_date = get_most_recent_date()

    latest_date = get_data_data_from_api()
    #print(f"last_date={last_date} latest_date={latest_date}")

    try:
        assert last_date == latest_date
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")
