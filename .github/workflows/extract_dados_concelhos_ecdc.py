import requests
import pandas as pd
import datetime
import numpy as np
import json
from pathlib import Path
import sys
import os
from util_concelhos import (
    get_list_municipalities,
    convert,
    convert_to_float,
    convert_to_int,
)

DMY = "%d-%m-%Y"

DAYS_OFFSET = 0
today = (datetime.date.today() - datetime.timedelta(days=DAYS_OFFSET)).strftime(DMY)

# today = "11-11-2020"  # 16-11-2020 (Mon) for 28-10-2020 (Wed) to 10-11-2020 (Tue)
# today = "20-11-2020"  # 23-11-2020 (Mon) for 06-11-2020 (Fri) to 19-11-2020 (Thu)


FIX_CONCELHOS = {
    "CALHETA DE SÃO JORGE": "CALHETA (AÇORES)",
    "VILA DO CORVO": "CORVO",
    "LAGOA [R.A. AÇORES]": "LAGOA",
    "LAGOA": "LAGOA (FARO)",
}


def get_list_cases_long():
    global today

    if len(sys.argv) > 1:
        local_file = sys.argv[1]
        today = local_file.split("/")[-1]
        today = f"{today[8:10]}-{today[5:7]}-{today[0:4]}"
        with open(local_file, "r") as f:
            data = json.loads(f.read())
        recordsPerPage = 0
    else:
        recordsPerPage = 1000
        URL = (
            "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/IncidenciaCOVIDporConc100k_view/FeatureServer/0/query"
            "?f=pjson&where=1%3d1&outFields=*&returnGeometry=false&cacheHint=true"
            "&resultOffset={}&resultRecordCount={}"
        )

        resultOffset = 0
        url_cases = URL.format(resultOffset, resultOffset + recordsPerPage)
        data = requests.get(url_cases).json()

    if today == "11-11-2020":
        # CALHETA S. JORGE is Açores but the API switched them
        FIX_CONCELHOS["CALHETA DE SÃO JORGE"] = "CALHETA"
        FIX_CONCELHOS["CALHETA"] = "CALHETA (AÇORES)"

    casos = []
    while len(data["features"]) != 0:

        for entry in data["features"]:

            concelho = entry["attributes"]["Concelho"]
            concelho = FIX_CONCELHOS.get(concelho, concelho)

            incidencia = entry["attributes"]["Incidência"]  # nnn
            incidencia_categoria = entry["attributes"][
                "Incidência_categoria"
            ]  # "Acima de xxx"
            incidencia_risco = entry["attributes"]["Incidência_"]  # "Acima de xxx"

            distrito = entry["attributes"]["Distrito"]
            dicofre = entry["attributes"]["Dicofre"]
            area = entry["attributes"]["AREA_2019_"]  # AREA_20191 is 0.1

            population = entry["attributes"]["Total"]
            population_65_69 = entry["attributes"]["F65_69"]
            population_70_74 = entry["attributes"]["F70_74"]
            population_75_79 = entry["attributes"]["F75_79"]
            population_80_84 = entry["attributes"]["F80_84"]
            population_85_mais = entry["attributes"]["F85oumais"]
            population_80_mais = population_85_mais + population_80_84
            population_75_mais = entry["attributes"]["PopSup75"]
            if population_75_mais != population_80_mais + population_75_79:
                raise Exception(concelho)
            population_70_mais = entry["attributes"]["PopSup70"]
            if population_70_mais != population_75_mais + population_70_74:
                raise Exception(concelho)
            population_65_mais = entry["attributes"]["PopSup65"]
            if population_65_mais != population_70_mais + population_65_69:
                raise Exception(concelho)

            densidade_populacional = entry["attributes"]["DensidadeP"]
            # ???
            densidade_1 = entry["attributes"]["Densidad_1"]
            densidade_2 = entry["attributes"]["Densidad_2"]
            densidade_3 = entry["attributes"]["Densidad_3"]

            casos.append(
                [
                    today,
                    concelho,
                    incidencia,
                    incidencia_categoria,
                    incidencia_risco,
                    distrito,
                    dicofre,
                    area,
                    population,
                    population_65_69,
                    population_70_74,
                    population_75_79,
                    population_80_84,
                    population_85_mais,
                    population_80_mais,
                    population_75_mais,
                    population_70_mais,
                    population_65_mais,
                    densidade_populacional,
                    densidade_1,
                    densidade_2,
                    densidade_3,
                ]
            )

        if recordsPerPage:
            resultOffset += 1000
            url_cases = URL.format(resultOffset, resultOffset + recordsPerPage)
            data = requests.get(url_cases).json()
        else:
            break

    casos_df = pd.DataFrame(
        data=casos,
        columns=[
            "data",
            "concelho",
            "incidencia",
            "incidencia_categoria",
            "incidencia_risco",
            "distrito",
            "dicofre",
            "area",
            "population",
            "population_65_69",
            "population_70_74",
            "population_75_79",
            "population_80_84",
            "population_85_mais",
            "population_80_mais",
            "population_75_mais",
            "population_70_mais",
            "population_65_mais",
            "densidade_populacional",
            "densidade_1",
            "densidade_2",
            "densidade_3",
        ],
    )

    return casos_df


