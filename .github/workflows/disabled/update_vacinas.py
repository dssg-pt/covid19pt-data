import datetime
import requests
import pandas as pd
import numpy as np
import sys
import json
from pathlib import Path


DEBUG = True

HIDE_JULY_FIRST_WEEK = True

def fix_date(unix_date, doses_total, latest_data=None, latest_total=None):

    if False:
        print(
            f'unix_date={unix_date}'
            f' doses_total={doses_total}'
            f' latest_data={latest_data}'
            f' latest_total={latest_total}'
        )

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
    # hack data incorrecta dia 03-08 dizia 02-08
    if unix_date == 1627862400 and doses_total == 11791962:
        return unix_date + 86400
    # hack dia 23-08-2021 actualizou dia 22-08-2021
    if unix_date == 1629590400 and doses_total == 13550289:
        return unix_date + 86400
    if unix_date == 1630540800 and doses_total == 14177937:
        return unix_date + 86400

    # Dia 12-07-2021 após um fim-de-semana sem dados, volta a ser o próprio dia
    if unix_date >= 1626048000:
        return unix_date

    # Desde dia 22-04-2021 que a API tem o dia anterior (!?)

    # hack data incorreta dia 22-05 dizia 20-04 e devia 21
    if unix_date == 1621468800 and doses_total == 4842021:
        unix_date += 86400
    # hack data incorreta dia 23-05 ainda dizia 20-04
    elif unix_date == 1621468800 and doses_total == 4913087:
        unix_date += 86400 * 2
    # hack data incorreta dia 30-05 ainda dizia 28-04
    elif unix_date == 1622160000 and doses_total == 5442582:
        unix_date += 86400

    unix_date += 86400

    last_date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%Y-%m-%d")
    latest_date = pd.to_datetime(latest_data, format="%Y-%m-%d").strftime("%Y-%m-%d")
    if last_date == latest_date and doses_total > latest_total:
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        print(f"FIXING DATE today={today} API date={latest_date} last date={last_date}")

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
        r = requests.get(
            url=url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
            },
        )
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

        # 2021-09-12 o valor "Inoculacao2_Ac" não foi actualizado e é menor que o "Inoculacao2"
        doses_total = max(doses_total, doses_novas)
        doses1_total = max(doses1_total, doses1_novas)
        doses2_total = max(doses2_total, doses2_novas)
        doses_novas, doses1_novas, doses2_novas = 0, 0, 0

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

        # 2021-08-06 doses1+doses2 != doses
        # 6884703 + 5200840 == 12085543 mas != 12086076 -> -533
        # optou-se pela solução mais conservadora e que altera apenas um valor
        ["06-08-2021", "doses", 6884703 + 5200840],
        # idem, 7494705 + 5567766 == 13062471 mas != 13062853 -> -382
        ["17-08-2021", "doses", 7494705 + 5567766],
        # 12-09 tem 14729376 (+125682), 8436183 (+9823), 6177334 (+0)
        # 2a dose são os 115k do fim de semana dos 12-15
        # update: Inoculacao2 (que devia ser o diário) está correcto mas
        # Inoculacao2_Ac (que devia ser o acumulado) está com o valor anterior
        # corrigido com o max(total, novas) abaixo
        # ["12-09-2021", "doses2", 6177334 + 125682 - 9823], # 6193193 - 115859

        # 2021-09-27 dados diários têm sido ajustados do relatório #31 de dia 13 e não
        # do #32 dia 20 pois não houve dados dia 20. Dataset #33 também reajustou os
        # dados do passado (como costume) portanto dados "inoculados" dá negativo.
        # Dataset #33 tem +85344 entre 13 e 27: 13 = 8845252, 20 = 8894442 (+49190), 27 = 8930596 (+36154)
        # Dados diários tem +90566 entre 13 e 27: 13 = 8441603, 27 = 8532169
        # 26-09-2021,15205735,,8530494,,6675241,,8636142,,298001,,8934143,,15952609,
        # 27-09-2021,15212273,6538,8532169,1675,6680104,4863,8663808,27666,266788,-31213,8930596,-3547,15956183,3574
        # Como não há dados de dia 25, reajustado dia 26 para dar sempre valores
        # positivos e, há falta de dados oficiais, os "novos" serem alinhados 26->27 com
        # os dados diários: doses +6538 (vacinas), doses1 +1675, doses2 +4863 (completo)
        ["26-09-2021", "vacinas", 15956183 - 6538], # 1_595_2609 -> 1_594_9645
        ["26-09-2021", "pessoas_inoculadas", 8930596 - 1675], # 8_934_143 -> 8_928_921
        ["26-09-2021", "pessoas_vacinadas_completamente", 8663808 - 4863], # 8_636_142 -> 8_658_945
        ["26-09-2021", "pessoas_vacinadas_parcialmente", 8928921 - 8658945], # 266788 ->
    ]

    for fix in FIXES:
        if DEBUG:
            old = data.loc[data.data == fix[0], fix[1]].to_numpy()[0]
            try:
                old = old.tolist()
            except AttributeError:
                pass
            if old != fix[2] and old > 0:
                print(f"Override {fix[0]} {fix[1]} from {old} to {fix[2]}")
        data.loc[data.data == fix[0], fix[1]] = fix[2]

    return data

