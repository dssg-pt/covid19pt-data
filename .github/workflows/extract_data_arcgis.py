import requests
import datetime
import pandas as pd
from pathlib import Path

def get_national_data():

    url_nacional = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19Portugal_view/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&orderByFields=datarelatorio+desc'
    data = requests.get(url_nacional)
    data = data.json()

    dados_nacionais = {}

    for entry in data['features']:

        if entry['attributes']['datarelatorio']:

            unix_date = entry['attributes']['datarelatorio']/1000
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%d-%m-%Y")

            if frmt_date == today:

                dados_nacionais['data'] = frmt_date

                # These seem to be updated everyday
                dados_nacionais['confirmados'] = entry['attributes']['casosconfirmados']
                dados_nacionais['obitos'] = entry['attributes']['nrobitos']
                dados_nacionais['recuperados'] = entry['attributes']['recuperados']
                dados_nacionais['confirmados_novos'] = entry['attributes']['casosnovos']
                dados_nacionais['internados'] = entry['attributes']['CasosInternados']
                dados_nacionais['internados_uci'] = entry['attributes']['CasosInternadosUCI']
                dados_nacionais['confirmados_m'] = entry['attributes']['casosmasculino']
                dados_nacionais['confirmados_f'] = entry['attributes']['casosfeminino']

                dados_nacionais['confirmados_0_9'] = entry['attributes']['gr_etario_0_9']
                dados_nacionais['confirmados_10_19'] = entry['attributes']['gr_etario_10_19']
                dados_nacionais['confirmados_20_29'] = entry['attributes']['gr_etario_20_29']
                dados_nacionais['confirmados_30_39'] = entry['attributes']['gr_etario_30_39']
                dados_nacionais['confirmados_40_49'] = entry['attributes']['gr_etario_40_49']
                dados_nacionais['confirmados_50_59'] = entry['attributes']['gr_etario_50_59']
                dados_nacionais['confirmados_60_69'] = entry['attributes']['gr_etario_60_69']
                dados_nacionais['confirmados_70_79'] = entry['attributes']['gr_etario_70_79']
                dados_nacionais['confirmados_80_89'] = entry['attributes']['gr_etario_80_89']
                dados_nacionais['confirmados_90_99'] = entry['attributes']['gr_etario_90_99']

                dados_nacionais['ativos'] = entry['attributes']['CasosActivos']
                dados_nacionais['obitos_novos'] = entry['attributes']['obitosnovos']
                dados_nacionais['recuperados_novos'] = entry['attributes']['recuperadosnovos']

                # These usually present 'None' values
                dados_nacionais['suspeitos'] = entry['attributes']['casossuspeitos']
                dados_nacionais['lab'] = entry['attributes']['AguardaReslab']
                dados_nacionais['vigilancia'] = entry['attributes']['ContactosVigil']
                dados_nacionais['transmissao_importada'] = entry['attributes']['casosimportados']
                dados_nacionais['cadeias_transmissao'] = entry['attributes']['CadeiasTransm']
                dados_nacionais['confirmados_estrangeiro'] = entry['attributes']['Estrangeiro']

                dados_nacionais['sintomas_febre'] = entry['attributes']['sintomafebre']
                dados_nacionais['sintomas_tosse'] = entry['attributes']['sintomatosse']
                dados_nacionais['sintomas_dores_musculares'] = entry['attributes']['sintomadores']
                dados_nacionais['sintomas_cefaleia'] = entry['attributes']['sintomador']
                dados_nacionais['sintomas_fraqueza_generalizada'] = entry['attributes']['sintomafraqueza']
                dados_nacionais['sintomas_dificuldade_respiratoria'] = entry['attributes']['sintomadifrespiratoria']

    return dados_nacionais

def get_ars_data():
    url_ars = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/ArcGIS/rest/services/COVID_Concelhos_ARS_View2/FeatureServer/0/query?where=ConfirmadosAcumulado_ARS+%3E+0&outFields=*&returnGeometry=false&f=pjson&token='

    data_ars = requests.get(url_ars)
    data_ars = data_ars.json()

    confirmados_ars = {}
    obitos_ars = {}

    for entry in data_ars['features']:

        unix_date_ars = entry['attributes']['Data_ARS']/1000
        frmt_date_ars = datetime.datetime.utcfromtimestamp(unix_date_ars).strftime("%d-%m-%Y")

        if frmt_date_ars == today:

            ars_name = entry['attributes']['ARSNome'].lower()
            confirmados_ars[ars_name] = entry['attributes']['ConfirmadosAcumulado_ARS']
            obitos_ars[ars_name] = entry['attributes']['Obitos_ARS']

    return confirmados_ars, obitos_ars


