# Imports
from pathlib import Path
import pytest
import pandas as pd
import datetime

# Constants
NULL_PLACEHOLDER_VALUE = 'NOO'

# Tests fixture (.csv with DGS data)
@pytest.fixture(scope='module')
def dgs_data():
    """ Loads the CSV with the DGS data and applies some processing to it. """

    # Loading the CSV
    current_dir = Path(__file__).parent.absolute()
    csv_filepath = current_dir / '..' / 'data.csv'
    data = pd.read_csv(csv_filepath, parse_dates=[0, 1], infer_datetime_format=True, skip_blank_lines=False)
    
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


def _check_column_with_empty_sintomas(val):
    """ Guarantees symptoms are reported as expected. """

    # Let's check if it's a float
    if isinstance(val, float):

        # Is it <= 1.0?
        return val <= 1.0

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
       datetime.datetime.strptime(str(date), '%d-%m-%Y') # Will fail if not
   else:
       return False

def _check_datetime_format_publication(date):
    # Let's guarantee it makes sense (data starts on 26th February 2020)
   if date >= datetime.date(2020, 2, 26):

       # Let's guarantee it's in the correct format
       datetime.datetime.strptime(str(date), '%d-%m-%Y %H:%M') # Will fail if not
   else:
       return False

@pytest.mark.parametrize("col_name, expected_dtype, extra_check", [

    # Data de publicação
    ('data', (pd.Timestamp), _check_datetime_format),

    # Data a que se referem os dados
    ('data_dados', (pd.Timestamp), _check_datetime_format_publication),

    # Confirmados
    ('confirmados', (int), lambda x: x >= 0),
    ('confirmados_arsnorte', (int), lambda x: x >= 0),
    ('confirmados_arscentro', (int), lambda x: x >= 0),
    ('confirmados_arslvt', (int), lambda x: x >= 0),
    ('confirmados_arsalentejo', (int), lambda x: x >= 0),
    ('confirmados_arsalgarve', (int), lambda x: x >= 0),
    ('confirmados_acores', (int), lambda x: x >= 0),
    ('confirmados_madeira', (int), lambda x: x >= 0),
    ('confirmados_estrangeiro', (float, str), _check_column_with_empty),
    ('confirmados_novos', (int), lambda x: x >= 0),

    # Internados 
    ('internados', (float, str), _check_column_with_empty),
    ('internados_uci', (float, str), _check_column_with_empty),

    # Casos suspeitos
    ('suspeitos', (int), lambda x: x >= 0),

    # Casos sob vigilância
    ('vigilancia', (float, str), _check_column_with_empty),

    # Casos não confirmados
    ('n_confirmados', (float, str), _check_column_with_empty),

    # Número de cadeias de transmissão
    ('cadeias_transmissao', (float, str), _check_column_with_empty),

    # Casos de transmissão importada 
    ('transmissao_importada', (float, str), _check_column_with_empty),    
    
    # Casos confirmados (nas várias faixas etárias e por género)
    ('confirmados_0_9_f', (float, str), _check_column_with_empty),    
    ('confirmados_0_9_m', (float, str), _check_column_with_empty),    
    ('confirmados_10_19_f', (float, str), _check_column_with_empty),    
    ('confirmados_10_19_m', (float, str), _check_column_with_empty),    
    ('confirmados_20_29_f', (float, str), _check_column_with_empty),    
    ('confirmados_20_29_m', (float, str), _check_column_with_empty),    
    ('confirmados_30_39_f', (float, str), _check_column_with_empty),    
    ('confirmados_30_39_m', (float, str), _check_column_with_empty),    
    ('confirmados_40_49_f', (float, str), _check_column_with_empty),    
    ('confirmados_40_49_m', (float, str), _check_column_with_empty),    
    ('confirmados_50_59_f', (float, str), _check_column_with_empty),    
    ('confirmados_50_59_m', (float, str), _check_column_with_empty),    
    ('confirmados_60_69_f', (float, str), _check_column_with_empty),    
    ('confirmados_60_69_m', (float, str), _check_column_with_empty),    
    ('confirmados_70_79_f', (float, str), _check_column_with_empty),    
    ('confirmados_70_79_m', (float, str), _check_column_with_empty),    
    ('confirmados_80_plus_f', (float, str), _check_column_with_empty),    
    ('confirmados_80_plus_m', (float, str), _check_column_with_empty),   
    ('confirmados_f', (float, str), _check_column_with_empty),   
    ('confirmados_m', (float, str), _check_column_with_empty),   

    # Sintomas
    ('sintomas_tosse', (float, str), _check_column_with_empty_sintomas), 
    ('sintomas_febre', (float, str), _check_column_with_empty_sintomas), 
    ('sintomas_dificuldade_respiratoria', (float, str), _check_column_with_empty_sintomas), 
    ('sintomas_cefaleia', (float, str), _check_column_with_empty_sintomas), 
    ('sintomas_dores_musculares', (float, str), _check_column_with_empty_sintomas), 
    ('sintomas_fraqueza_generalizada', (float, str), _check_column_with_empty_sintomas), 
    ('sintomas_tosse', (float, str), _check_column_with_empty_sintomas), 

    # Óbitos
    ('obitos', (int), lambda x: x >= 0),
    ('obitos_arsnorte', (int), lambda x: x >= 0),
    ('obitos_arscentro', (int), lambda x: x >= 0),
    ('obitos_arslvt', (int), lambda x: x >= 0),
    ('obitos_arsalentejo', (int), lambda x: x >= 0),
    ('obitos_arsalgarve', (int), lambda x: x >= 0),
    ('obitos_acores', (int), lambda x: x >= 0),
    ('obitos_madeira', (int), lambda x: x >= 0),
    ('obitos_estrangeiro', (float, str), _check_column_with_empty),
    ('obitos_0_9_f', (float, str), _check_column_with_empty),    
    ('obitos_0_9_m', (float, str), _check_column_with_empty),    
    ('obitos_10_19_f', (float, str), _check_column_with_empty),    
    ('obitos_10_19_m', (float, str), _check_column_with_empty),    
    ('obitos_20_29_f', (float, str), _check_column_with_empty),    
    ('obitos_20_29_m', (float, str), _check_column_with_empty),    
    ('obitos_30_39_f', (float, str), _check_column_with_empty),    
    ('obitos_30_39_m', (float, str), _check_column_with_empty),    
    ('obitos_40_49_f', (float, str), _check_column_with_empty),    
    ('obitos_40_49_m', (float, str), _check_column_with_empty),    
    ('obitos_50_59_f', (float, str), _check_column_with_empty),    
    ('obitos_50_59_m', (float, str), _check_column_with_empty),    
    ('obitos_60_69_f', (float, str), _check_column_with_empty),    
    ('obitos_60_69_m', (float, str), _check_column_with_empty),    
    ('obitos_70_79_f', (float, str), _check_column_with_empty),    
    ('obitos_70_79_m', (float, str), _check_column_with_empty),    
    ('obitos_80_plus_f', (float, str), _check_column_with_empty),    
    ('obitos_80_plus_m', (float, str), _check_column_with_empty),   
    ('obitos_f', (float, str), _check_column_with_empty),   
    ('obitos_m', (float, str), _check_column_with_empty),   

    # Recuperados
    ('recuperados', (int), lambda x: x >= 0),
    ('recuperados_arsnorte', (float, str), _check_column_with_empty),
    ('recuperados_arscentro', (float, str), _check_column_with_empty),
    ('recuperados_arslvt', (float, str), _check_column_with_empty),
    ('recuperados_arsalentejo', (float, str), _check_column_with_empty),
    ('recuperados_arsalgarve', (float, str), _check_column_with_empty),
    ('recuperados_acores', (float, str), _check_column_with_empty),
    ('recuperados_madeira', (float, str), _check_column_with_empty),
    ('recuperados_estrangeiro', (float, str), _check_column_with_empty),

])
def test_dtype(dgs_data, col_name, expected_dtype, extra_check):
    """ 
    Tests whether a certain column has the expected data types (and other column specific rules).
    """

    df_latest_line = dgs_data.tail(1) # Only run for the latest line
    for row in df_latest_line.iterrows(): 
        val = row[1][col_name]
        
        # Basic type assertion
        assert isinstance(val, expected_dtype), "Dia {}: erro na coluna {}, valor {}".format(row[1]['data'], col_name, val)

        # Extra verification
        if extra_check is not None:
            assert extra_check(val), "Dia: Coluna {}, valor {} não cumpre as condições específicas".format(row[1]['data'], col_name, val)