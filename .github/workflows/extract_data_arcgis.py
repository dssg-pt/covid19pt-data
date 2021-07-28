import requests
import datetime
import sys
import pandas as pd
from pathlib import Path

DMY = "%d-%m-%Y"

if __name__ == "__main__":

    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "data.csv")

    DAYS_OFFSET = 0
    if len(sys.argv) > 1:
        try:
            DAYS_OFFSET = int(sys.argv[1])
            today = (datetime.date.today() - datetime.timedelta(days=DAYS_OFFSET)).strftime(DMY)
            print(f"Retrieving date={today} OFFSET={DAYS_OFFSET}")
        except ValueError:
            DAYS_OFFSET = -1
            today = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d').strftime(DMY)
            print(f"Retrieving date={today}")
    else:
        today = (datetime.date.today() - datetime.timedelta(days=DAYS_OFFSET)).strftime(DMY)
        if DAYS_OFFSET:
            print(f"Retrieving date={today} OFFSET={DAYS_OFFSET}")
        else:
            print(f"Retrieving date={today}")

        csv_path = str(Path(__file__).resolve().parents[2] / "data.csv")
        latest = pd.read_csv(csv_path)
        latest_date = latest[-1:]["data"].item()
        if today == latest_date:
            print(f"Already got {today}")
            sys.exit(0)

    URL = (
        'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID_ARS_PT_HISTORICO_view/FeatureServer/0/query'
        "?f=json&outFields=*&cacheHint=false"
        '&where=1%3d1'
        '&orderByFields=Data_ARS+desc'
        '&resultRecordCount=10000'
    )
    print(f"Loading from '{URL}'")
    data = requests.get(URL).json()

    (found_date, latest_date) = (False, 0)
    for entry in data["features"]:
        attributes = entry['attributes']
        if not attributes["Data_ARS"]:
            continue

        unix_date = attributes["Data_ARS"] / 1000
        frmt_date = datetime.datetime.utcfromtimestamp(unix_date).strftime(DMY)
        latest_date = max(latest_date, unix_date)

        if frmt_date != today:
            continue

        found_date = True

        if attributes["ARSNome"] == "Nacional":

            # Continuam
            confirmados = attributes["casos"]
            obitos = attributes["obitos"]
            recuperados = attributes["recuperados"]
            confirmados_novos = attributes["novos_c"]
            internados = attributes["internamento"]
            internados_enfermaria = attributes["internadosenfermaria"]
            internados_uci = attributes["uci"]
            confirmados_m = attributes["casos_h_total"]
            confirmados_f = attributes["casos_m_total"]
            # 2021-07-16 agora há casos_d_<idade>
            confirmados_desconhecidos = attributes['casos_d_total'] # confirmados - confirmados_m - confirmados_f
            vigilancia = attributes["contactos"]
            ativos = attributes["ativos"]

            # Novos
            confirmados_0_9_f = attributes["casos_m_0009"]
            confirmados_0_9_m = attributes["casos_h_0009"]
            confirmados_10_19_f = attributes["casos_m_1019"]
            confirmados_10_19_m = attributes["casos_h_1019"]
            confirmados_20_29_f = attributes["casos_m_2029"]
            confirmados_20_29_m = attributes["casos_h_2029"]
            confirmados_30_39_f = attributes["casos_m_3039"]
            confirmados_30_39_m = attributes["casos_h_3039"]
            confirmados_40_49_f = attributes["casos_m_4049"]
            confirmados_40_49_m = attributes["casos_h_4049"]
            confirmados_50_59_f = attributes["casos_m_5059"]
            confirmados_50_59_m = attributes["casos_h_5059"]
            confirmados_60_69_f = attributes["casos_m_6069"]
            confirmados_60_69_m = attributes["casos_h_6069"]
            confirmados_70_79_f = attributes["casos_m_7079"]
            confirmados_70_79_m = attributes["casos_h_7079"]
            confirmados_80_plus_f = attributes["casos_m_80"]
            confirmados_80_plus_m = attributes["casos_h_80"]

            obitos_f = attributes["obitos_m_total"]
            obitos_m = attributes["obitos_h_total"]
            # if values exist but are zero e.g. 05-10-2020
            missing_obitos = not obitos_f or not obitos_m
            obitos_f = "" if missing_obitos else obitos_f
            obitos_m = "" if missing_obitos else obitos_m

            obitos_0_9_f = attributes["obitos_m_0009"]
            obitos_0_9_m = attributes["obitos_h_0009"]
            obitos_10_19_f = attributes["obitos_m_1019"]
            obitos_10_19_m = attributes["obitos_h_1019"]
            obitos_20_29_f = attributes["obitos_m_2029"]
            obitos_20_29_m = attributes["obitos_h_2029"]
            obitos_30_39_f = attributes["obitos_m_3039"]
            obitos_30_39_m = attributes["obitos_h_3039"]
            obitos_40_49_f = attributes["obitos_m_4049"]
            obitos_40_49_m = attributes["obitos_h_4049"]
            obitos_50_59_f = attributes["obitos_m_5059"]
            obitos_50_59_m = attributes["obitos_h_5059"]
            obitos_60_69_f = attributes["obitos_m_6069"]
            obitos_60_69_m = attributes["obitos_h_6069"]
            obitos_70_79_f = attributes["obitos_m_7079"]
            obitos_70_79_m = attributes["obitos_h_7079"]
            obitos_80_plus_f = attributes["obitos_m_80"]
            obitos_80_plus_m = attributes["obitos_h_80"]

        elif attributes["ARSNome"] == "ARS Norte":
            confirmados_arsnorte = attributes["casos"]
            obitos_arsnorte = attributes["obitos"]

        elif attributes["ARSNome"] == "ARS Centro":
            confirmados_arscentro = attributes["casos"]
            obitos_arscentro = attributes["obitos"]

        elif attributes["ARSNome"] == "ARS Lisboa e Vale do Tejo":
            confirmados_arslvt = attributes["casos"]
            obitos_arslvt = attributes["obitos"]

        elif attributes["ARSNome"] == "ARS Açores":
            confirmados_acores = attributes["casos"]
            obitos_acores = attributes["obitos"]

        elif attributes["ARSNome"] == "ARS Madeira":
            confirmados_madeira = attributes["casos"]
            obitos_madeira = attributes["obitos"]

        elif attributes["ARSNome"] == "Açores":
            confirmados_acores = attributes["casos"]
            obitos_acores = attributes["obitos"]

        elif attributes["ARSNome"] == "Madeira":
            confirmados_madeira = attributes["casos"]
            obitos_madeira = attributes["obitos"]

        elif attributes["ARSNome"] == "ARS Algarve":
            confirmados_arsalgarve = attributes["casos"]
            obitos_arsalgarve = attributes["obitos"]

        elif attributes["ARSNome"] == "ARS Alentejo":
            confirmados_arsalentejo = attributes["casos"]
            obitos_arsalentejo = attributes["obitos"]

        # DADOS QUE DEIXARAM DE SER DISPONIBILIZADOS
        suspeitos = ""
        lab = ""
        cadeias_transmissao = ""
        transmissao_importada = ""
        confirmados_estrangeiro = ""

        sintomas_febre = ""
        sintomas_tosse = ""
        sintomas_dores_musculares = ""
        sintomas_cefaleia = ""
        sintomas_fraqueza_generalizada = ""
        sintomas_dificuldade_respiratoria = ""

        confirmados_desconhecidos_f, confirmados_desconhecidos_m = "", ""
        n_confirmados = ""
        obitos_estrangeiro, recuperados_estrangeiro = "", ""
        recuperados_arsnorte = ""
        recuperados_arscentro = ""
        recuperados_arslvt = ""
        recuperados_arsalentejo = ""
        recuperados_arsalgarve = ""
        recuperados_acores, recuperados_madeira = "", ""

        # Estão no PDF mas não na API
        incidencia_nacional, incidencia_continente = "", ""
        rt_nacional, rt_continente = "", ""

    if not found_date:
        frmt_date = datetime.datetime.utcfromtimestamp(latest_date).strftime("%d-%m-%Y")
        raise Exception(f"Missing date {today}, latest date {frmt_date}")

    try:
        TEMP_CSV = str(Path(__file__).resolve().parents[2] / ".github" / "temp.csv")
        temp = pd.read_csv(TEMP_CSV)
        temp_today = temp.loc[temp.data == today]
        if len(temp_today):
            incidencia_nacional = float(temp_today['incidencia_nacional'])
            incidencia_continente = float(temp_today['incidencia_continente'])
            rt_nacional = float(temp_today['rt_nacional'])
            rt_continente = float(temp_today['rt_continente'])
            print(f"Updating temp data for {today}: {temp_today}")
    except FileNotFoundError:
        pass

    data = [
        today,
        "{} 00:00".format(today),
        confirmados,
        confirmados_arsnorte,
        confirmados_arscentro,
        confirmados_arslvt,
        confirmados_arsalentejo,
        confirmados_arsalgarve,
        confirmados_acores,
        confirmados_madeira,
        confirmados_estrangeiro,
        confirmados_novos,
        recuperados,
        obitos,
        internados,
        internados_uci,
        lab,
        suspeitos,
        vigilancia,
        n_confirmados,
        cadeias_transmissao,
        transmissao_importada,
        confirmados_0_9_f,
        confirmados_0_9_m,
        confirmados_10_19_f,
        confirmados_10_19_m,
        confirmados_20_29_f,
        confirmados_20_29_m,
        confirmados_30_39_f,
        confirmados_30_39_m,
        confirmados_40_49_f,
        confirmados_40_49_m,
        confirmados_50_59_f,
        confirmados_50_59_m,
        confirmados_60_69_f,
        confirmados_60_69_m,
        confirmados_70_79_f,
        confirmados_70_79_m,
        confirmados_80_plus_f,
        confirmados_80_plus_m,
        sintomas_tosse,
        sintomas_febre,
        sintomas_dificuldade_respiratoria,
        sintomas_cefaleia,
        sintomas_dores_musculares,
        sintomas_fraqueza_generalizada,
        confirmados_f,
        confirmados_m,
        obitos_arsnorte,
        obitos_arscentro,
        obitos_arslvt,
        obitos_arsalentejo,
        obitos_arsalgarve,
        obitos_acores,
        obitos_madeira,
        obitos_estrangeiro,
        recuperados_arsnorte,
        recuperados_arscentro,
        recuperados_arslvt,
        recuperados_arsalentejo,
        recuperados_arsalgarve,
        recuperados_acores,
        recuperados_madeira,
        recuperados_estrangeiro,
        obitos_0_9_f,
        obitos_0_9_m,
        obitos_10_19_f,
        obitos_10_19_m,
        obitos_20_29_f,
        obitos_20_29_m,
        obitos_30_39_f,
        obitos_30_39_m,
        obitos_40_49_f,
        obitos_40_49_m,
        obitos_50_59_f,
        obitos_50_59_m,
        obitos_60_69_f,
        obitos_60_69_m,
        obitos_70_79_f,
        obitos_70_79_m,
        obitos_80_plus_f,
        obitos_80_plus_m,
        obitos_f,
        obitos_m,
        confirmados_desconhecidos_m,
        confirmados_desconhecidos_f,
        ativos,
        internados_enfermaria,
        confirmados_desconhecidos,
        incidencia_nacional,
        incidencia_continente,
        rt_nacional,
        rt_continente,
    ]
    new_row = pd.DataFrame([data])

    # write to csv
    csv_path = str(Path(__file__).resolve().parents[2] / "data.csv")
    new_row.to_csv(csv_path, mode="a", header=False, index=False, sep=",")