if __name__ == "__main__":

    PATH_TO_CSV_NEW = str(
        Path(__file__).resolve().parents[2] / "data_concelhos_new.csv"
    )

    PATH_TO_CSV_ECDC = str(
        Path(__file__).resolve().parents[2] / "data_concelhos_ecdc.csv"
    )
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "data_concelhos_14.csv")

    # Get list of municipalities
    concelhos_df = get_list_municipalities()

    # Get list of cases
    casos_df = get_list_cases_long()

    casos_df["confirmados_14"] = (
        casos_df["incidencia"] * casos_df["population"] / 100000.0
    )
    casos_df["confirmados_1"] = casos_df["confirmados_14"].div(14)

    cols = ["confirmados_14", "confirmados_1"]
    casos_df = convert(casos_df, cols, convert_to_int)
    cols = ["incidencia"]
    casos_df = convert(casos_df, cols, convert_to_float)
    cols = [x for x in casos_df.columns if x.startswith("densidade")]
    casos_df = convert(casos_df, cols, convert_to_float)
    cols = [x for x in casos_df.columns if x.startswith("population")]
    casos_df = convert(casos_df, cols, convert_to_int)

    cols = list(casos_df.columns)
    for i in ["data", "confirmados_14", "confirmados_1"]:
        cols.remove(i)
    cols.insert(cols.index("concelho") + 1, "confirmados_14")
    cols.insert(cols.index("concelho") + 2, "confirmados_1")
    cols.insert(0, "data")
    casos_df = casos_df[cols]

    # ---

    ecdc_df = concelhos_df.copy().merge(casos_df, how="left", on="concelho")
    cols = list(ecdc_df.columns)
    cols.remove("data")
    cols.insert(0, "data")
    ecdc_df = ecdc_df[cols]

    if os.path.exists(PATH_TO_CSV_NEW):
        ecdc_df.to_csv(PATH_TO_CSV_NEW, mode="a", header=False, index=False, sep=",")
    else:
        ecdc_df.to_csv(PATH_TO_CSV_NEW, index=False, sep=",")

    # ---

    for key in ["incidencia", "confirmados_14"]:

        # Helper for pivot table
        casos_df.loc[casos_df.data.isna(), [key]] = -1
        casos_df.loc[casos_df.data.isna(), ["data"]] = today

        casos_df = casos_df.sort_values(by=["concelho"])

        # Convert long table to wide table
        casos_wide = pd.pivot_table(
            casos_df, values=key, index="data", columns="concelho"
        ).reset_index()

        casos_wide.data = pd.to_datetime(casos_wide.data, format="%d-%m-%Y")
        casos_wide = casos_wide.sort_values(by="data").reset_index(drop=True)
        casos_wide = casos_wide.replace(-1, np.nan)

        # casos_wide = patch_concelhos1(casos_wide)
        casos_wide.data = casos_wide["data"].dt.strftime("%d-%m-%Y")
        # casos_wide = patch_concelhos2(casos_wide)

        if key == "incidencia":
            file = PATH_TO_CSV_ECDC
            func = convert_to_float
        else:
            file = PATH_TO_CSV
            func = convert_to_int

        cols = [x for x in casos_wide.columns if not x.startswith("data")]
        casos_wide = convert(casos_wide, cols, func)

        casos_wide.to_csv(file, mode="a", header=False, index=False, sep=",")
