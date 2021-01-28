import datetime
import requests
import pandas as pd
import numpy as np
import sys
import json
from pathlib import Path


DEBUG = True


def get_vacinas(url):
    if len(sys.argv) > 1:
        local_file = sys.argv[1]
        with open(local_file, "r") as f:
            data = json.loads(f.read())
        print(f"Loading from '{local_file}'")
    else:
        r = requests.get(url=url)
        data = r.json()
        print(f"Loading from '{url}'")

    vacinas = []
    for entry in data["features"]:
        unix_date = entry["attributes"]["Data"] / 1000
        frmt_date = datetime.datetime.utcfromtimestamp(unix_date)
        doses_total = entry["attributes"].get("Vacinados_Ac", None)
        doses_novas = entry["attributes"].get("Vacinados", None)
        doses1_total = entry["attributes"].get("Inoculacao1_Ac", None)
        doses1_novas = entry["attributes"].get("Inoculacao1", None)
        doses2_total = entry["attributes"].get("Inoculacao2_Ac", None)
        doses2_novas = entry["attributes"].get("Inoculacao2", None)

        # 26-01-2021 to ? only have Vacinados without novas nor history
        if doses_novas == doses_total and doses1_total is None:
            doses_novas = None

        vacinas.append(
            [
                frmt_date,
                doses_total,
                doses_novas,
                doses1_total,
                doses1_novas,
                doses2_total,
                doses2_novas,
            ]
        )

    vacinas_df = pd.DataFrame(
        data=vacinas,
        columns=[
            "data",
            "doses",
            "doses_novas",
            "doses1",
            "doses1_novas",
            "doses2",
            "doses2_novas",
        ],
    )
    return vacinas_df


def fix_vacinas(data):
    # \o/
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
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "vacinas.csv")
    URL = (
        "https://services5.arcgis.com/eoFbezv6KiXqcnKq/arcgis/rest/services/Covid19_Total_Vacinados/FeatureServer/0/query"
        "?where=1%3D1&"
        "&orderByFields=Data+desc"
        "&f=pjson&outFields=*&cacheHint=true"
        "&resultType=standard"
        # "&resultOffset=0&resultRecordCount=1000"
    )
    # Get the data available in the dashboard
    available = get_vacinas(URL)

    # Get latest data
    latest = pd.read_csv(PATH_TO_CSV)
    latest["data"] = pd.to_datetime(latest["data"], format="%d-%m-%Y")

    for col in [
        "doses",
        "doses_novas",
        "doses1",
        "doses1_novas",
        "doses2",
        "doses2_novas",
    ]:
        if col not in latest.columns:
            latest.loc[:, col] = np.nan

    # Find rows with differences
    merged = available.merge(
        latest, how="outer", on=["data"], suffixes=("_available", "_latest")
    )
    merged = merged.fillna('""')

    different_rows = merged[
        (merged.doses_available != merged.doses_latest)
        | (merged.doses_novas_available != merged.doses_novas_latest)
        | (merged.doses1_available != merged.doses1_latest)
        | (merged.doses1_novas_available != merged.doses1_novas_latest)
        | (merged.doses2_available != merged.doses2_latest)
        | (merged.doses2_novas_available != merged.doses2_novas_latest)
    ]

    # Order by date
    different_rows = different_rows.sort_values(by="data")

    # Update values
    updated = latest.copy()

    for r, row in different_rows.iterrows():

        # existing row
        if (updated.data == row["data"]).any():
            index = updated.index[updated["data"] == row["data"]]
            for k in ["", "1", "2"]:
                for j in ["", "_novas"]:
                    l = f"doses{k}{j}"
                    latest = row[f"{l}_latest"]
                    available = row[f"{l}_available"]
                    if latest != available and available and available != '""':
                        print(f"Update {row['data']} from {latest} to {available}")
                        updated.at[index, f"{l}"] = available

        # new row
        else:
            tmp_df = pd.DataFrame(
                [
                    [
                        row["data"],
                        row["doses_available"],
                        row["doses_novas_available"],
                        row["doses1_available"],
                        row["doses1_novas_available"],
                        row["doses2_available"],
                        row["doses2_novas_available"],
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
    updated = fix_vacinas(updated)
    # save to .csv
    updated.to_csv(PATH_TO_CSV, index=False, line_terminator="\n")
