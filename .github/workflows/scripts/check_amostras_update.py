import json
import pathlib
import sys
import datetime
import requests

DEBUG = len(sys.argv) > 1


def get_most_recent_date():
    data_file = pathlib.Path('amostras.csv')
    with open(data_file, "r") as file:
        csv_line = file.readlines()[-1]
    if DEBUG:
        print(f'csv_line=\'{csv_line}\'')
    csv_date = csv_line.split(',')[0]
    if DEBUG:
        nice_date = datetime.datetime.strptime(csv_date, "%d-%m-%Y")
        print(f'csv_date=\'{csv_date}\' {nice_date}')
    return csv_date


def get_data_data_from_api():

    URL = (
        "https://services5.arcgis.com/eoFbezv6KiXqcnKq/arcgis/rest/services/Covid19_Amostras/FeatureServer/0/query"
        #"https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/Covid19_Amostras_Temporario/FeatureServer/0/query"
        "?where=Total_Amostras__Ac+%3E+0"
        "&orderByFields=Data_do_Relatorio+desc"
        "&f=pjson&outFields=*&cacheHint=false"
    )
    if DEBUG: print(f"Loading from '{URL}'")
    response = requests.get(
        url=URL,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        },
    )

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from data endpoint. Error %s: $s' % response.status_code, response.text)

    data =  response.json()

    latest_date = data['features'][0]['attributes']['Data_do_Relatorio']
    #if latest_date == 1672444800000:
    #    latest_date = 1640822400000 + 86400000 # 2021-12-31 reportado como 2022-12-31
    #elif latest_date == 1643760000000:
    #    latest_date = 1640995200000 + 86400000 # 2022-01-02 reportado como 2022-02-02
    if DEBUG: print(f'latest_date=\'{latest_date}\'')
    latest_date = datetime.datetime.utcfromtimestamp(latest_date / 1000)
    if DEBUG: print(f'latest_date=\'{latest_date}\'')
    latest_date = latest_date.strftime("%d-%m-%Y")
    if DEBUG: print(f'latest_date=\'{latest_date}\'')
    return latest_date


if __name__ == '__main__':

    last_date = get_most_recent_date()

    latest_date = get_data_data_from_api()
    if DEBUG: print(f"last_date={last_date} latest_date={latest_date}")

    try:
        assert last_date == latest_date
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")
