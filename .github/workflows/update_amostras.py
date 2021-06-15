import datetime
import requests
import pandas as pd
import numpy as np
import sys
from pathlib import Path


DEBUG = True


def get_amostras(url):
    print(f"Loading from '{url}'")
    r = requests.get(url=url)
    data = r.json()
    amostras = []

    # Sort by total amostras, which should allow us to guess the date if missing
    features = sorted(
        data["features"],
        key=lambda entry: entry["attributes"].get(
            "Total_Amostras__Ac", entry["attributes"].get("Amostras__Ac", None)
        ),
        reverse=False,
    )

    last_fid, last_date, last_data = None, None, None
    for entry in features:
        attr = entry["attributes"]

        amostras_total = attr.get("Total_Amostras__Ac", attr.get("Amostras__Ac", None))
        amostras_novas = attr.get(
            "Total_Amostras_Novas", attr.get("Amostras_Novas", None)
        )
        amostras_pcr_total = attr.get("Testes_PCR_Amostras__Ac", None)
        amostras_pcr_novas = attr.get("Testes_PCR_Amostras_Novas", None)
        amostras_antigenio_total = attr.get("Testes_Antigenio_Amostras__Ac", None)
        amostras_antigenio_novas = attr.get("Testes_Antigenio_Amostras_Novas", None)
        data = [
            None,  # will be filled below
            amostras_total,
            amostras_novas,
            amostras_pcr_total,
            amostras_pcr_novas,
            amostras_antigenio_total,
            amostras_antigenio_novas,
        ]

        fid = attr.get("FID", None)

        unix_date = attr.get("Data_do_Relatorio", attr.get("Data_do_Relatório", None))
        frmt_date = (
            datetime.datetime.utcfromtimestamp(unix_date / 1000) if unix_date else None
        )

        if not unix_date:
            # ensure each of the three totals are larger or equal than previous day
            ok = True
            for i in [1, 3, 5]:
                if last_data[i] > data[i]:
                    ok = False

            last_frmt_date = datetime.datetime.utcfromtimestamp(last_date / 1000)
            unix_date = last_date + 86400000  # assume it's the following day
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date / 1000)
            print(
                ("" if ok else "NOT ") + f"Fixing entry for"
                f" fid={fid} last={last_fid}"
                f" date={frmt_date} / {unix_date}"
                f" last_date={last_frmt_date} / {last_date}"
            )
            if not ok:
                print(f"  last={last_data}")
                print(f"  cur={data}")
                sys.exit(1)

        data[0] = frmt_date
        amostras.append(data)
        last_fid, last_date, last_data = fid, unix_date, data

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


def fix_amostras(data):

    for i in ["26-02-2020", "27-02-2020", "28-02-2020", "29-02-2020"]:
        data.loc[data.data == i, data.columns[1:]] = 0

    # data is constantly changing about two weeks into the past, and totals
    # are constantly incorrect, so we just give up and only use the totals
    # and recalculate the diff out of them
    data.loc[1:, "amostras_novas"] = data.loc[1:, "amostras"].diff(1)
    data.loc[1:, "amostras_pcr_novas"] = data.loc[1:, "amostras_pcr"].diff(1)
    data.loc[1:, "amostras_antigenio_novas"] = data.loc[1:, "amostras_antigenio"].diff(
        1
    )

    for i in ["26-02-2020", "27-02-2020", "28-02-2020", "29-02-2020"]:
        data.loc[data.data == i, data.columns[1:]] = ""

    FIXES = [
        # [data DD-MM-YYYY, columns, fix_value]
    ]

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
        #"https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/Covid19_Amostras_Temporario/FeatureServer/0/query"
        "?where=Total_Amostras__Ac+%3E+0"
        "&orderByFields=Data_do_Relatorio+desc"
        "&f=pjson&outFields=*&cacheHint=false"
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
