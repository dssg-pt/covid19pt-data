import pandas as pd
import numpy as np
from pathlib import Path
import sys

# same as notebooks/clean_concelhos_new.ipynb

# DATA_NEW_FILEPATH = Path.cwd() / '..'  / 'data_concelhos_new.csv'
DATA_NEW_FILEPATH = Path(__file__).resolve().parents[2] / 'data_concelhos_new.csv'
df = pd.read_csv(DATA_NEW_FILEPATH) # , parse_dates=[0], index_col=[0], infer_datetime_format=True)

# -----
cols = list(df.columns)
cols = cols[cols.index("ars"):]

# len(cols), cols[0], cols[-1]#

# -----
concelhos = list(df.concelho.unique())

# len(concelhos), concelhos[0], concelhos[-1]

# -----
meta = {}
for i, row in df.iterrows():
    concelho = row.concelho
    if concelho not in meta: meta[concelho] = {}
    meta_concelho = meta[concelho]
    for col in cols:
        val = row[col]
        if type(val) == float and np.isnan(val): continue
        if col not in meta_concelho: meta_concelho[col] = val
        elif meta_concelho[col] != val:
            print(f"ERRO {concelho} {col} {val} {meta_concelho[col]}")
            sys.exit(1)

# meta

# -----
#for concelho, row in meta.items():
#    for col, val in row.items():
#        df[col][df.concelho == concelho] = val
for i, row in df.iterrows():
    for col in cols:
        df[col][i] = meta[row.concelho][col]

# df

# -----
# df[["concelho", "confirmados_14", "casos_14dias"]][~(df["casos_14dias"].isna())]
for i, row in df.iterrows():
    if np.isnan(row.casos_14dias):
        df.loc[i, "casos_14dias"] = row.confirmados_14
        continue
    if abs(row.casos_14dias - row.confirmados_14) > 2:
        print(f"FAIL {i} {row.concelho} {row.casos_14dias} {row.confirmados_14}")
        sys.exit(1)

# df.loc[:, ['concelho', 'confirmados_14', 'casos_14dias']]

# -----
df.incidencia_categoria.unique()
df.incidencia_categoria.loc[df.incidencia_categoria == "[0,20)"] = "[0,20]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[0,20}"] = "[0,20]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[0,204]"] = "[0,240]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[0,240)"] = "[0,240]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[20,60)"] = "[20,60]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[60,120)"] = "[60,120]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[120,240)"] = "[120,240]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[240,480)"] = "[240,480]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[480,960)"] = "[480,960]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[960, Max)"] = "[960,Max]"
df.incidencia_categoria.loc[df.incidencia_categoria == "[960, Max]"] = "[960,Max]"
df.incidencia_categoria.loc[df.incidencia_categoria == "Abaixo de 20,0"] = "[0,20]"
df.incidencia_categoria.loc[df.incidencia_categoria == "Entre 20,0 e 59,9"] = "[20,60]"
df.incidencia_categoria.loc[df.incidencia_categoria == "Entre 60,0 e 119,9"] = "[60,120]"
df.incidencia_categoria.loc[df.incidencia_categoria == "Entre 120,0 e 239,9"] = "[120,240]"
df.incidencia_categoria.loc[df.incidencia_categoria == "Acima de 240,0"] = "[240,Max]"
df.incidencia_categoria.loc[df.incidencia_categoria == "Acima de 240,0 "] = "[240,Max]"

# sorted(df.incidencia_categoria.unique())

# -----
cols_int = [x for x in df.columns if x.startswith("population")]
cols_int += ["casos_14dias", "dicofre"]
cols_int += ["confirmados_14", "confirmados_1", "incidencia"]
df[cols_int] = df[cols_int].applymap(lambda x: int(x))

df[["dicofre"]] = df[["dicofre"]].applymap(lambda x: f"0{x}" if x < 1000 else x)

# -----

# DATA_NEW_FILEPATH_OUT = Path.cwd() / '..' / 'data_concelhos_new_out.csv'
# DATA_NEW_FILEPATH_OUT = Path(__file__).resolve().parents[2] / 'data_concelhos_new_out.csv'
DATA_NEW_FILEPATH_OUT = Path.cwd() / '..' / 'data_concelhos_new.csv'
DATA_NEW_FILEPATH_OUT = Path(__file__).resolve().parents[2] / 'data_concelhos_new.csv'
df.to_csv(DATA_NEW_FILEPATH_OUT, index=False, sep=",")
