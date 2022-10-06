import datetime
import pandas as pd
import numpy as np
from pathlib import Path

URL = "https://www.insa.min-saude.pt/wp-content/uploads/{year:04d}/{month:02d}/Rt_{region}.xlsx"

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
    PATH_TO_CSV = str(Path(__file__).resolve().parents[2] / "rt.csv")
    df = pd.read_csv(PATH_TO_CSV, parse_dates=[0], index_col=[0], infer_datetime_format=True)
    # Rename index column 'data' to 'Data'
    df.index.names = ["Data"]

    today = datetime.datetime.today()
    year, month = int(today.strftime("%Y")), int(today.strftime("%m"))
    diff = 0
    for region in REGIONS:
        try:
            url = URL.format(year=year, month=month, region=region[1])
            print(f"Retrieving {'last' if diff else 'this'} month {year}-{month} for {region}: {url}")
            data = pd.read_excel(url, index_col="Data")
        except Exception as e:
            print(f"Error {e}")
            try:
                (year, month) = (year - 1, 12) if month == 1 else (year, month-1)
                diff += 1
                url = URL.format(year=year, month=month, region=region[1])
                print(f"Retrieving last month {year}-{month} for {region}: {url}")
                data = pd.read_excel(url, index_col="Data")
            except Exception as e:
                print(f"Error2 {e}")
                print(f"Bad luck, region={region} is missing")
                continue

        # 'Rt_número_de_reprodução', 'limite_inferior_IC95%', 'limite_superior_IC95%']
        data.columns = [
            f"rt_{region[0]}",
            f"rt_95_inferior_{region[0]}",
            f"rt_95_superior_{region[0]}",
        ]
        df[data.columns] = data

    # end for regions

    # Rename index column 'Data' back to 'data'
    df.index.names = ["data"]

    # save to .csv
    df.to_csv(PATH_TO_CSV, index=True, line_terminator="\n")
