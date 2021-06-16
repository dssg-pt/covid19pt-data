# Imports
from pathlib import Path
import pytest
import pandas as pd
import datetime
import csv
import numpy as np

# Constants
NULL_PLACEHOLDER_VALUE = "NOO"

# Tests fixture (.csv with DGS data)
@pytest.fixture(scope="module")
def data_amostras():
    """ Loads the CSV with the DGS data and applies some processing to it. """

    # Loading the CSV
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / ".." / "amostras.csv"
    data = pd.read_csv(
        csv_filepath,
        parse_dates=[0],
        infer_datetime_format=True,
        skip_blank_lines=False,
    )

    # Filling NaNs with a custom value for easier processing
    data.fillna(value=NULL_PLACEHOLDER_VALUE, inplace=True)

    # Returning
    return data


def _check_column_with_empty(val):
    """ Guarantees columns with empty values are as expeceted. """

    # Let's check if it's a float
    if isinstance(val, float):

        # Is it a float representing an integer value?
        return val.is_integer()

    # If it's a string, it must be equal to the expeceted string
    elif isinstance(val, str):
        return val == NULL_PLACEHOLDER_VALUE

    # Anything else, it's wrong
    else:
        return False


def _check_datetime_format(date):

    # Let's guarantee it makes sense (data starts on 26th February 2020)
    if date >= datetime.date(2020, 2, 26):

        # Let's guarantee it's in the correct format
        datetime.datetime.strptime(str(date), "%d-%m-%Y")  # Will fail if not
    else:
        return False


def test_date():

    # TODO: Optimize this.
    # Loading the CSV
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / ".." / "amostras.csv"
    data = pd.read_csv(csv_filepath)

    # Data de publicação
    data_dados = data["data"]
    # Data a que se referem os dados

    data_dados.apply(lambda x: datetime.datetime.strptime(x, "%d-%m-%Y"))


@pytest.mark.parametrize(
    "col_name, expected_dtype, int_check, extra_check",
    [
        ("amostras", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("amostras_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("amostras_pcr", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("amostras_pcr_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("amostras_antigenio", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("amostras_antigenio_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
    ],
)
def test_dtype(data_amostras, col_name, expected_dtype, int_check, extra_check):
    """
    Tests whether a certain column has the expected data types (and other column specific rules).
    """

    for i, row in data_amostras.iterrows():
        # skip NaN for 26-02..29-02
        if i < 4:
            continue
        val = row[col_name]

        # Basic type assertion (panda always load as float)
        assert isinstance(
            val, expected_dtype
        ), "Dia {}: erro na coluna {}, valor {}".format(row["data"], col_name, val)

        # Check it's an integer (even if represented like float)
        if int_check is not None:
            assert int_check(
                val
            ), "Dia: Coluna {}, valor {} não cumpre as condições específicas: int".format(
                row["data"], col_name, val
            )

        # Extra verification
        if extra_check is not None:
            assert extra_check(
                val
            ), "Dia: Coluna {}, valor {} não cumpre as condições específicas: extra".format(
                row["data"], col_name, val
            )


def test_delimiter_comma():
    """
    Tests that the delimiter is a comma
    """
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / ".." / "amostras.csv"
    with open(csv_filepath, newline="") as csvfile:
        csv.Sniffer().sniff(csvfile.read(1024), delimiters=",")


def test_blank_lines(data_amostras):
    """
    Tests if the last row is blank
    """
    df_latest_line = data_amostras.tail(1)  # Only run for the latest line
    for row in df_latest_line.iterrows():
        val = row[1]

    assert val["data"] != np.nan, "Empty row"


def test_sequentiality_new_cases(data_amostras):
    """
    Tests if the number of new cases is correct
    """

    for i, row in data_amostras.iterrows():
        # skip NaN for 26-02..29-02, plus the first real value
        if i < 5:
            continue
        today = data_amostras.iloc[i]
        yesterday = data_amostras.iloc[i - 1]

        for k in ["", "_pcr", "_antigenio"]:
            assert (
                today[f"amostras{k}_novas"] >= 0
            ), "Amostras{}_novas do dia {} NEGATIVAS".format(
                k,
                row["data"],
            )

        assert (
            today[f"amostras"] == today[f"amostras_pcr"] + today[f"amostras_antigenio"]
        ), "Amostras do dia {} não coerentes total={} soma={} pcr={} antigenio={}".format(
            row["data"],
            today[f"amostras"],
            today[f"amostras_pcr"] + today[f"amostras_antigenio"],
            today[f"amostras_pcr"],
            today[f"amostras_antigenio"],
        )

        for k in ["", "_pcr", "_antigenio"]:
            assert (
                today[f"amostras{k}"]
                == yesterday[f"amostras{k}"] + today[f"amostras{k}_novas"]
            ), "Amostras{} do dia {} não coerentes com dia anterior today={} yesterday={} novas={} expected={}".format(
                k,
                row["data"],
                today[f"amostras{k}"],
                yesterday[f"amostras{k}"],
                today[f"amostras{k}_novas"],
                today[f"amostras{k}"] - yesterday[f"amostras{k}"],
            )


def test_sequentiality_dates(data_amostras):
    """
    Tests if the sequentiality of dates is correct
    """

    for i, row in data_amostras.iterrows():
        # skip NaN for 26-02..29-02, plus the first real value
        if i < 5:
            continue
        today_date = data_amostras.iloc[i]["data"]
        yesterday_date = data_amostras.iloc[i - 1]["data"]
        diff_date = (today_date - yesterday_date).days

        assert diff_date == 1
