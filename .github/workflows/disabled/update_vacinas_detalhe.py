from os import listdir
from os.path import isfile, join
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import re
import sys
from util import convert, convert_to_int


VACINAS_RECEBIDAS = [
  np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
  651900, 830730, 1002999, 1186389, 1468929, 1713540, 1883850, 2344530, 2684460, 2983590,
  3400260, 4128420, 4655370, 5197920, 5728470, 6254220, 7263540, 7880400, 8604606,
  9519240, 11510810, 12300690,
  12886770,
  13644850, 14398170,
  15322080,  # #27
  16675410,  # #28
  17448090,  # #29
  18136070,  # #30
  18507560,  # #31
  18507560,  # #32
  19507520,  # #33
  20258230,  # #34
  20414230,  # #35
  20836630,  # #36
  21400630,  # #37
  22153760,  # #38
  23017910,  # #39
  23017910,  # #40
]
VACINAS_DISTRIBUIDAS = [
  np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
  571981, 718143, 933847, 1095103, 1264093, 1462079, 1753999, 1996561, 2360167, 2679813,
  3039329, 3581288, 4171038, 4686071, 5126418, 5644760, 6299315, 6896272, 7566600,
  8357319, 10694447, 11385656,
  12043017,
  12597147, 13236664,
  14093439,  # #27
  14969971,  # #28
  15136630,  # #29
  15247675,  # #30
  15554044,  # #31
  15554044,  # #32
  15814437,  # #33
  16192139,  # #34
  16394069,  # #35
  16421977,  # #36
  16599465,  # #37
  16799210,  # #38
  16936974,  # #39
  17211348,  # #40
]


