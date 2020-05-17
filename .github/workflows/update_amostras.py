import datetime
import requests
import pandas as pd
from pathlib import Path

def get_amostras(url):
    r = requests.get(url=url) 
    data = r.json()
    amostras = []
    
    for entry in data['features']:
        if entry['attributes']['Data_do_Relatório']:
            unix_date = entry['attributes']['Data_do_Relatório']/1000
            frmt_date = datetime.datetime.utcfromtimestamp(unix_date)
            amostras_total = entry['attributes']['Amostras']
            amostras_novas = entry['attributes']['Amostras_Novas']
            amostras.append([frmt_date, amostras_total, amostras_novas])
    
    amostras_df = pd.DataFrame(data=amostras, columns=['data', 'amostras', 'amostras_novas'])
    return amostras_df

if __name__ == '__main__':
    # Constants
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / 'amostras.csv')
    URL = "https://services.arcgis.com/CCZiGSEQbAxxFVh3/arcgis/rest/services/An%C3%A1lises_Extra_Covid_new/FeatureServer/0/query?f=json&Amostras_Novas&where=Confirmados%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Data_do_Relat%C3%B3rio%20desc&resultOffset=0&resultRecordCount=318&cacheHint=true"

    # Get the data available in the dashboard
    available = get_amostras(URL)

    # Get latest data
    latest = pd.read_csv(PATH_TO_CSV)
    latest['data'] = pd.to_datetime(latest['data'], format='%d-%m-%Y')

    # Find rows with differences
    merged = available.merge(latest, how='outer', on=['data'], suffixes=('_available', '_latest'))
    merged = merged.fillna('""')

    different_rows = merged[(merged.amostras_available != merged.amostras_latest) | 
                            (merged.amostras_novas_available != merged.amostras_novas_latest)]

    # Order by date
    different_rows = different_rows.sort_values(by='data')

    # Update values
    updated = latest.copy()

    for r, row in different_rows.iterrows():

        # existing row
        if (updated.data == row['data']).any(): 
            index = updated.index[updated['data'] == row['data']]
            updated.at[index, 'amostras'] = row['amostras_available']
            updated.at[index, 'amostras_novas'] = row['amostras_novas_available']
        
        # new row
        else: 
            tmp_df = pd.DataFrame([[row['data'], row['amostras_available'], row['amostras_novas_available']]], 
                                columns=updated.columns)
            updated = pd.concat([updated, tmp_df], ignore_index=True)

    # sort by date      
    updated = updated.sort_values('data')
    updated['data'] = updated['data'].dt.strftime('%d-%m-%Y')
    
    # save to .csv
    updated.to_csv(PATH_TO_CSV, index=False, line_terminator='\n')