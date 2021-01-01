import datetime
import requests
import pandas as pd
import numpy as np
from pathlib import Path


DEBUG = False


def get_amostras(url):
    r = requests.get(url=url)
    data = r.json()
    amostras = []

    for entry in data["features"]:
        if "Data_do_Relatório" in entry["attributes"]:
            unix_date = entry["attributes"]["Data_do_Relatório"] / 1000
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date)
            amostras_total = entry["attributes"]["Amostras__Ac"]
            amostras_novas = entry["attributes"]["Amostras_Novas"]
            amostras.append([frmt_date, amostras_total, amostras_novas, 0, 0, 0, 0])
        elif "Data_do_Relatorio" in entry["attributes"]:
            unix_date = entry["attributes"]["Data_do_Relatorio"] / 1000
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date)
            amostras_total = entry["attributes"]["Total_Amostras__Ac"]
            amostras_novas = entry["attributes"]["Total_Amostras_Novas"]
            amostras_pcr_total = entry["attributes"]["Testes_PCR_Amostras__Ac"]
            amostras_pcr_novas = entry["attributes"]["Testes_PCR_Amostras_Novas"]
            amostras_antigenio_total = entry["attributes"][
                "Testes_Antigenio_Amostras__Ac"
            ]
            amostras_antigenio_novas = entry["attributes"][
                "Testes_Antigenio_Amostras_Novas"
            ]
            amostras.append(
                [
                    frmt_date,
                    amostras_total,
                    amostras_novas,
                    amostras_pcr_total,
                    amostras_pcr_novas,
                    amostras_antigenio_total,
                    amostras_antigenio_novas,
                ]
            )

    amostras_df = pd.DataFrame(
        data=amostras,
        columns=[
            "data",
            "amostras",
            "amostras_novas",
            "amostras_pcr",
            "amostras_pcr_novas",
            "amostras_antigenio",
            "amostras_antigenio_novas",
        ],
    )
    return amostras_df


NOVAS = ("amostras_novas", "amostras_pcr_novas")
FIXES = (
    # data, columns, fix_value
    ("16-03-2020", NOVAS, 1683),
    ("18-03-2020", NOVAS, 2465),
    ("19-03-2020", NOVAS, 2498),
    ("24-03-2020", NOVAS, 5027),
    ("25-03-2020", NOVAS, 5319),
    ("26-03-2020", NOVAS, 6694),
    ("27-03-2020", NOVAS, 7913),
    ("30-03-2020", NOVAS, 7986),
    ("31-03-2020", NOVAS, 7962),
    ("01-04-2020", NOVAS, 8650),
    ("02-04-2020", NOVAS, 9299),
    ("03-04-2020", NOVAS, 9479),
    ("04-04-2020", NOVAS, 9158),
    ("06-04-2020", NOVAS, 9369),
    ("07-04-2020", NOVAS, 10623),
    ("08-04-2020", NOVAS, 11691),
    ("10-04-2020", NOVAS, 10216),
    ("11-04-2020", NOVAS, 9121),
    ("13-04-2020", NOVAS, 8944),
    ("15-04-2020", NOVAS, 13649),
    ("16-04-2020", NOVAS, 13474),
    ("17-04-2020", NOVAS, 14720),
    ("18-04-2020", NOVAS, 12795),
    ("20-04-2020", NOVAS, 11089),
    ("21-04-2020", NOVAS, 14930),
    ("22-04-2020", NOVAS, 15531),
    ("23-04-2020", NOVAS, 15183),
    ("24-04-2020", NOVAS, 14817),
    ("27-04-2020", NOVAS, 12207),
    ("30-04-2020", NOVAS, 16438),
    ("26-12-2020", "amostras_novas", 19834),
    ("26-12-2020", "amostras_antigenio_novas", 1747),
    ("28-12-2020", "amostras_novas", 33699),
    ("28-12-2020", "amostras_antigenio_novas", 5077),
    ("29-12-2020", "amostras_novas", 44603),
    ("29-12-2020", "amostras_antigenio_novas", 4658),
    ("30-12-2020", "amostras_novas", 41199),
    ("30-12-2020", "amostras_antigenio_novas", 5902),
)