def fix_vacinas2(data):

    # dados diários 28-06-2021 a 04-07-2021 não fazem sentido
    if HIDE_JULY_FIRST_WEEK:
        for i in range(2, 7):
            dia = (datetime.datetime(2021, 6, 28) + datetime.timedelta(days=i)).strftime("%d-%m-%Y")
            cols = ['pessoas_vacinadas_completamente', 'pessoas_vacinadas_parcialmente', 'pessoas_inoculadas', 'vacinas']
            data.loc[data.data == dia, cols] = ''
        # dia 6 taskforce anuncia recorde 141K, tem 146k (ilhas), aceitável
        # dia 7 taskforce anuncia recorde 151k, tem 158k (ilhas), aceitável
        # dia 8 tem 182k mas dias mais tarde há recorde 156k, não pode ser
        dia = datetime.datetime(2021, 7, 8).strftime("%d-%m-%Y")
        cols = ['pessoas_vacinadas_completamente', 'pessoas_vacinadas_parcialmente', 'pessoas_inoculadas', 'vacinas']
        data.loc[data.data == dia, cols] = ''

    # hack para publicar os dados de dia 2021-09-20 (do relatório) pois não houve diários
    # e o código necessita deles
    data.loc[data.data == "20-09-2021", [
        'pessoas_inoculadas',
        'pessoas_vacinadas_completamente',
        'pessoas_vacinadas_parcialmente',
        'vacinas',
    ]] = [
        8_889_941,
        8_546_688,
        8_889_941 - 8_546_688,
        (
            5_584_026 + # norte
            2_596_902 + # centro
            5_489_097 + # lvt
            735_227 + # alentejo
            659_736 + # algarve
            383_428 + # madeira
            360_641 + # açores
            0
        ),
        ]

    # recalculate *_novas when missing or incorrect
    last = {}
    for i, row in data.iterrows():
        cols = ['pessoas_vacinadas_completamente', 'pessoas_vacinadas_parcialmente', 'pessoas_inoculadas', 'vacinas']
        for k in ["doses", "doses1", "doses2"] + cols:
            val = row[k]
            last_val = last.get(k, 0)
            last[f"{k}"] = val
            # print(f"data={row.data} k={k} val={val} last_val={last_val}")
            if val=='' or last_val=='' or np.isnan(val) or np.isnan(last_val):
                data.at[i, f"{k}_novas"] = ''
            elif row.data == '12-07-2021':
                data.at[i, f"{k}_novas"] = ''
            else:
                cur = row[f"{k}_novas"]
                diff = val - last_val
                if cur != diff:
                    data.at[i, f"{k}_novas"] = diff
                    # first row of pessoas has novas recalculated and empty, don't print them
                    if (i != 0 or cur != '') and cur != 0:
                        print(f"update i={i} data={row.data} k={k}_novas from cur={cur} to diff={diff} val={val} last_val={last_val}")

    # sem dados 9 a 11-07-2021 inclusive
    data.loc[data.data == "12-07-2021", [col for col in data.columns if '_novas' in col]] = ''

    # hack para remover "novas" de dia 21 pois há relatório 20 mas não há dados diários
    data.loc[data.data == "21-09-2021", [col for col in data.columns if '_novas' in col]] = ''

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

