from os import listdir
from os.path import isfile, join
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import re
import sys
from util import convert, convert_to_float, convert_to_int

if __name__ == "__main__":

  PATH_TO_ROOT = Path(__file__).resolve().parents[2]
  PATH_TO_CSV = PATH_TO_ROOT / "extra" / "vacinas" / "relatório"

  OFFSET = 0

  # Find out the latest dataset available under PATH_TO_CSV
  datasets = [f for f in listdir(PATH_TO_CSV) if isfile(join(PATH_TO_CSV, f)) and f.endswith(".csv") and "Dataset" in f]
  last_dataset = sorted(datasets)[-1 - OFFSET]
  print(f"Last dataset={last_dataset}")

  # read the "Semi-colon Separated Values"
  data = pd.read_csv(PATH_TO_CSV / last_dataset, sep=";", decimal=',')


  # Dataset 12 (maybe 11) dropped RECEIVED + DISTRIBUTED
  dataset12 = False
  for k in ['RECEIVED', 'DISTRIBUTED']:
    if k not in data.columns:
      data[k] = np.nan
      dataset12 = True

  # Until 2021-03-17 the first column was an unnamed numeric index
  if len(data.columns) == 19 and data.columns[0] != 'TYPE':
    data.drop(data.columns[0], axis=1, inplace=True)

  # rename columns
  #   'TYPE', 'DATE', 'YEAR', 'WEEK', 'REGION', 'AGEGROUP',
  #   'TOTAL_VAC_1', 'TOTAL_VAC_2', 'TOTAL_VAC_UNK', 'TOTAL',
  #   'CUMUL_VAC_1', 'CUMUL_VAC_2', 'CUMUL_VAC_UNK', 'CUMUL',
  #   'COVER_1_VAC', 'COVER', 'RECEIVED', 'DISTRIBUTED'
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
    'data', # 'ano', 'semana', # redundante
    'região', 'idades',
    'recebidas', 'distribuidas',
    'doses', 'doses_novas',
    'doses1', 'doses1_novas',
    'doses2', 'doses2_novas',
    'dosesunk', 'dosesunk_novas',
    'doses1_perc', 'doses2_perc',
  ]]

  # 2021-03-24 Dataset 6 contém ilhas mas tem datas inconsistentes, com continente
  # a dia 15, tal como a Madeira, mas Açores a 17 e região "outro" a 16
  # Isto corrige as 3 datas para 15, para ficar uma linha com dados consistentes
  FIX_DATA = {
    '16/03/2021': '15/03/2021',
    '17/03/2021': '15/03/2021',
  }
  data['data'] = data['data'].apply(lambda x: FIX_DATA.get(x, x))

  # "day" como timestamp, para ser usado como indice e para merge
  try:
    data['day'] = data['data'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
  except ValueError:
    # 2021-04-29 tem ano com 2 digitos "21"
    try:
      data['day'] = data['data'].apply(lambda x: datetime.strptime(x, '%d/%m/%y'))
    except ValueError:
      # relatório 12 (talvez 11) tem Y-M-D
      data['day'] = data['data'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
  data['data'] = data['data'].apply(lambda x: x.replace("/", "-"))

  # CSV tem data do inicio da semana enquanto o PDF tem data do final da semana
  data['day'] = data['day'].apply(lambda x: x + timedelta(days=7))
  data['data'] = data['day'].apply(lambda x: x.strftime('%d-%m-%Y'))

  data.sort_values(['day', 'tipo', 'idades', 'região'], inplace=True)

  # Calculate population from doses e percentagem
  data['populacao1'] = (data['doses1'] / data['doses1_perc']).apply(lambda x: x if np.isnan(x) else np.ceil(x))
  data['populacao2'] = (data['doses2'] / data['doses2_perc']).apply(lambda x: x if np.isnan(x) else np.ceil(x))

  # colunas tipo=general
  data_general = data[ data['tipo'] == 'GENERAL'][[
      'day', 'data',
      'recebidas', 'distribuidas',
      'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
      'dosesunk', 'dosesunk_novas',
      'doses1_perc', 'doses2_perc', 'populacao1', 'populacao2'
    ]]
  data_general.set_index('day', inplace=True)

  if dataset12:
    print(f"WARNING: dados receibidas/distribuidas em falta")
    data_general['recebidas'] = [
      651900, 830730, 1002999, 1186389, 1468929, 1713540, 1883850, 2344530, 2684460, 2983590,
      3400260, 4218420
    ]
    data_general['distribuidas'] = [
      571981, 718143, 933847, 1095103, 1264093, 1462079, 1753999, 1996561, 2360167, 2679813,
      3039329, 3581288
    ]

  # dicionario para alteração do nome de idades
  ages = dict([ ( k,
      re.sub('-', '_',
      re.sub(' ou mais', '+',
      re.sub(' anos', '',
      # 2021.05.10 tem age como "NA"/float.nan
      k.lower() if type(k) == str else 'na'
    ))) ) for k in data.idades.unique() ])

  # wide table de colunas por idade
  data_ages = data[ data['tipo'] == 'AGES'].pivot(index='day', columns='idades', values=[
      # 'data',
      'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
      'dosesunk', 'dosesunk_novas',
      'doses1_perc', 'doses2_perc', 'populacao1', 'populacao2'
    ])
  cols = list(map(lambda x: f"{x[0]}_{ages.get(x[1], x[1])}", data_ages.columns))
  data_ages.columns = cols
  # reordena
  cols = sorted(cols, key=lambda x: x.split('_')[-1] )
  data_ages = data_ages[cols]

  # dicionario para alteração do nome de regiões
  ars = dict([ (k,
      re.sub(' ', '',
      re.sub('lisboa e vale do tejo', 'lvt',
      re.sub('ra.madeira', 'madeira',
      re.sub('ra.a[cç]ores', 'açores',
      k.lower()
    )))) ) for k in data['região'].unique() ])

  # wide table de colunas por região
  cols_ars = [
    'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
    'dosesunk', 'dosesunk_novas',
    'doses1_perc', 'doses2_perc', 'populacao1', 'populacao2'
  ]
  data_regional = data[ data['tipo'] == 'REGIONAL'].pivot(index='day', columns='região', values=cols_ars)
  cols = list(map(lambda x: f"{x[0]}_{ars.get(x[1], x[1])}", data_regional.columns))
  data_regional.columns = cols

  # data_continente
  for col in cols_ars:
    data_regional[f'{col}_continente'] = (
      data_regional[f'{col}_arsnorte'] + 
      data_regional[f'{col}_arscentro'] + 
      data_regional[f'{col}_arslvt'] +
      data_regional[f'{col}_arsalentejo'] +
      data_regional[f'{col}_arsalgarve'] +
      0)
  cols = data_regional.columns

  # reordena por ARS (norte->sul)
  ARS_ORDER = {
    'continente': 0,
    'arsnorte': 1,
    'arscentro': 2,
    'arslvt': 3,
    'arsalentejo': 4,
    'arsalgarve': 5,
    'madeira': 6,
    'açores': 7,
    'outro': 8,
    'all': 9,
  }
  cols = sorted(cols, key=lambda x: ARS_ORDER[x.split('_')[-1]] )
  data_regional = data_regional[cols]

  # concatena tudo numa wiiiiiide table
  data_wide = pd.concat([data_general, data_regional, data_ages], axis=1)

  # limpa colunas vazias
  for col in [
      "doses1_perc_outro", "doses2_perc_outro",
      "populacao1_outro", "populacao2_outro",
      "doses1_perc_desconhecido", "doses2_perc_desconhecido",
      "populacao1_desconhecido", "populacao2_desconhecido",
    ]:
    if data_wide[col].sum() != 0:
      print(f"ERRO: Dados inesperados na coluna {col}")
      sys.exit(1)
    data_wide.drop(col, axis=1, inplace=True)

  # limpa dados - inteiros,
  #  e floats com 10 casas para prevenir inconsistencias entre plataformas 0.3(3)
  cols = [x for x in data_wide.columns if not x.startswith("data") and not 'perc' in x]
  data_wide = convert(data_wide, cols, convert_to_int)
  cols = [x for x in data_wide.columns if 'perc' in x]
  data_wide[cols] = data_wide[cols].apply(lambda x: round(x, 10))

  # recalcula a data, just in case
  data_wide['data'] = data_wide.index
  data_wide['data'] = data_wide['data'].apply(lambda x: x.strftime('%d-%m-%Y'))

  data_wide.to_csv(PATH_TO_ROOT / 'vacinas_detalhe.csv', index=False)