if __name__ == '__main__':

    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / 'data.csv')
    DAYS_OFFSET = 0
    today = str((datetime.date.today()-datetime.timedelta(days=DAYS_OFFSET)).strftime("%d-%m-%Y"))

    url = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/ArcGIS/rest/services/COVID_Concelhos_DadosDiariosARS_VIEW2/FeatureServer/0/query?where=ConfirmadosAcumulado>=0&outFields=*&orderByFields=Data+desc&groupByFieldsForStatistics=&f=pjson&token='
    data = requests.get(url)
    data = data.json()

    confirmados_ars = {}
    obitos_ars = {}

    # DADOS NACIONAIS
    (found_date, latest_date) = (False, 0)
    for entry in data['features']:
        if entry['attributes']['Data']:

            unix_date = entry['attributes']['Data']/1000
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%d-%m-%Y")
            latest_date = max(latest_date, unix_date)

            if frmt_date == today: # today: #change to another day to experiment
                found_date = True

                #  print("In with", frmt_date)

                if entry['attributes']['ARSNome'] == 'Nacional':

                    # Continuam
                    confirmados = entry['attributes']['ConfirmadosAcumulado']
                    obitos = entry['attributes']['Obitos']
                    recuperados = entry['attributes']['Recuperados']
                    confirmados_novos = entry['attributes']['ConfirmadosNovos']
                    internados = entry['attributes']['Internados']
                    internados_enfermaria = entry['attributes']['InternadosEnfermaria']
                    internados_uci = entry['attributes']['InternadosUCI']
                    confirmados_m = entry['attributes']['conftotalm']
                    confirmados_f = entry['attributes']['conftotalf']

                    # Deixaram de existir
                    suspeitos = entry['attributes'].get('Suspeitos', '')
                    lab = entry['attributes'].get('AguardarResultadosLab', '')
                    vigilancia = entry['attributes'].get('EmVigil', '')
                    transmissao_importada = entry['attributes'].get('casosimportados', '')
                    confirmados_estrangeiro = entry['attributes'].get('Estrangeiro', '')

                    sintomas_febre = entry['attributes'].get('sintomafebre', '')
                    sintomas_tosse = entry['attributes'].get('sintomatosse', '')
                    sintomas_dores_musculares = entry['attributes'].get('sintomadores', '')
                    sintomas_cefaleia = entry['attributes'].get('sintomador', '')
                    sintomas_fraqueza_generalizada = entry['attributes'].get('sintomafraqueza', '')
                    sintomas_dificuldade_respiratoria = entry['attributes'].get('sintomadifrespiratoria', '')

                    # Novos mas não preenchidos (não acrescentar, deixar caso futuramente atualizem os valores)
                    transmissao_contacto = entry['attributes'].get('casoscontacto', '')
                    cadeias_transmissao = entry['attributes'].get('CadeiasTransm', '')

                    # Novos
                    confirmados_0_9_f = entry['attributes']['conf0009f']
                    confirmados_0_9_m = entry['attributes']['conf0009m']
                    confirmados_10_19_f = entry['attributes']['conf1019f']
                    confirmados_10_19_m = entry['attributes']['conf1019m']
                    confirmados_20_29_f = entry['attributes']['conf2029f']
                    confirmados_20_29_m = entry['attributes']['conf2029m']
                    confirmados_30_39_f = entry['attributes']['conf3039f']
                    confirmados_30_39_m = entry['attributes']['conf3039m']
                    confirmados_40_49_f = entry['attributes']['conf4049f']
                    confirmados_40_49_m = entry['attributes']['conf4049m']
                    confirmados_50_59_f = entry['attributes']['conf5059f']
                    confirmados_50_59_m = entry['attributes']['conf5059m']
                    confirmados_60_69_f = entry['attributes']['conf6069f']
                    confirmados_60_69_m = entry['attributes']['conf6069m']
                    confirmados_70_79_f = entry['attributes']['conf7079f']
                    confirmados_70_79_m = entry['attributes']['conf7079m']
                    confirmados_80_plus_f = entry['attributes']['conf80f']
                    confirmados_80_plus_m = entry['attributes']['conf80m']

                    obitos_f = entry['attributes']['obitostotalf']
                    obitos_m = entry['attributes']['obitostotalm']
                    # if values exist but are zero e.g. 05-10-2020
                    missing_obitos = not obitos_f or not obitos_m
                    obitos_f = "" if missing_obitos and not obitos_f else obitos_f
                    obitos_m = "" if missing_obitos and not obitos_m else obitos_m

                    obitos_0_9_f = entry['attributes']['obitos0009f']
                    obitos_0_9_f = "" if missing_obitos and not obitos_0_9_f else obitos_0_9_f
                    obitos_0_9_m = entry['attributes']['obitos0009m']
                    obitos_0_9_m = "" if missing_obitos and not obitos_0_9_m else obitos_0_9_m
                    obitos_10_19_f = entry['attributes']['obitos1019f']
                    obitos_10_19_f = "" if missing_obitos and not obitos_10_19_f else obitos_10_19_f
                    obitos_10_19_m = entry['attributes']['obitos1019m']
                    obitos_10_19_m = "" if missing_obitos and not obitos_10_19_m else obitos_10_19_m
                    obitos_20_29_f = entry['attributes']['obitos2029f']
                    obitos_20_29_f = "" if missing_obitos and not obitos_20_29_f else obitos_20_29_f
                    obitos_20_29_m = entry['attributes']['obitos2029m']
                    obitos_20_29_m = "" if missing_obitos and not obitos_20_29_m else obitos_20_29_m
                    obitos_30_39_f = entry['attributes']['obitos3039f']
                    obitos_30_39_f = "" if missing_obitos and not obitos_30_39_f else obitos_30_39_f
                    obitos_30_39_m = entry['attributes']['obitos3039m']
                    obitos_30_39_m = "" if missing_obitos and not obitos_30_39_m else obitos_30_39_m
                    obitos_40_49_f = entry['attributes']['obitos4049f']
                    obitos_40_49_f = "" if missing_obitos and not obitos_40_49_f else obitos_40_49_f
                    obitos_40_49_m = entry['attributes']['obitos4049m']
                    obitos_40_49_m = "" if missing_obitos and not obitos_40_49_m else obitos_40_49_m
                    obitos_50_59_f = entry['attributes']['obitos5059f']
                    obitos_50_59_f = "" if missing_obitos and not obitos_50_59_f else obitos_50_59_f
                    obitos_50_59_m = entry['attributes']['obitos5059m']
                    obitos_50_59_m = "" if missing_obitos and not obitos_50_59_m else obitos_50_59_m
                    obitos_60_69_f = entry['attributes']['obitos6069f']
                    obitos_60_69_f = "" if missing_obitos and not obitos_60_69_f else obitos_60_69_f
                    obitos_60_69_m = entry['attributes']['obitos6069m']
                    obitos_60_69_m = "" if missing_obitos and not obitos_60_69_m else obitos_60_69_m
                    obitos_70_79_f = entry['attributes']['obitos7079f']
                    obitos_70_79_f = "" if missing_obitos and not obitos_70_79_f else obitos_70_79_f
                    obitos_70_79_m =  entry['attributes']['obitos7079m']
                    obitos_70_79_m = "" if missing_obitos and not obitos_70_79_m else obitos_70_79_m
                    obitos_80_plus_f = entry['attributes']['obitos80f']
                    obitos_80_plus_f = "" if missing_obitos and not obitos_80_plus_f else obitos_80_plus_f
                    obitos_80_plus_m = entry['attributes']['obitos80m']
                    obitos_80_plus_m = "" if missing_obitos and not obitos_80_plus_m else obitos_80_plus_m

                    ativos = entry['attributes']['Activos']

                elif entry['attributes']['ARSNome'] == 'ARS Norte':
                   # ars_name = entry['attributes']['ARSNome'].lower()
                   # confirmados_ars[ars_name] = entry['attributes']['ConfirmadosAcumulado_ARS']
                   # obitos_ars[ars_name] = entry['attributes']['Obitos_ARS']
                    confirmados_arsnorte = entry['attributes']['ConfirmadosAcumulado']
                    obitos_arsnorte = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'ARS Centro':
                    confirmados_arscentro = entry['attributes']['ConfirmadosAcumulado']
                    obitos_arscentro = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'ARS Lisboa e Vale do Tejo':
                    confirmados_arslvt = entry['attributes']['ConfirmadosAcumulado']
                    obitos_arslvt = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'ARS Açores':
                    confirmados_acores = entry['attributes']['ConfirmadosAcumulado']
                    obitos_acores = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'ARS Madeira':
                    confirmados_madeira = entry['attributes']['ConfirmadosAcumulado']
                    obitos_madeira = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'Açores':
                    confirmados_acores = entry['attributes']['ConfirmadosAcumulado']
                    obitos_acores = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'Madeira':
                    confirmados_madeira = entry['attributes']['ConfirmadosAcumulado']
                    obitos_madeira = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'ARS Algarve':
                    confirmados_arsalgarve = entry['attributes']['ConfirmadosAcumulado']
                    obitos_arsalgarve = entry['attributes']['Obitos']

                elif entry['attributes']['ARSNome'] == 'ARS Alentejo':
                    confirmados_arsalentejo = entry['attributes']['ConfirmadosAcumulado']
                    obitos_arsalentejo = entry['attributes']['Obitos']

                # DADOS QUE DEIXARAM DE SER DISPONIBILIZADOS - agora já estão disponíveis (adicionar nos dados nacionais)
                confirmados_desconhecidos_f, confirmados_desconhecidos_m = "", ""
                n_confirmados = ""

                obitos_estrangeiro, recuperados_estrangeiro = "", ""

                recuperados_arsnorte, recuperados_arscentro, recuperados_arslvt, recuperados_arsalentejo, recuperados_arsalgarve = "", "", "", "", ""
                recuperados_acores, recuperados_madeira = "", ""

    if not found_date:
        frmt_date = datetime.datetime.utcfromtimestamp(latest_date).strftime("%d-%m-%Y")
        raise Exception(f"Missing date {today}, latest date {frmt_date}")

    # ORDENAR DADOS
    new_row = pd.DataFrame([[
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
    ]])

    # write to csv
    csv_path = str(Path(__file__).resolve().parents[2] / 'data.csv')
    new_row.to_csv(csv_path, mode='a', header=False, index=False, sep = ',')

