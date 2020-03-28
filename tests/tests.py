import pytest
import pandas as pd

def test_first():
    data = pd.read_csv('data.csv')
	
    print(data)

    assert data['confirmados'].iloc[0] == 0, "CSV was changed"