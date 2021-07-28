import datetime
import pandas as pd
import numpy as np
from pathlib import Path

URL = "http://www.insa.min-saude.pt/wp-content/uploads/{year:04d}/{month:02d}/Rt_{region}.xlsx"

REGIONS = (
    ("nacional", "nacional", ),
    ("continente", "Continente", ),
    ("arsnorte", "norte", ),
    ("arscentro", "centro", ),
    ("arslvt", "lvt", ),
    ("arsalentejo", "Alentejo", ),
    ("arsalgarve", "Algarve", ),
    ("açores", "RAA", ),
    ("madeira", "RAM",),
)

if __name__ == "__main__":
    today = datetime.datetime.today()
    year, month = int(today.strftime("%Y")), int(today.strftime("%m"))
    diff = 0
    df = None
    for region in REGIONS:
        try:
            url = URL.format(year=year, month=month, region=region[1])
            print(f"Retrieving {'last' if diff else 'this'} month {year}-{month} for {region}: {url}")
            data = pd.read_excel(url, index_col="Data")
        except:
            (year, month) = (year - 1, 12) if month == 1 else (year, month-1)
            diff += 1
            url = URL.format(year=year, month=month, region=region[1])
            print(f"Retrieving last month {year}-{month} for {region}: {url}")
            data = pd.read_excel(url, index_col="Data")

        # 'Rt_número_de_reprodução', 'limite_inferior_IC95%', 'limite_superior_IC95%']
        data.columns = [
            f"rt_{region[0]}",
            f"rt_95_inferior_{region[0]}",
            f"rt_95_superior_{region[0]}",
        ]
        if df is None:
            df = data
        else:
            df = pd.merge(df, data, how="outer", on=["Data"])

    # Rename index column 'Data' to 'data'
    df.index.names = ["data"]

    # save to .csv
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "rt.csv")
    df.to_csv(PATH_TO_CSV, index=True, line_terminator="\n")
