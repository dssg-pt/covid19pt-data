import requests
import pandas as pd


def get_list_municipalities():
    """ Retrieve list of municipalities. """
    recordsPerPage = 200
    URL = (
        "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_Concelhos_V/FeatureServer/0/query"
        "?f=json&outFields=*&cacheHint=false"
        "&where=1%3D1"
        "&returnGeometry=false&spatialRel=esriSpatialRelIntersects"
        "&resultOffset={}&resultRecordCount={}"
    )

    resultOffset = 0
    url_concelhos = URL.format(resultOffset, resultOffset + recordsPerPage)
    data = requests.get(
        url=url_concelhos,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        },
    ).json()

    concelhos = []
    while len(data["features"]) != 0:
        for entry in data["features"]:
            concelho = entry["attributes"]["Concelho"]
            concelhos.append(concelho)

        resultOffset += 200
        url_concelhos = URL.format(resultOffset, resultOffset + recordsPerPage)
        data = requests.get(
            url=url_concelhos,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
            },
        ).json()

    concelhos_df = pd.DataFrame(data=concelhos, columns=["concelho"])

    return concelhos_df
