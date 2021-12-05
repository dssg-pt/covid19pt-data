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
def data_vacinas():
    """ Loads the CSV with the DGS data and applies some processing to it. """

    # Loading the CSV
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / ".." / "vacinas.csv"
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
    csv_filepath = current_dir / ".." / "vacinas.csv"
    data = pd.read_csv(csv_filepath)

    # Data de publicação
    data_dados = data["data"]
    # Data a que se referem os dados

    data_dados.apply(lambda x: datetime.datetime.strptime(x, "%d-%m-%Y"))


@pytest.mark.parametrize(
    "col_name, expected_dtype, int_check, extra_check",
    [
        ("doses", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("doses_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("doses1", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("doses1_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("doses2", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("doses2_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("pessoas_vacinadas_completamente", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("pessoas_vacinadas_completamente_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("pessoas_vacinadas_parcialmente", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("pessoas_vacinadas_parcialmente_novas", (float), lambda x: x % 1 == 0, lambda x: True), # can be negative
        ("pessoas_inoculadas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("pessoas_inoculadas_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("vacinas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
        ("vacinas_novas", (float), lambda x: x % 1 == 0, lambda x: x >= 0),
    ],
)
def test_dtype(data_vacinas, col_name, expected_dtype, int_check, extra_check):
    """
    Tests whether a certain column has the expected data types (and other column specific rules).
    """

    for i, row in data_vacinas.iterrows():
        val = row[col_name]

        if val == "NOO":
            # unknown value _heh_
            continue

        # Basic type assertion (panda always load as float)
        assert isinstance(
            val, expected_dtype
        ), "Dia {}: erro na coluna {}, valor {}".format(row["data"], col_name, val)

        # Check it's an integer (even if represented like float)
        if int_check is not None:
            assert int_check(
                val
            ), "Dia {} Coluna {}, valor {} não é inteiro".format(
                row["data"], col_name, val
            )

        # Extra verification
        if extra_check is not None:
            # FIXME semana em que Pfizer 2a dose foi adiada 21->28 dias houve poucas
            # 2a dose e o ajuste semanal dá negativo não se sabe ainda porquê
            if (
                row['data'].strftime("%Y-%m-%d") == '2021-03-29'
                and col_name == 'pessoas_vacinadas_completamente_novas'
                # and val == -552  # Relatório 22
                # and val == -377  # Relatório 24
                # and val == -315  # Relatório 25
                # and val == -235  # Relatório 26
                # and val == -142  # Relatório 27
                # and val == -69  # Relatório 28
                and val > 0  # 122 # Relatório 29
            ):
                continue
            assert extra_check(
                val
            ), "Dia {} Coluna {}, valor {} não é positivo ou zero".format(
                row["data"], col_name, val
            )


def test_delimiter_comma():
    """
    Tests that the delimiter is a comma
    """
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / ".." / "vacinas.csv"
    with open(csv_filepath, newline="") as csvfile:
        sample = csvfile.read()
        csv.Sniffer().sniff(sample, delimiters=",")


def test_blank_lines(data_vacinas):
    """
    Tests if the last row is blank
    """
    df_latest_line = data_vacinas.tail(1)  # Only run for the latest line
    for row in df_latest_line.iterrows():
        val = row[1]

    assert val["data"] != np.nan, "Empty row"


def test_sequentiality_new_vaccines(data_vacinas):
    """
    Tests if the number of new vaccines is correct
    """

    for i, row in data_vacinas.iterrows():
        # skip NaN for the first real value
        if i < 1:
            continue
        today = data_vacinas.iloc[i]
        yesterday = data_vacinas.iloc[i - 1]


        for k in [
            'doses', 'doses1', 'doses2',
            'pessoas_vacinadas_completamente', 'pessoas_vacinadas_parcialmente',
            'pessoas_inoculadas', 'vacinas',
        ]:
            if yesterday[f"{k}"] == "NOO" or today[f"{k}_novas"] == "NOO":
                # unknown value _heh_
                continue
            assert (
                today[f"{k}"] == yesterday[f"{k}"] + today[f"{k}_novas"]
            ), "Dia {} k={} today={} yesterday={} novas={} expected={}".format(
                row["data"],
                k,
                today[f"{k}"],
                yesterday[f"{k}"],
                today[f"{k}_novas"],
                today[f"{k}"] - yesterday[f"{k}"],
            )


def test_vaccines(data_vacinas):
    """
    Tests if the sum of vaccines is correct between themselves
    """
    for i, row in data_vacinas.iterrows():
        if row['doses1'] != 'NOO':
            assert row['doses'] == row['doses1'] + row['doses2'], row['data']
        if row['pessoas_vacinadas_parcialmente'] != 'NOO':
            assert row['pessoas_inoculadas'] == row['pessoas_vacinadas_parcialmente'] + row['pessoas_vacinadas_completamente'], row['data']
            if row['data'] >= datetime.datetime(2021, 5, 3):
                # before, the diff is small positive and negative, maybe recuperados
                # after, it grows due to Janssen
                assert row['vacinas'] <= row['pessoas_vacinadas_parcialmente'] + 2 * row['pessoas_vacinadas_completamente'], row['data']


def test_sequentiality_dates(data_vacinas):
    """
    Tests if the sequentiality of dates is correct
    """

    for i, row in data_vacinas.iterrows():
        # skip the first real value
        if i < 1:
            continue
        today_date = data_vacinas.iloc[i]["data"]
        yesterday_date = data_vacinas.iloc[i - 1]["data"]

        diff_date = (today_date - yesterday_date).days

        assert diff_date == 1
