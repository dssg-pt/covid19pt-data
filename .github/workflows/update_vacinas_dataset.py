from os import listdir
from os.path import isfile, join
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import re
from util import convert, convert_to_float, convert_to_int

if __name__ == "__main__":

  PATH_TO_ROOT = Path(__file__).resolve().parents[2]
  PATH_TO_CSV = PATH_TO_ROOT / "extra" / "vacinas"

  # Find out the latest dataset available
  datasets = [f for f in listdir(PATH_TO_CSV) if isfile(join(PATH_TO_CSV, f)) and f.endswith(".csv") and "Dataset" in f]
  last_dataset = sorted(datasets)[-1]
  print(f"Last dataset={last_dataset}")

  # read the "semi-colon separated values"
  data = pd.read_csv(PATH_TO_CSV / last_dataset, sep=";", index_col=0, decimal=',')

  # rename columns
  #   'TYPE', 'DATE', 'YEAR', 'WEEK', 'REGION', 'AGEGROUP',
  #   'TOTAL_VAC_1', 'TOTAL_VAC_2', 'TOTAL_VAC_UNK', 'TOTAL',
  #   'CUMUL_VAC_1', 'CUMUL_VAC_2', 'CUMUL_VAC_UNK', 'CUMUL',
  #   'COVER_1_VAC', 'COVER', 'RECEIVED', 'DISTRIBUTED']
  data.columns = [
    'tipo',
    'data', 'ano', 'semana',
    'região', 'idades',
    'doses1_novas', 'doses2_novas', 'dosesunk_novas', 'doses_novas',
    'doses1', 'doses2', 'dosesunk', 'doses',
    'doses1_perc', 'doses2_perc',
    'recebidas', 'distribuidas',
  ]
  # reorder columns
  data = data[[
    'tipo',
    'data', # 'ano', 'semana',
    'região', 'idades',
    'recebidas', 'distribuidas',
    'doses', 'doses_novas',
    'doses1', 'doses1_novas',
    'doses2', 'doses2_novas',
    'dosesunk', 'dosesunk_novas',
    'doses1_perc', 'doses2_perc',
  ]]
  data['day'] = data['data'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
  data['data'] = data['data'].apply(lambda x: x.replace("/", "-"))
  data.sort_values(['day', 'tipo', 'idades', 'região'], inplace=True)

  # Calculate population
  data['populacao1'] = (data['doses1'] / data['doses1_perc']).apply(lambda x: x if np.isnan(x) else np.ceil(x))
  data['populacao2'] = (data['doses2'] / data['doses2_perc']).apply(lambda x: x if np.isnan(x) else np.ceil(x))

  # colunas general
  data_general = data[ data['tipo'] == 'GENERAL'][[
      'day', 'data', # 'ano', 'semana',
      'recebidas', 'distribuidas',
      'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
      'dosesunk', 'dosesunk_novas',
      'doses1_perc', 'doses2_perc', 'populacao1', 'populacao2'
    ]]
  data_general.set_index('day', inplace=True)

  # dicionario alteração valores de idades
  ages = dict([ ( age, re.sub('-', '_', re.sub(' ou mais', '+', re.sub(' anos', '', age))) ) for age in data.idades.unique() ])

  # colunas por idade
  data_ages = data[ data['tipo'] == 'AGES'].pivot(index='day', columns='idades', values=[
      'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
      'dosesunk', 'dosesunk_novas',
      'doses1_perc', 'doses2_perc', 'populacao1', 'populacao2'
    ])
  cols = list(map(lambda x: f"{x[0]}_{ages.get(x[1], x[1])}", data_ages.columns))
  data_ages.columns = cols
  cols = sorted(cols, key=lambda x: x.split('_')[-1] )
  data_ages = data_ages[cols]

  # dicionario alteração valores de regiões
  ars = dict([ (k, re.sub(' ', '', re.sub('lisboa e vale do tejo', 'lvt', k.lower())) ) for k in data['região'].unique() ])

  # colunas por região
  data_regional = data[ data['tipo'] == 'REGIONAL'].pivot(index='day', columns='região', values=[
      'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
      'dosesunk', 'dosesunk_novas',
      'doses1_perc', 'doses2_perc', 'populacao1', 'populacao2'
    ])
  cols = list(map(lambda x: f"{x[0]}_{ars.get(x[1], x[1])}", data_regional.columns))
  data_regional.columns = cols
  # ARS order
  ARS_ORDER = {
    'arsnorte': 1,
    'arscentro': 2,
    'arslvt': 3,
    'arsalentejo': 4,
    'arsalgarve': 5,
    'outro': 8,
    'all': 9,
  }
  cols = sorted(cols, key=lambda x: ARS_ORDER[x.split('_')[-1]] )
  data_regional = data_regional[cols]

  # concatena tudo
  data_wide = pd.concat([data_general, data_ages, data_regional], axis=1)
  cols = [x for x in data_wide.columns if not x.startswith("data") and not 'perc' in x]
  data_wide = convert(data_wide, cols, convert_to_int)
  cols = [x for x in data_wide.columns if 'perc' in x]
  data_wide[cols] = data_wide[cols].apply(lambda x: round(x, 10))
  
  data_wide.to_csv(PATH_TO_ROOT / 'vacinas_dataset.csv', index=False)
