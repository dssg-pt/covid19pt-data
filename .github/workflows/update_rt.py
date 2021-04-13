import datetime
import requests
import pandas as pd
import numpy as np
import sys
import json
from pathlib import Path

URL = 'http://www.insa.min-saude.pt/wp-content/uploads/{year}/{month}/Rt_{region}.xlsx'

REGIONS = (
    ('nacional', 'nacional',),
    ('continente', 'Continente',),
    ('arsnorte', 'norte',),
    ('arscentro', 'centro', ),
    ('arslvt', 'lvt',),
    ('arsalentejo', 'Alentejo',),
    ('arsalgarve', 'Algarve',),
    ('açores', 'RAA',),
    ('madeira', 'RAM',),
)

if __name__ == "__main__":
    today = datetime.datetime.today()
    year, month = today.strftime("%Y"), today.strftime("%m")
    # TODO se o url der erro, testar o mês anterior
    df = None
    for region in REGIONS:
        url = URL.format(year=year, month=month, region=region[1])
        print(f"Retrieving {year}-{month} for {region}: {url}")
        data = pd.read_excel(url, index_col='Data')

        # 'Rt_número_de_reprodução', 'limite_inferior_IC95%', 'limite_superior_IC95%']
        data.columns = [f"rt_{region[0]}", f"rt_95_inferior_{region[0]}", f"rt_95_superior_{region[0]}"]
        if df is None:
          df = data
        else:
          df = pd.merge(df, data, how="outer", on=['Data'])
    
    # Rename index column 'Data' to 'data'
    df.index.names = ['data']
        
    # save to .csv
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "rt.csv")
    df.to_csv(PATH_TO_CSV, index=True, line_terminator="\n")
