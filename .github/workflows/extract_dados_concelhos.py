import requests
import pandas as pd
import datetime
import numpy as np
from pathlib import Path
from util_concelhos import get_list_municipalities
from util import convert, convert_to_int


SKIP_DATES = [
    # On Sunday 05-07-2020 data was frozen:
    # > ESTE RELATÓRIO DE SITUAÇÃO NÃO INCLUI A ATUALIZAÇÃO DA IMPUTAÇÃO DE CASOS
    # > AOS CONCELHOS. A DGS ESTÁ A REALIZAR A VERIFICAÇÃO DE TODOS OS DADOS COM
    # > AS AUTORIDADES LOCAIS E REGIONAIS DE SAÚDE QUE FICARÁ CONCLUÍDA DURANTE OS
    # > PRÓXIMOS DIAS.
    # Data unfroze on Tuesday 14-07-2020, and then it's updated only on Mondays.
    # This list keeps Monday 06-07 and 13-07 for consistency, and ignore the
    # duplicated data until Sunday 16-08.
    "07-07-2020",
    "08-07-2020",
    "09-07-2020",
    "10-07-2020",
    "11-07-2020",
    "12-07-2020",
    #
    # 14 was the day of the update
    "15-07-2020",
    "16-07-2020",
    "17-07-2020",
    "18-07-2020",
    "19-07-2020",
    #
    "21-07-2020",
    "22-07-2020",
    "23-07-2020",
    "24-07-2020",
    "25-07-2020",
    "26-07-2020",
    #
    "28-07-2020",
    "29-07-2020",
    "30-07-2020",
    "31-07-2020",
    "01-08-2020",
    "02-08-2020",
    #
    "04-08-2020",
    "05-08-2020",
    "06-08-2020",
    "07-08-2020",
    "08-08-2020",
    "09-08-2020",
    #
    "11-08-2020",
    "12-08-2020",
    "13-08-2020",
    "14-08-2020",
    "15-08-2020",
    "16-08-2020",
]


def get_list_cases_long():
    recordsPerPage = 1000
    URL = (
        "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_ConcelhosDiarios/FeatureServer/0/query"
        "?f=json&outFields=*&cacheHint=false"
        "&where=1%3D1&orderByFields=Data+desc"
        "&returnGeometry=false&spatialRel=esriSpatialRelIntersects"
        "&resultOffset={}&resultRecordCount={}"
    )

    resultOffset = 0
    url_cases = URL.format(resultOffset, resultOffset + recordsPerPage)
    data = requests.get(
        url=url_cases,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
        },
    ).json()

    casos = []
    while len(data["features"]) != 0:

        for entry in data["features"]:
            unix_date = entry["attributes"]["Data"] / 1000
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date).strftime(
                "%d-%m-%Y"
            )
            if frmt_date in SKIP_DATES:
                continue
            confirmados_acumulado = entry["attributes"]["ConfirmadosAcumulado"]
            confirmados_concelho = entry["attributes"]["Concelho"]
            casos.append([frmt_date, confirmados_concelho, confirmados_acumulado])

        resultOffset += 1000
        url_cases = URL.format(resultOffset, resultOffset + recordsPerPage)
        data = requests.get(
            url=url_cases,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
            },
        ).json()

    casos_df = pd.DataFrame(data=casos, columns=["data", "concelho", "confirmados"])

    return casos_df


def patch_concelhos1(concelhos):

    # Is LAGOA FARO, as LAGOA AÇORES only has cases since 2020-10-05
    for k, v in concelhos.loc[
        concelhos["data"] < "2020-10-05", "LAGOA (FARO)"
    ].iteritems():
        if np.isnan(v):
            concelhos.loc[[k], "LAGOA (FARO)"] = concelhos.loc[[k], "LAGOA"]
            concelhos.loc[[k], "LAGOA"] = np.nan

    # Is CALHETA AÇORES, as CALHETA MADEIRA only has cases since 2020-07-20
    for k, v in concelhos.loc[
        concelhos["data"] < "2020-07-20", "CALHETA (AÇORES)"
    ].iteritems():
        if np.isnan(v):
            concelhos.loc[[k], "CALHETA (AÇORES)"] = concelhos.loc[[k], "CALHETA"]
            concelhos.loc[[k], "CALHETA"] = np.nan

    return concelhos


def patch_concelhos2(concelhos):

    idx = concelhos.data == "16-05-2020"
    concelhos.loc[idx, "SANTO TIRSO"] = 378
    concelhos.loc[idx, "SÃO BRÁS DE ALPORTEL"] = 3

    # is 157 on 09 and 11
    idx = concelhos.data == "10-08-2020"
    concelhos.loc[idx, "REGUENGOS DE MONSARAZ"] = 157

    # Missing
    idx = concelhos.data == "31-08-2020"
    concelhos.loc[idx, "LOUSADA"] = 378
    concelhos.loc[idx, "LOUSÃ"] = 26

    # Missing accent
    idx = concelhos.data == "05-10-2020"
    concelhos.loc[idx, "MÊDA"] = 8
    idx = concelhos.data == "26-10-2020"
    concelhos.loc[idx, "MÊDA"] = 9

    return concelhos


if __name__ == "__main__":

    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "data_concelhos.csv")

    # Get list of municipalities
    concelhos_df = get_list_municipalities()

    # Get list of cases
    casos_df = get_list_cases_long()

    # Merge list of cases with list of municipalities
    casos_df = concelhos_df.merge(casos_df, how="left", on="concelho")

    # Helper for pivot table
    casos_df.loc[casos_df.data.isna(), ["confirmados"]] = -1
    casos_df.loc[casos_df.data.isna(), ["data"]] = "24-03-2020"

    casos_df = casos_df.sort_values(by=["concelho"])

    # Convert long table to wide table
    casos_wide = pd.pivot_table(
        casos_df, values="confirmados", index="data", columns="concelho"
    )
    casos_wide = casos_wide.reset_index()

    casos_wide.data = pd.to_datetime(casos_wide.data, format="%d-%m-%Y")
    casos_wide = casos_wide.sort_values(by="data").reset_index(drop=True)
    casos_wide = casos_wide.replace(-1, np.nan)

    casos_wide = patch_concelhos1(casos_wide)
    casos_wide.data = casos_wide["data"].dt.strftime("%d-%m-%Y")
    casos_wide = patch_concelhos2(casos_wide)

    cols = [x for x in casos_wide.columns if not x.startswith("data")]
    casos_wide = convert(casos_wide, cols, convert_to_int)

    casos_wide.to_csv(PATH_TO_CSV, index=False, sep=",")
