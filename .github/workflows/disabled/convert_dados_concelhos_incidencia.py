import requests
import pandas as pd
import datetime
import numpy as np
from pathlib import Path
from util import convert, convert_to_float, convert_to_int


if __name__ == "__main__":
    # Constants
    CWD = Path(__file__).resolve().parents[2]

    DATA_CONCELHOS_CSV = str(CWD / "data_concelhos.csv")
    POPULATION_CSV = str(
        CWD / "extra" / "populacional" / "PORDATA_Estimativas-a-31-12_concelhos.csv"
    )

    DATA_CONCELHOS_14DIAS_CSV = str(CWD / "data_concelhos_14dias.csv")
    DATA_CONCELHOS_INCIDENCIA_CSV = str(CWD / "data_concelhos_incidencia.csv")

    population = pd.read_csv(POPULATION_CSV)
    # rename to Concelho and upper case values
    population["Concelho"] = population["Anos"].str.upper()

    data = pd.read_csv(DATA_CONCELHOS_CSV)
    # convert date string to proper date
    data["data"] = pd.to_datetime(data["data"], dayfirst=True)

    # Only data since it's weekly
    data = data[data["data"] >= "2020-07-14"]

    for i in [DATA_CONCELHOS_14DIAS_CSV, DATA_CONCELHOS_INCIDENCIA_CSV]:
        updated = data.copy()

        if i == DATA_CONCELHOS_INCIDENCIA_CSV:

            updated = updated.melt(
                id_vars=["data"], var_name="Concelho", value_name="Casos"
            )
            updated = updated.merge(
                population[["Concelho", "2019"]],
                how="left",
                left_on="Concelho",
                right_on="Concelho",
            )
            updated.fillna(0, inplace=True)
            updated["ratio"] = round(updated["Casos"] * 100 * 1000 / updated["2019"], 1)
            updated = updated.pivot_table(
                values="ratio", index="data", columns="Concelho"
            )

            updated = updated.reset_index(level=0)

        cols = [x for x in updated.columns if x != "data"]
        updated[cols] = updated[cols].diff(2)  # 14 days
        updated = updated[2:]
        func = convert_to_int if i == DATA_CONCELHOS_14DIAS_CSV else convert_to_float
        updated = convert(updated, cols, func)

        # sort by date
        updated = updated.sort_values("data")
        # convert back into dd-mm-yyyy
        updated["data"] = updated["data"].dt.strftime("%d-%m-%Y")

        updated.to_csv(i, index=False, line_terminator="\n")
