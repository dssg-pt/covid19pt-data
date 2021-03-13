import requests
import datetime
import pandas as pd
import numpy as np
from pathlib import Path


def get_new_data(url):
    """
    retrieve historic data for Activos (ativos) and InternadosEnfermaria (internados_enfermaria)
    """

    r = requests.get(url=url)
    data = r.json()
    new_data = []

    for entry in data['features']:
        if entry['attributes']['ARSNome'] == 'Nacional':
            unix_date = int(entry['attributes']['Data']/1000/86400)*86400
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date)

            #ativos = entry['attributes'].get('Activos', '')
            #internados_enfermaria = entry['attributes']['InternadosEnfermaria']
            ## derive from internados minus UCI until 18-08-2020, and 19-08-2020 with value 0
            #if not internados_enfermaria or internados_enfermaria == 0:
            #    internados = entry['attributes']['Internados']
            #    internados_uci = entry['attributes']['InternadosUCI']
            #    internados_enfermaria = internados - internados_uci

            confirmados = entry['attributes']['ConfirmadosAcumulado']
            confirmados_m = entry['attributes']['conftotalm']
            confirmados_f = entry['attributes']['conftotalf']

            confirmados_desconhecidos = confirmados - confirmados_m - confirmados_f

            new_data.append([
                frmt_date, #
                # ativos, internados_enfermaria,
                confirmados_desconhecidos,
            ])

    new_data_df = pd.DataFrame(data=new_data, columns=[
        'data', #
        # 'ativos', 'internados_enfermaria',
        'confirmados_desconhecidos',
    ])
    return new_data_df


def convert(x):
    if np.isnan(x):
        return ''
    try:
        return int(x)
    except:
        return x


if __name__ == '__main__':
    # Constants
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / 'data.csv')

    URL = (
        'https://services.arcgis.com/CCZiGSEQbAxxFVh3/ArcGIS/rest/services/COVID_Concelhos_DadosDiariosARS_VIEW2/FeatureServer/0/query'
        '?where=ConfirmadosAcumulado>=0&outFields=*&orderByFields=Data+desc&groupByFieldsForStatistics=&f=pjson'
    )
    # Get the data available in the dashboard
    new_data = get_new_data(URL)

    latest = pd.read_csv(PATH_TO_CSV)
    latest['data'] = pd.to_datetime(latest['data'], format='%d-%m-%Y')

    # drop incomplete 'ativos' columm
    #latest = latest.drop(columns='ativos')
    #if 'internados_enfermaria' in latest:
    #    latest = latest.drop(columns='internados_enfermaria')

    # merge
    updated = latest.merge(new_data, how='outer', on=['data'])
    # sort by date
    updated = updated.sort_values('data')
    # convert back into dd-mm-yyyy
    updated['data'] = updated['data'].dt.strftime('%d-%m-%Y')
    # convert numbers back to int (everything besides sintomas_* (float) and data* (dates))
    cols = [x for x in updated.columns if not x.startswith('sintomas') and not x.startswith('data')]
    updated[cols] = updated[cols].applymap(convert)

    # reorder columns
    # cols = list(updated.columns)
    # cols.remove('internados_enfermaria')
    # cols.insert(cols.index('internados') + 1, 'internados_enfermaria')
    # cols.remove('ativos')
    # cols.insert(cols.index('obitos') + 1, 'ativos')
    # updated = updated[cols]

    updated.to_csv(PATH_TO_CSV, index=False, line_terminator='\n')
