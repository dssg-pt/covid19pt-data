import datetime
import requests
import pandas as pd
import numpy as np
from pathlib import Path


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


def convert(x):
    if np.isnan(x):
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
        "?where=1%3D1&outFields=*&cacheHint=true&orderByFields=Data_do_Relatorio%20desc&f=pjson"
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
            latest.loc[:, col] = 0  # NaN!

    # Find rows with differences
    merged = available.merge(
        latest, how="outer", on=["data"], suffixes=("_available", "_latest")
    )
    merged = merged.fillna('""')

    different_rows = merged[
        (merged.amostras_available != merged.amostras_latest)
        | (merged.amostras_novas_available != merged.amostras_novas_latest)
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
    cols = [x for x in updated.columns if not x.startswith("data")]
    updated[cols] = updated[cols].applymap(convert)
    # save to .csv
    updated.to_csv(PATH_TO_CSV, index=False, line_terminator="\n")
