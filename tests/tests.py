import pytest
import pandas as pd

def first_test():
    data = pd.read_csv('data.csv')

    assert data['confirmados'].iloc[0] == 0, "CSV was changed"