import requests
import pandas as pd
import datetime
import numpy as np
from pathlib import Path


def get_list_municipalities():
    resultOffset = 0
    resultRecordCount = 200

    url_concelhos = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_Concelhos_V/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&cacheHint=true&resultOffset={}&resultRecordCount={}'.format(resultOffset, resultRecordCount)
    data = requests.get(url_concelhos)
    data = data.json()

    concelhos = []

    while len(data['features']) != 0:
        for entry in data['features']:
            concelho = entry['attributes']['Concelho']
            concelhos.append(concelho)

        resultOffset+=200
        resultRecordCount+=200
        url_concelhos = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_Concelhos_V/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&cacheHint=true&resultOffset={}&resultRecordCount={}'.format(resultOffset, resultRecordCount)
        data = requests.get(url_concelhos)
        data = data.json()
    
    concelhos_df = pd.DataFrame(data=concelhos, columns=['concelho'])
    
    return concelhos_df

skip_dates = [
    # On Sunday 05-07-2020 data was frozen:
    # "ESTE RELATÓRIO DE SITUAÇÃO NÃO INCLUI A ATUALIZAÇÃO DA IMPUTAÇÃO DE CASOS
    # AOS CONCELHOS. A DGS ESTÁ A REALIZAR A VERIFICAÇÃO DE TODOS OS DADOS COM
    # AS AUTORIDADES LOCAIS E REGIONAIS DE SAÚDE QUE FICARÁ CONCLUÍDA DURANTE OS
    # PRÓXIMOS DIAS.
    # Data unfroze on Tuesday 14-07-2020, and then it's updated only on Mondays.
    # This keeps Monday 06-07 and 13-07 for consistency, and ignore the duplicate
    # data until Sunday 16-08
    '07-07-2020', '08-07-2020', '09-07-2020', '10-07-2020', '11-07-2020', '12-07-2020',
    '15-07-2020', '16-07-2020', '17-07-2020', '18-07-2020', '19-07-2020',
    '21-07-2020', '22-07-2020', '23-07-2020', '24-07-2020', '25-07-2020', '26-07-2020',
    '28-07-2020', '29-07-2020', '30-07-2020', '31-07-2020', '01-08-2020', '02-08-2020',
    '04-08-2020', '05-08-2020', '06-08-2020', '07-08-2020', '08-08-2020', '09-08-2020',
    '11-08-2020', '12-08-2020', '13-08-2020', '14-08-2020', '15-08-2020', '16-08-2020',
]

def get_list_cases_long():
    
    resultOffset = 0
    resultRecordCount = 1000

    URL = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_ConcelhosDiarios/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Data%20DESC&cacheHint=true&resultOffset=' + str(resultOffset) + '&resultRecordCount=' + str(resultRecordCount)
    data = requests.get(URL)
    data = data.json()

    casos=[]
    while len(data['features']) != 0:

        for entry in data['features']:
            unix_date = entry['attributes']['Data']/1000
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date).strftime("%d-%m-%Y")
            if frmt_date in skip_dates: continue
            confirmados_acumulado = entry['attributes']['ConfirmadosAcumulado']
            confirmados_concelho = entry['attributes']['Concelho']
            casos.append([frmt_date, confirmados_concelho, confirmados_acumulado])

        resultOffset+=1000
        resultRecordCount+=1000

        URL = 'https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/COVID19_ConcelhosDiarios/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Data%20DESC&cacheHint=true&resultOffset=' + str(resultOffset) + '&resultRecordCount=' + str(resultRecordCount)
        data = requests.get(URL)
        data = data.json()

    casos_df = pd.DataFrame(data=casos, columns=['data', 'concelho', 'confirmados'])
    
    return casos_df


def patch_concelhos(concelhos):
    
    fix1 = concelhos.data=='16-05-2020'
    concelhos.loc[fix1, 'SANTO TIRSO'] = 378
    concelhos.loc[fix1, 'SÃO BRÁS DE ALPORTEL'] = 3

    # is 157 on 09 and 11
    fix2 = concelhos.data=='10-08-2020'
    concelhos.loc[fix2, 'REGUENGOS DE MONSARAZ'] = 157

    return concelhos    

if __name__ == '__main__':

    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / 'data_concelhos.csv')

    # Get list of municipalities
    concelhos_df = get_list_municipalities()

    # Get list of cases
    casos_df = get_list_cases_long()

    # Merge list of cases with list of municipalities
    casos_df = concelhos_df.merge(casos_df, how='left', on='concelho')
    casos_df.confirmados[casos_df.data.isna()] = -1 # Helper for pivot table
    casos_df.data[casos_df.data.isna()] = '24-03-2020' # Helper for pivot table
    casos_df = casos_df.sort_values(by=['concelho'])

    # Convert long table to wide table
    casos_wide = pd.pivot_table(casos_df, values='confirmados', index='data', columns = 'concelho').reset_index()
    casos_wide.data = pd.to_datetime(casos_wide.data, format='%d-%m-%Y')
    casos_wide = casos_wide.sort_values(by='data').reset_index(drop=True)
    casos_wide = casos_wide.replace(-1, np.nan)
    
    casos_wide.data = casos_wide['data'].dt.strftime('%d-%m-%Y')
    
    casos_wide = patch_concelhos(casos_wide)

    casos_wide.to_csv(PATH_TO_CSV, index=False, sep = ',') 