def ajuste_2021_07_05(df):
    # dados diários dia 28-06 a 08-07 estão inflated talvez por incluirem as
    # ilhas incluindo o histórico todo, portanto a semana 28-06 a 04-07 é ignorada
    # (vide HIDE_JULY_FIRST_WEEK) e os dias 05-07 a 08-07 são alinhados pelos dados
    # semanais assumindo nacional e não continente. Dia 12 volta ao calculo normal
    df5 = df[df['data'] =='05-07-2021']
    diff5 = [ int(df5['doses2_diff']), int(df5['doses1_diff']), int(df5['doses_diff']) ]
    diff12 = [
        int( df5[f'pessoas_vacinadas_completamente'] - df5[f'doses2_diario']
            - df5['doses2_continente'] + df5['doses2']
        ),
        int( df5[f'pessoas_inoculadas'] - df5[f'doses1_diario']
            - df5['doses1_continente'] + df5['doses1']
        ),
        int( df5[f'doses'] - df5[f'doses_diario']
            - df5['doses_continente'] + df5['doses']
        ),
    ]
    df.loc[df['data'] == '05-07-2021', ['doses2_diff', 'doses1_diff', 'doses_diff']] = diff12
    return diff5

def ajuste_dados_semanais(updated):
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "vacinas_detalhe.csv")

    # Para os dias do relatório, calcula a diferença entre `doses` com ´vacinas` (ilhas),
    # `doses2` com `completo` (ilhas + unidoses em falta) e `doses1` com `inoculados`
    df_vacinas_detalhes = pd.read_csv(PATH_TO_CSV)

    df_vacinas_detalhes['dt'] = df_vacinas_detalhes['data'].apply(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
    for r, row in df_vacinas_detalhes.loc[df_vacinas_detalhes.dt >= '2021-10-01'].iterrows():
        data = [
            row['data'],
            row['doses_continente'] - row['dosesunk_continente'],
            row['doses1_continente'],
            #row['pessoas_inoculadas_continente'],
            row['doses2_continente'],
            #row['pessoas_vacinadas_completamente_continente'],
        ]
        # df_tmp = pd.DataFrame(data=[data], columns=["data", "doses", "doses1", "doses2"])
        # updated = pd.concat([updated, df_tmp])
        updated.loc[updated['data'] == row['data'], ["data", "doses", "doses1", "doses2"]] = data

    df = pd.merge(df_vacinas_detalhes, updated, how='left', on='data', suffixes=("", "_diario"))

    df[f'doses2_diff'] = df[f'pessoas_vacinadas_completamente'] - df[f'doses2_diario']
    df[f'doses1_diff'] = df[f'pessoas_inoculadas'] - df[f'doses1_diario']
    df[f'doses_diff'] = df[f'doses'] - df[f'doses_diario']

    # FIX relatório diário semana 2021-07-05
    diff5 = ajuste_2021_07_05(df)

    kk = ['','1','2']
    df = df[ ['data'] + [f'doses{k}_diff' for k in kk] ]
    updated = pd.merge(updated, df, how="left", on="data")
    for k in kk:
        updated[f'doses{k}_diff'] = updated[f'doses{k}_diff'].ffill().fillna(0)

    # fix 05-07-2021
    for i in [5, 6, 7, 8]:
        updated.loc[updated['data'] == f'0{i}-07-2021', ['doses2_diff', 'doses1_diff', 'doses_diff']] = diff5

    updated['pessoas_vacinadas_completamente'] = updated['doses2']
    updated['pessoas_vacinadas_parcialmente'] = updated['doses1'] - updated['doses2']
    updated['pessoas_inoculadas'] = updated['doses1']
    updated['vacinas'] = updated['doses']

    DEBUG_ADJUSTMENT=False

    if DEBUG_ADJUSTMENT:
        updated['pessoas_vacinadas_completamente_1'] = updated['pessoas_vacinadas_completamente']
        updated['pessoas_vacinadas_parcialmente_1'] = updated['pessoas_vacinadas_parcialmente']
        updated['pessoas_inoculadas_1'] = updated['pessoas_inoculadas']
        updated['vacinas_1'] = updated['vacinas']

    # ajuste doses semanais
    updated['pessoas_vacinadas_completamente'] += updated['doses2_diff']
    updated['pessoas_inoculadas'] += updated['doses1_diff']
    updated['pessoas_vacinadas_parcialmente'] = updated['pessoas_inoculadas'] - updated['pessoas_vacinadas_completamente']
    updated['vacinas'] += updated['doses_diff']

    if DEBUG_ADJUSTMENT:
        updated['pessoas_vacinadas_completamente_2'] = updated['pessoas_vacinadas_completamente']
        updated['pessoas_vacinadas_parcialmente_2'] = updated['pessoas_vacinadas_parcialmente']
        updated['pessoas_inoculadas_2'] = updated['pessoas_inoculadas']
        updated['vacinas_2'] = updated['vacinas']

    if DEBUG_ADJUSTMENT:
        updated.to_csv(PATH_TO_CSV + "_debug.csv", index=False, line_terminator="\n")

    for k in kk:
        updated.drop(f'doses{k}_diff', inplace=True, axis=1)

    return updated


if __name__ == "__main__":

    # DEPRECATED
    print("DEPRECATED")
    sys.exit(1)

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
    # print(URL)

    # Get latest data
    latest = pd.read_csv(PATH_TO_CSV)
    latest["data"] = pd.to_datetime(latest["data"], format="%d-%m-%Y")

    latest_data, latest_total = latest.data.tail(1).values[0], latest.doses.tail(1).item()
    if not np.isnan(latest_total): latest_total = int(latest_total)

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
        latest, how="outer", on=["data"], suffixes=("", "_latest")
    )
    merged = merged.fillna('""')

    different_rows = merged[
        (merged.doses != merged.doses_latest)
        | (merged.doses1 != merged.doses1_latest)
        | (merged.doses2 != merged.doses2_latest)
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
                    available = row[f"{l}"]
                    if latest != available and available and available != '""':
                        print(f"Update {row['data']} from {latest} to {available}")
                        updated.at[index, f"{l}"] = available

        # new row
        else:
            tmp_df = pd.DataFrame(
                [ [row[col] for col in updated.columns] ],
                columns=updated.columns,
            )
            updated = pd.concat([updated, tmp_df], ignore_index=True)

    # Add missing days after End Of Vaccination (27-09-2021)
    dt = datetime.datetime(2021, 9, 27)
    now = datetime.datetime.now() - datetime.timedelta(days=1) # before midnight
    while dt < now:
        if len(updated[ updated['data'] == dt.strftime("%Y-%m-%d")]) == 0:
            tmp_df = pd.DataFrame(
                [ [dt] ],
                columns=['data'],
            )
            updated = pd.concat([updated, tmp_df], ignore_index=True)
        dt = dt + datetime.timedelta(days=1)

    # sort by date
    updated = updated.sort_values("data")
    updated["data"] = updated["data"].dt.strftime("%d-%m-%Y")

    updated = fix_vacinas(updated)

    # add people columns
    updated['pessoas_vacinadas_completamente'] = updated['doses2']
    updated['pessoas_vacinadas_parcialmente'] = updated['doses1'] - updated['doses2']
    updated['pessoas_inoculadas'] = updated['doses1']
    updated['vacinas'] = updated['doses']
    # ajuste aos dados semanais
    updated = ajuste_dados_semanais(updated)
    # recalculate daily diff
    updated['pessoas_vacinadas_completamente_novas'] = updated['pessoas_vacinadas_completamente'].diff(1)
    updated['pessoas_vacinadas_parcialmente_novas'] = updated['pessoas_vacinadas_parcialmente'].diff(1)
    updated['pessoas_inoculadas_novas'] = updated['pessoas_inoculadas'].diff(1)
    updated['vacinas_novas'] = updated['vacinas'].diff(1)

    # convert values to integer
    cols = [x for x in updated.columns if not x.startswith("data")]
    updated[cols] = updated[cols].applymap(convert)
    # fix values
    updated = fix_vacinas(updated)
    updated = fix_vacinas2(updated)

    updated = updated[ "data,doses,doses_novas,doses1,doses1_novas,doses2,doses2_novas,pessoas_vacinadas_completamente,pessoas_vacinadas_completamente_novas,pessoas_vacinadas_parcialmente,pessoas_vacinadas_parcialmente_novas,pessoas_inoculadas,pessoas_inoculadas_novas,vacinas,vacinas_novas".split(",") ]

    # save to .csv
    updated.to_csv(PATH_TO_CSV, index=False, line_terminator="\n")
