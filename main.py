import os
import requests  # noqa We are just importing this to prove the dependency installed correctly
import numpy as np
import pandas as pd

def main():
    data = pd.read_csv('data.csv')

    assert data['confirmados'].iloc[0] == 0, "CSV was changed"



if __name__ == "__main__":
    main()
