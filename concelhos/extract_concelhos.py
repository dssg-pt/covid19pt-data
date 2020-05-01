from pathlib import Path
import glob
import re
import warnings
import pandas as pd
import tabula
import yaml


# path to reports
reports_path = Path(__file__).resolve().parents[1] / 'dgs-reports-archive'


# download official concelhos codes
dico = pd.read_csv('https://raw.githubusercontent.com/centraldedados/codigos_postais/master/data/concelhos.csv')
dico.sort_values(by='nome_concelho', inplace=True)


# import synonyms for concelhos
with open('fix_names.yml') as f:
    tmp = yaml.load(f, Loader=yaml.FullLoader)
    synonyms = {e: k for k, v in tmp.items() for e in v}


def extract_table(file, page=3):
    """
    Extract the main table with concelhos data.
    file: path to pdf file
    page: specify pdf page where concelhos data is found
    """
    raw_tables = tabula.read_pdf(file, pages=page, lattice=True, stream=False, multiple_tables=True, silent=True)
    tab_widths = [x.shape[1] for x in raw_tables]
    return raw_tables[tab_widths.index(max(tab_widths))]


def validate_table(t):
    """
    Checks if extracted table has expected data
    """
    keywords = ['CONCELHO', 'Lisboa', 'Condeixa-a-Nova', 'Portimão']

    for k in keywords:
        assert any(t[0].astype('str').str.contains(k)), f"Selected table does not include {k}"


def clean_table(t):
    """
    reshapes and cleans tabula extracted concelhos data
    """
    t = t.loc[~t[0].apply(lambda x: str(x)[:3].isupper())]
    t = pd.concat(
        [t.rename(columns={i: "concelho", i + 1: "casos"}).iloc[:, [i, i + 1]] for i in range(0, t.shape[1], 2)],
        axis=0, ignore_index=True)
    t.dropna(inplace=True)
    t['concelho'] = t['concelho'].apply(lambda x: re.sub('\\r', ' ', x))
    t['casos'].astype('int')

    if any(t['concelho'].duplicated()):
        warnings.warn(f"Dropping duplicated row for concelho: {t[t['concelho'].duplicated()]['concelho'].tolist()}")
        t.drop_duplicates(subset=['concelho'], keep='first', inplace=True)  # e.g. Penacova was duplicated on 02-Abril

    return t


def get_date(f):
    """
    get datestamp from the file path
    """

    x = re.search('\d{2}_\d{2}_\d{4}.pdf', str(f))
    x = x.group().split('.pdf')[0]
    return re.sub('_', '-', x)


def fix_concelho_name(name, synonyms_dict):
    """
    fixes incorrect table names using the synonyms dictionary
    """
    if name in synonyms_dict.keys():
        return synonyms_dict[name]
    else:
        return name


def get_concelhos_from_file(file, page=3):

    x = extract_table(file, page)

    try:
        validate_table(x)
        x = clean_table(x)
    except:
        warnings.warn('Report format is invalid and will not be processed.')
        return

    # replace incorrect concelho names
    x['concelho'] = x['concelho'].apply(lambda a: a.replace('*', ''))
    x['concelho'] = x['concelho'].apply(lambda a: fix_concelho_name(a, synonyms))


    # merge with official names

    if x['concelho'].isin(dico['nome_concelho']).all():
        x = pd.merge(dico, x, how='left', left_on='nome_concelho', right_on='concelho').drop(columns='concelho')
    else:
        tmp = x['concelho'][~x['concelho'].isin(dico['nome_concelho'])].to_list()
        raise Exception(f"There are invalid concelho names: {tmp}. Inspect and add to fix_names.yaml")

    # add date stamp
    x['dia'] = get_date(file)

    return x


if __name__ == '__main__':

    tables = []

    for report_number in range(22, len(list(reports_path.iterdir())) + 1):  # first report with concelhos: 22

        report_filepath = glob.glob(f"{reports_path}/*-{str(report_number).zfill(2)}_*")[0]
        print(f"Processing report {report_number} ({get_date(report_filepath)})...")

        try:
            df = get_concelhos_from_file(report_filepath)
            tables.append(df)

        except:
            warnings.warn(f"Cannot read data from {report_filepath}")

    final = pd.concat(tables, axis=0, ignore_index=True)

    final.to_csv('casos_concelho.csv', index=False)

    print('Finished.')
