import requests
import pandas as pd
import numpy as np


def convert(df, cols, func):
    """ Apply func to columnss of dataframe. """
    df[cols] = df[cols].applymap(func)
    return df


def convert_to_int(x):
    """ Convert NaN to empty string, numbers to integers, or fallback to self. """
    if np.isnan(x):
        return ""
    try:
        return int(round(x))
    except:
        return x


def convert_to_float(x):
    """ Convert NaN to empty string, numbers to 2 digits. """
    if np.isnan(x):
        return ""
    else:
        return round(float(x), 2)


def get_list_municipalities():
    """ Retrieve list of municipalities. """
    recordsPerPage = 200
    URL = (
        "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_Concelhos_V/FeatureServer/0/query"
        "?f=json&outFields=*&cacheHint=true"
        "&where=1%3D1"
        "&returnGeometry=false&spatialRel=esriSpatialRelIntersects"
        "&resultOffset={}&resultRecordCount={}"
    )

    resultOffset = 0
    url_concelhos = URL.format(resultOffset, resultOffset + recordsPerPage)
    data = requests.get(url_concelhos).json()

    concelhos = []
    while len(data["features"]) != 0:
        for entry in data["features"]:
            concelho = entry["attributes"]["Concelho"]
            concelhos.append(concelho)

        resultOffset += 200
        url_concelhos = URL.format(resultOffset, resultOffset + recordsPerPage)
        data = requests.get(url_concelhos).json()

    concelhos_df = pd.DataFrame(data=concelhos, columns=["concelho"])

    return concelhos_df
