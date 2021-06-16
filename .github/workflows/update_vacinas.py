import datetime
import requests
import pandas as pd
import numpy as np
import sys
import json
from pathlib import Path


DEBUG = True

def fix_date(unix_date, doses_total, latest_data=None, latest_total=None):
    # hack data incorreta dia 31-01 dizia 01-02
    if unix_date == 1612137600 and doses_total == 336771:
        return unix_date - 86400
    # hack data incorreta dia 06-02 dizia 05-02
    if unix_date == 1612483200 and doses_total == 394088:
        return unix_date + 86400
    # hack data incorreta dia 19-02 dizia 18-02
    if unix_date == 1613606400 and doses_total == 618636:
        return unix_date + 86400
    # hack data incorreta dia 19-02 dizia 18-02
    if unix_date == 1613692800 and doses_total == 656411:
        return unix_date + 86400
    # hack data incorreta dia 11-04 dizia 10-04
    if unix_date == 1618012800 and doses_total == 2121998:
        return unix_date + 86400
    # hack data incorreta dia 22-04 dizia 21-04
    if unix_date == 1618963200 and doses_total == 2711174:
        return unix_date + 86400
    # hack data incorreta dia 23-04 dizia 22-04
    if unix_date == 1619049600 and doses_total == 2778982:
        return unix_date + 86400
    # hack data incorreta dia 09-05 dizia 18-04
    if unix_date == 1618704000 and doses_total == 3845140:
        return 1620432000 + 86400

    # Desde dia 22-04-2021 que a API tem o dia anterior (!?)

    # hack data incorreta dia 22-05 dizia 20-04 e devia 21
    if unix_date == 1621468800 and doses_total == 4842021:
        unix_date = unix_date + 86400
    # hack data incorreta dia 23-05 ainda dizia 20-04
    elif unix_date == 1621468800 and doses_total == 4913087:
        unix_date = unix_date + 86400 * 2
    # hack data incorreta dia 30-05 ainda dizia 28-04
    elif unix_date == 1622160000 and doses_total == 5442582:
        unix_date = unix_date + 86400


    last_date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%Y-%m-%d")
    latest_date = pd.to_datetime(latest_data, format="%Y-%m-%d").strftime("%Y-%m-%d")
    if last_date == latest_date and doses_total > latest_total:
        unix_date += 86400
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        print("FIXING DATE today={today} API date={latest_date} last date={last_date}")

    return unix_date

def save_vacinas(text, data, latest_data=None, latest_total=None):
    # Save a copy
    attributes = data["features"][0]["attributes"]
    doses_total = attributes["Vacinados_Ac"]
    unix_date = fix_date(attributes["Data"] / 1000, doses_total, latest_data, latest_total)
    last_date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%Y-%m-%d")
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    if today != last_date:
        print(f"Vaccines with no new data, today={today} last_date={last_date}")
    else:
        PATH_TO_JSON = str(Path(__file__).resolve().parents[2] / "extra" / "vacinas" / "diário" / f"{today}_vacinas.json")
        print(f"Saving a copy for today={today} at {PATH_TO_JSON}")
        with open(PATH_TO_JSON, "w") as f:
            f.write(text)

