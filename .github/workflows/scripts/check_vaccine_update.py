import json
import pathlib
import subprocess
import sys
import os

import requests


def get_most_recent_vaccine_file():

    vaccine_folder = pathlib.Path('extra/vacinas/diário/')

    vaccine_files = list(vaccine_folder.glob('*.json'))

    vaccine_files.sort(key=lambda p: p.stem, reverse=True)

    with vaccine_files[0].open('r') as f:
        data = json.load(f)

    return data


def get_vaccine_data_from_api():

    url = 'https://services5.arcgis.com/eoFbezv6KiXqcnKq/arcgis/rest/services/Covid19_Total_Vacinados/FeatureServer/0/query'
    params = (
        ('f', 'pjson'),
        ('where', '1=1'),
        ('returnGeometry', 'false'),
        ('spatialRel', 'esriSpatialRelIntersects'),
        ('outFields', '*'),
        ('resultOffset', '0'),
        ('resultRecordCount', '50'),
        ('resultType', 'standard'),
        ('cacheHint', 'false'),
    )

    response = requests.get(url=url, params=params)

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from vaccine endpoint. Error %s: $s' % response.status_code, response.text)

    return response.json()


if __name__ == '__main__':

    current_data = get_most_recent_vaccine_file()

    new_data = get_vaccine_data_from_api()

    try:
        assert current_data != new_data
    except AssertionError:
        print('No new vaccine data found!')
        sys.exit()

    os.environ['TWITTER_CONSUMER_KEY_VAC'] = "DEBUG"

    subprocess.call(args=["python3", ".github/workflows/tweet_vacinas.py"])