def fix_amostras(data):
    for i in ("26-02-2020", "27-02-2020", "28-02-2020", "29-02-2020"):
        data.loc[
            data.data == i,
            [
                "amostras_pcr",
                "amostras_pcr_novas",
                "amostras_antigenio",
                "amostras_antigenio_novas",
            ],
        ] = ""

    for fix in FIXES:
        if DEBUG:
            old = data.loc[data.data == fix[0], fix[1]].to_numpy()[0]
            try:
                old = old.tolist()
            except AttributeError:
                pass
            print(f"Override {fix[0]} {fix[1]} from {old} to {fix[2]}")
        data.loc[data.data == fix[0], fix[1]] = fix[2]
    return data


def convert(x):
    try:
        if np.isnan(x):
            return ""
    except:
        return ""
    try:
        return int(x)
    except:
        return x


if __name__ == "__main__":
    # Constants
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "amostras.csv")
    URL = (
        "https://services5.arcgis.com/eoFbezv6KiXqcnKq/arcgis/rest/services/Covid19_Amostras/FeatureServer/0/query"
        "?where=Total_Amostras__Ac+%3E+0"
        "&orderByFields=Data_do_Relatorio+desc"
        "&f=pjson&outFields=*&cacheHint=true"
    )
    # Get the data available in the dashboard
    available = get_amostras(URL)

    # Get latest data
    latest = pd.read_csv(PATH_TO_CSV)
    latest["data"] = pd.to_datetime(latest["data"], format="%d-%m-%Y")

    for col in [
        "amostras",
        "amostras_novas",
        "amostras_pcr",
        "amostras_pcr_novas",
        "amostras_antigenio",
        "amostras_antigenio_novas",
    ]:
        if col not in latest.columns:
            latest.loc[:, col] = np.nan

    # Find rows with differences
    merged = available.merge(
        latest, how="outer", on=["data"], suffixes=("_available", "_latest")
    )
    merged = merged.fillna('""')

    different_rows = merged[
        (merged.amostras_available != merged.amostras_latest)
        | (merged.amostras_novas_available != merged.amostras_novas_latest)
        | (merged.amostras_pcr_available != merged.amostras_pcr_latest)
        | (merged.amostras_pcr_novas_available != merged.amostras_pcr_novas_latest)
        | (merged.amostras_antigenio_available != merged.amostras_antigenio_latest)
        | (
            merged.amostras_antigenio_novas_available
            != merged.amostras_antigenio_novas_latest
        )
    ]

    # Order by date
    different_rows = different_rows.sort_values(by="data")

    # Update values
    updated = latest.copy()

    for r, row in different_rows.iterrows():

        # existing row
        if (updated.data == row["data"]).any():
            index = updated.index[updated["data"] == row["data"]]
            updated.at[index, "amostras"] = row["amostras_available"]
            updated.at[index, "amostras_novas"] = row["amostras_novas_available"]
            updated.at[index, "amostras_pcr"] = row["amostras_pcr_available"]
            updated.at[index, "amostras_pcr_novas"] = row[
                "amostras_pcr_novas_available"
            ]
            updated.at[index, "amostras_antigenio"] = row[
                "amostras_antigenio_available"
            ]
            updated.at[index, "amostras_antigenio_novas"] = row[
                "amostras_antigenio_novas_available"
            ]

        # new row
        else:
            tmp_df = pd.DataFrame(
                [
                    [
                        row["data"],
                        row["amostras_available"],
                        row["amostras_novas_available"],
                        row["amostras_pcr_available"],
                        row["amostras_pcr_novas_available"],
                        row["amostras_antigenio_available"],
                        row["amostras_antigenio_novas_available"],
                    ]
                ],
                columns=updated.columns,
            )
            updated = pd.concat([updated, tmp_df], ignore_index=True)

    # sort by date
    updated = updated.sort_values("data")
    updated["data"] = updated["data"].dt.strftime("%d-%m-%Y")
    # convert values to integer
    cols = [x for x in updated.columns if not x.startswith("data")]
    updated[cols] = updated[cols].applymap(convert)
    # fix values
    updated = fix_amostras(updated)
    # save to .csv
    updated.to_csv(PATH_TO_CSV, index=False, line_terminator="\n")