if __name__ == "__main__":
  # DEPRECATED
  print("DEPRECATED")
  sys.exit(1)


  PATH_TO_ROOT = Path(__file__).resolve().parents[2]
  PATH_TO_CSV = PATH_TO_ROOT / "extra" / "vacinas" / "relatório"

  OFFSET = 0

  if len(sys.argv) > 1:
    last_dataset = sys.argv[1]
  else:
    # Find out the latest dataset available under PATH_TO_CSV
    datasets = [f for f in listdir(PATH_TO_CSV) if isfile(join(PATH_TO_CSV, f)) and f.endswith(".csv") and "Dataset" in f]
    last_dataset = sorted(datasets)[-1 - OFFSET]
    print(f"Last dataset={last_dataset}")
    last_dataset = PATH_TO_CSV / last_dataset

  # read the "Semi-colon Separated Values"
  data = pd.read_csv(last_dataset, sep=";", decimal=',')

  # Dataset 12 (maybe 11) dropped RECEIVED + DISTRIBUTED
  dataset_num = None
  for k in ['RECEIVED', 'DISTRIBUTED']:
    if k not in data.columns:
      data[k] = np.nan
      if len(data.columns) in [18]:
        dataset_num = 12
      elif len(data.columns) in [24]:
        dataset_num = 24

  # Dataset 29 perdeu o COVER
  # ...;COVER_1_VAC;COVER;COVER_INIT;COVER_COMPLETE;COVER_LEAST
  # ...;COVER_1_VAC;COVER_INIT;COVER_COMPLETE;COVER_LEAST
  misses_cover = 'COVER_INIT' in data.columns and 'COVER' not in data.columns
  if misses_cover:
    data['COVER'] = np.nan

  # Until 2021-03-17 the first column was an unnamed numeric index
  # #20 2021-06-29 again
  if data.columns[0] != 'TYPE' and len(data.columns) in [19, 25]:
    data.drop(data.columns[0], axis=1, inplace=True)

  # rename columns
  #   'TYPE', 'DATE', 'YEAR', 'WEEK', 'REGION', 'AGEGROUP',
  #   'TOTAL_VAC_1', 'TOTAL_VAC_2', 'TOTAL_VAC_UNK', 'TOTAL',
  #   'CUMUL_VAC_1', 'CUMUL_VAC_2', 'CUMUL_VAC_UNK', 'CUMUL',
  # #20
  #   'CUMUL_VAC_INIT', 'CUMUL_VAC_COMPLETE', 'CUMUL_VAC_LEAST',
  #   'COVER_1_VAC', 'COVER',
  # #20
  #   'COVER_INIT', 'COVER_COMPLETE', 'COVER_LEAST',
  #   'RECEIVED', 'DISTRIBUTED'
  columns = [
    # [0:14]
    'tipo', 'data', 'ano', 'semana', 'região', 'idades',
    'doses1_novas', 'doses2_novas', 'dosesunk_novas', 'doses_novas',
    'doses1', 'doses2', 'dosesunk', 'doses',
    # [14:16]
    'doses1_perc', 'doses2_perc',
    # [16:]
    'recebidas', 'distribuidas',
  ]
  if len(data.columns) == 24:
    columns = (
      # ;TYPE;DATE;YEAR;WEEK;REGION;AGEGROUP;
      #'tipo', 'data', 'ano', 'semana', 'região', 'idades',
      # TOTAL_VAC_1;TOTAL_VAC_2;TOTAL_VAC_UNK;TOTAL;
      #'doses1_novas', 'doses2_novas', 'dosesunk_novas', 'doses_novas',
      # CUMUL_VAC_1;CUMUL_VAC_2;CUMUL_VAC_UNK;CUMUL;
      #'doses1', 'doses2', 'dosesunk', 'doses',
      columns[0:14] +
      [
        #   'CUMUL_VAC_INIT', 'CUMUL_VAC_COMPLETE', 'CUMUL_VAC_LEAST',
        'pessoas_vacinadas_parcialmente',
        'pessoas_vacinadas_completamente',
        'pessoas_inoculadas',
      ] +
      # COVER_1_VAC;
      #'doses1_perc', #' doses2_perc',
      ( columns[14:15] if misses_cover else columns[14:16] ) +
      [
        # 'COVER_INIT', 'COVER_COMPLETE', 'COVER_LEAST',
        'pessoas_vacinadas_parcialmente_perc',
        'pessoas_vacinadas_completamente_perc',
        'pessoas_inoculadas_perc',
      ] +
      # <gone>
      #'recebidas', 'distribuidas',
      columns[16:] +
      # missing COVER
      ( columns[15:16] if misses_cover else [] )
    )
  #print(columns)

  data.columns = columns
  # reorder columns
  data = data[[
    'tipo',
    'data', # 'ano', # redundante
    'semana',
    'região', 'idades',
    'recebidas', 'distribuidas',
    'doses', 'doses_novas',
    'doses1', 'doses1_novas',
    'doses2', 'doses2_novas',
    'dosesunk', 'dosesunk_novas',
    'doses1_perc', 'doses2_perc',
    'pessoas_vacinadas_parcialmente',
    'pessoas_vacinadas_completamente',
    'pessoas_inoculadas',
    'pessoas_vacinadas_parcialmente_perc',
    'pessoas_vacinadas_completamente_perc',
    'pessoas_inoculadas_perc',
  ]]

  # 2021-08-17 #27 linhas vazias ficam NaN
  data.dropna(how='all', inplace=True)

  # 2021-07-12 Datas todas misturadas
  # - 01/04/2021 -> 2021-01-04
  # - 18/01/21 -> 2021-01-18
  for i, row in data.iterrows():
    new_date = datetime(2021, 1, 4) + timedelta(days=7*(row.semana-1))
    # print(f"data={row.data} week={row.semana} new_date={new_date}")
    data.loc[i, 'data'] = new_date.strftime('%d/%m/%Y')

  # 2021-03-24 Dataset 6 contém ilhas mas tem datas inconsistentes, com continente
  # a dia 15, tal como a Madeira, mas Açores a 17 e região "outro" a 16
  # Isto corrige as 3 datas para 15, para ficar uma linha com dados consistentes
  FIX_DATA = {
    '16/03/2021': '15/03/2021',
    '17/03/2021': '15/03/2021',
  }
  data['data'] = data['data'].apply(lambda x: FIX_DATA.get(x, x))

  # percentagens como 0.xxx e 69% tudo misturado
  cols = [x for x in data.columns if 'perc' in x]
  data[cols] = data[cols].apply(lambda x: x.apply(lambda y: np.nan if '%' in str(y) else float(str(y).replace(',', '.'))))

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
  data['populacao1'] = (data['pessoas_inoculadas'] / data['pessoas_inoculadas_perc']).apply(lambda x: x if np.isnan(x) else np.ceil(x))
  data['populacao2'] = (data['doses1'] / data['doses1_perc']).apply(lambda x: x if np.isnan(x) else np.ceil(x))

  # colunas tipo=general
  data_general = data[ data['tipo'] == 'GENERAL'][[
      'day', 'data',
      'recebidas', 'distribuidas',
      'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
      'dosesunk', 'dosesunk_novas',
      'doses1_perc', 'doses2_perc',
      'pessoas_vacinadas_parcialmente',
      'pessoas_vacinadas_completamente',
      'pessoas_inoculadas',
      'pessoas_vacinadas_parcialmente_perc',
      'pessoas_vacinadas_completamente_perc',
      'pessoas_inoculadas_perc',
      'populacao1', 'populacao2'
    ]]
  data_general.set_index('day', inplace=True)

  if dataset_num == 12:
    data_general['recebidas'] = [
      651900, 830730, 1002999, 1186389, 1468929, 1713540, 1883850, 2344530, 2684460, 2983590,
      3400260, 4218420
    ]
    data_general['distribuidas'] = [
      571981, 718143, 933847, 1095103, 1264093, 1462079, 1753999, 1996561, 2360167, 2679813,
      3039329, 3581288
    ]
  elif dataset_num == 24:
    data_general['recebidas'] = VACINAS_RECEBIDAS
    data_general['distribuidas'] = VACINAS_DISTRIBUIDAS

  # dicionario para alteração do nome de idades
  ages = dict([ ( k,
      re.sub('-', '_',
      re.sub(' ou mais', '+',
      re.sub(' anos', '',
      # 2021.05.10 tem age como "NA"/float.nan
      k.lower() if type(k) == str else 'na' if np.isnan(k) else f'na_{k}'
    ))) ) for k in data.idades.unique() ])

  # wide table de colunas por idade
  data_ages = data[ data['tipo'] == 'AGES'].pivot(index='day', columns='idades', values=[
      # 'data',
      'doses', 'doses_novas', 'doses1', 'doses1_novas', 'doses2', 'doses2_novas',
      'dosesunk', 'dosesunk_novas', 'doses1_perc', 'doses2_perc',
      'pessoas_vacinadas_parcialmente',
      'pessoas_vacinadas_completamente',
      'pessoas_inoculadas',
      'pessoas_vacinadas_parcialmente_perc',
      'pessoas_vacinadas_completamente_perc',
      'pessoas_inoculadas_perc',
      'populacao1', 'populacao2'
    ])
  cols = list(map(lambda x: f"{x[0]}_{ages.get(x[1], x[1])}", data_ages.columns))
  data_ages.columns = cols
  # reordena
  cols = sorted(cols, key=lambda x: x.split('_')[-1] )
  data_ages = data_ages[cols]
  # relatório 25 tem percentagens como x% e 0.xx, que torna em 0,xx
  for i in ['pessoas_vacinadas_parcialmente',
      'pessoas_vacinadas_completamente',
      'pessoas_inoculadas',]:
      for _, age in ages.items():
          if age == 'all': continue
          # percentagem pode ser maior que 100% pois a população é INE 2019
          # (relatório já fala em 2020) mas estamos em 2021 e acontece nos
          # escalões 80+ e 70+
          data_ages[f'{i}_perc_{age}'] = data_ages[f'{i}_{age}'] / data_ages[f'populacao1_{age}']

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
    'dosesunk', 'dosesunk_novas', 'doses1_perc', 'doses2_perc',
    'pessoas_vacinadas_parcialmente',
    'pessoas_vacinadas_completamente',
    'pessoas_inoculadas',
    'pessoas_vacinadas_parcialmente_perc',
    'pessoas_vacinadas_completamente_perc',
    'pessoas_inoculadas_perc',
    'populacao1', 'populacao2'
  ]
  data_regional = data[ data['tipo'] == 'REGIONAL'].pivot(index='day', columns='região', values=cols_ars)
  cols = list(map(lambda x: f"{x[0]}_{ars.get(x[1], x[1])}", data_regional.columns))
  data_regional.columns = cols

  # data_continente
  for col in [x for x in cols_ars if '_perc' not in x]:
    data_regional[f'{col}_continente'] = (
      data_regional[f'{col}_arsnorte'] +
      data_regional[f'{col}_arscentro'] +
      data_regional[f'{col}_arslvt'] +
      data_regional[f'{col}_arsalentejo'] +
      data_regional[f'{col}_arsalgarve'] +
      0)
  # recalcula a percentagem continente
  for i in [1, 2]:
    data_regional[f'doses{i}_perc_continente'] = data_regional[f'doses{i}_continente'] / data_regional[f'populacao{i}_continente']
  for i in ['pessoas_vacinadas_parcialmente', 'pessoas_vacinadas_completamente', 'pessoas_inoculadas']:
    data_regional[f'{i}_perc_continente'] = data_regional[f'{i}_continente'] / data_regional[f'populacao1_continente']
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

  # relatório semanal #32 CSV em falta
  if False:
    row = [
          ['data', '20-09-2021'],
          ['recebidas', 18_885_800],
          ['distribuidas', 15_758_915],
          ['pessoas_inoculadas', 8_889_941],
          ['pessoas_vacinadas_completamente', 8_546_688],
          ['pessoas_vacinadas_parcialmente', 8_889_941 - 8_546_688],
          ['doses', (
              5_584_026 + # norte
              2_596_902 + # centro
              5_489_097 + # lvt
                735_227 + # alentejo
                659_736 + # algarve
                383_428 + # madeira
                360_641 + # açores
                      0
            )],
          # doses1, doses2
          ['doses_continente', (
              5_584_026 + # norte
              2_596_902 + # centro
              5_489_097 + # lvt
                735_227 + # alentejo
                659_736 + # algarve
                      0
            )],
          ['doses_arsnorte', 5_584_026], # norte
          ['doses_arscentro', 2_596_902], # centro
          ['doses_arslvt', 5_489_097], # lvt
          ['doses_arsalentejo', 735_227], # alentejo
          ['doses_arsalgarve', 659_736], # algarve
          ['doses_madeira', 383_428], # madeira
          ['doses_açores', 360_641], # açores

          ['pessoas_inoculadas_12_17', 538_752],
          ['pessoas_vacinadas_completamente_12_17', 449_089],
          ['pessoas_vacinadas_parcialmente_12_17', 538_752 - 449_089],
          ['pessoas_inoculadas_18_24', 695_284],
          ['pessoas_vacinadas_completamente_18_24', 635_419],
          ['pessoas_vacinadas_parcialmente_18_24', 695_284 - 635_419],
          ['pessoas_inoculadas_25_49', 3_123_998],
          ['pessoas_vacinadas_completamente_25_49', 2_992_594],
          ['pessoas_vacinadas_parcialmente_25_49', 3_123_998 - 2_992_594],
          ['pessoas_inoculadas_50_64', 2_156_022],
          ['pessoas_vacinadas_completamente_50_64', 2_118_649],
          ['pessoas_vacinadas_parcialmente_50_64', 2_156_022 - 2_118_649],
          ['pessoas_inoculadas_65_79', 1_681_600],
          ['pessoas_vacinadas_completamente_65_79', 1_662_956],
          ['pessoas_vacinadas_parcialmente_65_79', 1_681_600 - 1_662_956],
          ['pessoas_inoculadas_80+', 693_992],
          ['pessoas_vacinadas_completamente_80+', 687_935],
          ['pessoas_vacinadas_parcialmente_80+', 693_992 - 687_935],
      ]
    cols = list(map(lambda x: x[0], row))
    data = list(map(lambda x: x[1], row))
    row = pd.DataFrame([data], columns=cols)
    data_wide.loc[datetime(2021, 9, 20), cols] = data

  # limpa colunas vazias
  for col in [c for c in data_wide.columns if 'outro' in c]:
    if data_wide[col].sum() != 0:
      print(f"ERRO: Dados inesperados na coluna {col} - 0 != {data_wide[col].sum()}")
      sys.exit(1)
    #print(f"drop {col}")
    data_wide.drop(col, axis=1, inplace=True)

  # recalcula percentagens que vêm arredondadas e como string "xx%"
  for col in [col for col in data_wide.columns if "populacao" in col]:
    data_wide[col] = data_wide[col].ffill()
  for col in [col for col in data_wide.columns if "_perc" in col]:
    parts = col.split('_perc')
    key = parts[0]
    suffix = parts[1] if len(parts) > 1 else ''
    #print(f"col={col} key={key} suffix={suffix}")
    data_wide[col] = data_wide[key+suffix] / data_wide['populacao1'+suffix]

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
