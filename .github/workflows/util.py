import pandas as pd
import numpy as np


def convert(df, cols, func):
    """ Apply func to columnss of dataframe. """
    df[cols] = df[cols].applymap(func)
    return df


def convert_to_int(x):
    """ Convert NaN to empty string, numbers to integers, or fallback to self. """
    if x is None or np.isnan(x):
        return ""
    try:
        return int(round(x))
    except:
        return x


def convert_to_float(x):
    """ Convert NaN to empty string, numbers to 2 digits. """
    if x is None or np.isnan(x):
        return ""
    else:
        return round(float(x), 2)
