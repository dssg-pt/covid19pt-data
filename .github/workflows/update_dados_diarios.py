#!env python3

import datetime
import pandas as pd
import numpy as np
import sys
from pathlib import Path


if __name__ == "__main__":

    ROOT = Path(__file__).resolve().parents[2]
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = str(ROOT / 'dados_diarios/covid_dados_2022-05-24.xlsx')

    data = pd.ExcelFile(url)
    data = data.parse(data.sheet_names[1], index_col='confirmation_date1')
    data.index.name = 'data'
    data = data.replace(np.nan, 0)
    data.columns = ['confirmados_novos', 'obitos_novos']
    data['confirmados'] = data['confirmados_novos'].cumsum()
    data['obitos'] = data['obitos_novos'].cumsum()

    data = data.applymap(lambda x: int(x))
    data = data[[data.columns[2], data.columns[0], data.columns[3], data.columns[1]]]

    #print(data.tail(2))
    data.to_csv(ROOT / 'dados_diarios.csv', sep=",")


