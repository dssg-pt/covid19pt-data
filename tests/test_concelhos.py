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
    csv_filepath = current_dir / ".." / "data_concelhos.csv"
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
    
    #TODO: Optimize this. 
    # Loading the CSV
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / ".." / "data_concelhos.csv"
    data = pd.read_csv(csv_filepath)
    
    # Data de publicação
    data_dados = data['data']
    # Data a que se referem os dados
    
    data_dados.apply(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))

def test_delimiter_comma():
    """
    Tests that the delimiter is a comma
    """
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / ".." / "data_concelhos.csv"
    with open(csv_filepath, newline="", encoding='utf8') as csvfile:
        csv.Sniffer().sniff(csvfile.read(1024), delimiters=",")


def test_blank_lines(data_amostras):
    """
    Tests if the last row is blank
    """
    df_latest_line = data_amostras.tail(1)  # Only run for the latest line
    for row in df_latest_line.iterrows():
        val = row[1]
    
    assert val["data"] != np.nan, "Empty row"


def test_sequentiality_dates(data_amostras):
    """
    Tests if the sequentiality of dates is correct
    """

    for i, row in data_amostras.iterrows(): 
        if i >= 1:
            today_date = data_amostras.iloc[i]["data"]
            yesterday_date = data_amostras.iloc[i-1]["data"]
            diff_date = (today_date - yesterday_date).days
            assert diff_date == 1