def get_vacinas(url, latest_data=None, latest_total=None):
    if len(sys.argv) > 1:
        local_file = sys.argv[1]
        with open(local_file, "r") as f:
            data = json.loads(f.read())
        print(f"Loading from '{local_file}'")
    else:
        print(f"Loading from '{url}'")
        r = requests.get(url=url)
        data = r.json()
        save_vacinas(r.text, data, latest_data, latest_total)

    vacinas = []
    for entry in data["features"]:
        attributes = entry["attributes"]
        doses_total = attributes.get("Vacinados_Ac", None)
        doses_novas = attributes.get("Vacinados", None)
        doses1_total = attributes.get("Inoculacao1_Ac", None)
        doses1_novas = attributes.get("Inoculacao1", None)
        doses2_total = attributes.get("Inoculacao2_Ac", None)
        doses2_novas = attributes.get("Inoculacao2", None)
        unix_date = fix_date(attributes["Data"] / 1000, doses_total, latest_data, latest_total)
        frmt_date = datetime.datetime.utcfromtimestamp(unix_date)

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

    FIXES = [
        # data DD-MM-YYYY, columns, fix_value
        # https://twitter.com/govpt/status/1355528712813473794
        # https://twitter.com/SNS_Portugal/status/1355606908833566728
        ["30-01-2021", "doses1", 264772],
        ["30-01-2021", "doses2", 65461],
        # https://twitter.com/govpt/status/1355871948350386180
        # https://twitter.com/SNS_Portugal/status/1355922638816817156
        ["31-01-2021", "doses1", 268386],
        ["31-01-2021", "doses2", 68385],
        # https://twitter.com/govpt/status/1356233893029048324
        # ...
        ["01-02-2021", "doses1", 269814],
        ["01-02-2021", "doses2", 68752],
        # https://twitter.com/govpt/status/1356596233264132102
        # json includes doses1 and doses2 - see extra/vacinas/diário/*.json
    ]

    for fix in FIXES:
        if DEBUG:
            old = data.loc[data.data == fix[0], fix[1]].to_numpy()[0]
            try:
                old = old.tolist()
            except AttributeError:
                pass
            if old != fix[2]:
                print(f"Override {fix[0]} {fix[1]} from {old} to {fix[2]}")
        data.loc[data.data == fix[0], fix[1]] = fix[2]

    # recalculate *_novas when missing or incorrect
    last = {}
    for i, row in data.iterrows():
        for k in ["doses", "doses1", "doses2", 'pessoas_vacinadas_completamente', 'pessoas_vacinadas_parcialmente']:
            cur = row[f"{k}_novas"] or 0
            val = row[f"{k}"] or 0
            last_val = last.get(f"{k}", 0)
            diff = val - last_val if val else 0
            if last_val and cur != diff:
                # print(f"FIX {row.data} {k} from {cur} to {diff} v={val} lv={last_val}")
                data.at[i, f"{k}_novas"] = diff
            last[f"{k}"] = val

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
        #"https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/Covid19_Total_Vacinados_Temporario/FeatureServer/0/query"
        "?where=1%3D1&"
        "&orderByFields=Data+desc"
        "&f=pjson&outFields=*&cacheHint=false"
        "&resultType=standard"
        # "&resultOffset=0&resultRecordCount=1000"
    )

    # Get latest data
    latest = pd.read_csv(PATH_TO_CSV)
    latest["data"] = pd.to_datetime(latest["data"], format="%d-%m-%Y")

    latest_data, latest_total = latest.data.tail(1).values[0], int(latest.doses.tail(1))
    # Get the data available in the dashboard
    available = get_vacinas(URL, latest_data, latest_total)

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
                # don't update *_novas, as they're recalculated anyway on the "fix"
                for j in [""]:  # ["", "_novas"]:
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
                        row["pessoas_vacinadas_completamente"],
                        row["pessoas_vacinadas_completamente_novas"],
                        row["pessoas_vacinadas_parcialmente"],
                        row["pessoas_vacinadas_parcialmente_novas"],
                    ]
                ],
                columns=updated.columns,
            )
            updated = pd.concat([updated, tmp_df], ignore_index=True)

    # sort by date
    updated = updated.sort_values("data")
    updated["data"] = updated["data"].dt.strftime("%d-%m-%Y")

    # add people columns
    updated['pessoas_vacinadas_completamente'] = updated['doses2']
    updated['pessoas_vacinadas_completamente_novas'] = updated['doses2_novas']
    updated['pessoas_vacinadas_parcialmente'] = updated['doses1'] - updated['doses2']
    updated['pessoas_vacinadas_parcialmente_novas'] = updated['doses1_novas'] - updated['doses2_novas']

    # convert values to integer
    cols = [x for x in updated.columns if not x.startswith("data")]
    updated[cols] = updated[cols].applymap(convert)
    # fix values
    updated = fix_vacinas(updated)


    # save to .csv
    updated.to_csv(PATH_TO_CSV, index=False, line_terminator="\n")
