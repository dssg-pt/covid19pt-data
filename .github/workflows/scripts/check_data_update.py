import pathlib
import sys
import os
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
    data_file = pathlib.Path('data.csv')
    with open(data_file, "r") as file:
        lines = file.readlines()
        last_line = get_last_date(lines, exclude_manual)

    last_date = last_line.split(',')[0]
    res = datetime.datetime.strptime(last_date, "%d-%m-%Y")
    #if DEBUG: print(f"CSV last_date={last_date} {res}")
    return res


def get_data_data_from_api():

    URL = (
        'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID_ARS_PT_HISTORICO_view/FeatureServer/0/query'
        "?f=json&outFields=*&cacheHint=false"
        '&where=1%3d1'
        '&orderByFields=Data_ARS+desc'
        '&resultRecordCount=10000'
    )
    response = requests.get(
        url=URL,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        },
    )

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from data endpoint. Error %s: $s' % response.status_code, response.text)

    data =  response.json()

    last_date = data['features'][0]['attributes']['Data_ARS']
    last_date = datetime.datetime.utcfromtimestamp(last_date / 1000)
    last_date = last_date.strftime("%d-%m-%Y")
    res = datetime.datetime.strptime(last_date, "%d-%m-%Y")
    #if DEBUG: print(f"API last_date={last_date} {res}")
    return res

if __name__ == '__main__':
    last_date_csv = get_most_recent_date(exclude_manual=True)
    last_date_auto = get_most_recent_date()
    last_date_api = get_data_data_from_api()
    if DEBUG: print(f"CSV={last_date_csv} auto={last_date_auto} api={last_date_api}")
    if last_date_api == last_date_auto:
        # got latest data already, nothing to do
        print("FALSE")
    elif last_date_api == last_date_csv:
        # replace latest manual data
        latest_date = last_date_api.strftime("%d-%m-%Y")
        # quick hack to remove latest date with manual data if any
        os.system(f'cat data.csv | grep -v -E "^{latest_date}," > data2.csv')
        os.system(f'mv data2.csv data.csv')

        print("TRUE")
    elif last_date_api == last_date_csv + datetime.timedelta(days=1):
        print("TRUE")
    else:
        # missing data for more than a day, don't do anything
        print("FALSE")
