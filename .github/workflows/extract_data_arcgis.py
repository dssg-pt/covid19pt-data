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
    today = str(datetime.date.today().strftime("%d-%m-%Y"))

    # Get data at a national level
    dados_nacionais = get_national_data()

    # Get ARS data
    confirmados_ars, obitos_ars = get_ars_data()

    # Order data for .csv
    # ORDENAR DADOS
    new_row = pd.DataFrame([[
        today,
        "{} 00:00".format(today),
        dados_nacionais['confirmados'],
        confirmados_ars['ars norte'],
        confirmados_ars['ars centro'],
        confirmados_ars['ars lisboa e vale do tejo'],
        confirmados_ars['ars alentejo'],
        confirmados_ars['ars algarve'],
        confirmados_ars['ars açores'],
        confirmados_ars['ars madeira'],
        dados_nacionais['confirmados_estrangeiro'],
        dados_nacionais['confirmados_novos'],
        dados_nacionais['recuperados'],
        dados_nacionais['obitos'],
        dados_nacionais['internados'],
        dados_nacionais['internados_uci'],
        dados_nacionais['lab'],
        dados_nacionais['suspeitos'],
        dados_nacionais['vigilancia'],
        "", #n_confirmados,
        dados_nacionais['cadeias_transmissao'],
        dados_nacionais['transmissao_importada'],
        "", #confirmados_0_9_f
        "", #confirmados_0_9_m,
        "", #confirmados_10_19_f,
        "", #confirmados_10_19_m,
        "", #confirmados_20_29_f,
        "", #confirmados_20_29_m,
        "", #confirmados_30_39_f,
        "", #confirmados_30_39_m,
        "", #confirmados_40_49_f,
        "", #confirmados_40_49_m,
        "", #confirmados_50_59_f,
        "", #confirmados_50_59_m,
        "", #confirmados_60_69_f,
        "", #confirmados_60_69_m,
        "", #confirmados_70_79_f,
        "", #confirmados_70_79_m,
        "", #confirmados_80_plus_f,
        "", #confirmados_80_plus_m,
        dados_nacionais['sintomas_tosse'],
        dados_nacionais['sintomas_febre'],
        dados_nacionais['sintomas_dificuldade_respiratoria'],
        dados_nacionais['sintomas_cefaleia'],
        dados_nacionais['sintomas_dores_musculares'],
        dados_nacionais['sintomas_fraqueza_generalizada'],
        dados_nacionais['confirmados_f'],
        dados_nacionais['confirmados_m'],
        obitos_ars['ars norte'],
        obitos_ars['ars centro'],
        obitos_ars['ars lisboa e vale do tejo'],
        obitos_ars['ars alentejo'],
        obitos_ars['ars algarve'],
        obitos_ars['ars açores'],
        obitos_ars['ars madeira'],
        "", #obitos_estrangeiro,
        "", #recuperados_arsnorte,
        "", #recuperados_arscentro,
        "", #recuperados_arslvt,
        "", #recuperados_arsalentejo,
        "", #recuperados_arsalgarve,
        "", #recuperados_acores,
        "", #recuperados_madeira,
        "", #recuperados_estrangeiro,
        "", #obitos_0_9_f,
        "", #obitos_0_9_m,
        "", #obitos_10_19_f,
        "", #obitos_10_19_m,
        "", #obitos_20_29_f,
        "", #obitos_20_29_m,
        "", #obitos_30_39_f,
        "", #obitos_30_39_m,
        "", #obitos_40_49_f,
        "", #obitos_40_49_m,
        "", #obitos_50_59_f,
        "", #obitos_50_59_m,
        "", #obitos_60_69_f,
        "", #obitos_60_69_m,
        "", #obitos_70_79_f,
        "", #obitos_70_79_m,
        "", #obitos_80_plus_f,
        "", #obitos_80_plus_m,
        "", #obitos_f,
        "", #obitos_m,
        "", #confirmados_desconhecidos_m,
        "", #confirmados_desconhecidos_f,
        dados_nacionais['ativos'],
        dados_nacionais['obitos_novos'],
        dados_nacionais['recuperados_novos'],
        dados_nacionais['confirmados_0_9'],
        dados_nacionais['confirmados_10_19'],
        dados_nacionais['confirmados_20_29'],
        dados_nacionais['confirmados_30_39'],
        dados_nacionais['confirmados_40_49'],
        dados_nacionais['confirmados_50_59'],
        dados_nacionais['confirmados_60_69'],
        dados_nacionais['confirmados_70_79'],
        dados_nacionais['confirmados_80_89'],
        dados_nacionais['confirmados_90_99']
    ]])

    # write to csv
    csv_path = str(Path(__file__).resolve().parents[2] / 'data.csv')
    new_row.to_csv(csv_path, mode='a', header=False, index=False, sep = ',')

    