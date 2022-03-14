import json
import pathlib
import sys

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

    response = requests.get(
        url=url,
        params=params,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        },
    )

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from vaccine endpoint. Error %s: $s' % response.status_code, response.text)

    return response.json()


if __name__ == '__main__':

    current_data = get_most_recent_vaccine_file()

    new_data = get_vaccine_data_from_api()

    try:
        assert current_data == new_data
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")
