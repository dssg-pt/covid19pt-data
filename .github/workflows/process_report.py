""" Renames and verifies whether the report is really new. """

# Imports 
import os
import sys
import datetime
import shutil
from pathlib import Path

# Constants
reports_folder = Path(__file__).resolve().parents[2] / 'dgs-reports-archive'

# Helper functions
def get_reports_list(reports_folder):
    reports_list = list(reports_folder.iterdir())
    reports = [r for r in reports_list if str(r).endswith('.pdf')]

    return reports


def _extract_report_id(r):
    r_file = r[r.rfind('/'):]
    r_id = int(r_file[r_file.rfind('-') + 1:r_file.find('_')])
    return r_id

def get_latest_report_date_id(reports_list):
    reports_list = [str(r) for r in reports_list]
    reports_list.sort(key=_extract_report_id)

    latest_name = reports_list[-1]
    latest_name_file = latest_name[latest_name.rfind('/')+1:]
    latest_id = int(latest_name_file[latest_name_file.rfind('-') + 1:latest_name_file.find('_')])

    # Now, let's extract the date from the report
    latest_year = int(latest_name_file.split('_')[-1].split('.')[0])
    latest_month = int(latest_name_file.split('_')[-2])
    latest_day = int(latest_name_file.split('_')[-3])

    latest_date = datetime.datetime(latest_year, latest_month, latest_day)
    
    return latest_date, latest_id


def rename_report(report_filepath, latest_date, latest_id):
    
    # Getting its modification date
    fname = Path(report_filepath)
    m_date = datetime.datetime.fromtimestamp(fname.stat().st_mtime)

    # TODO: Should check out whether m_date > latest_date (but latest_date should be extracted from the PDF metadata)

    new_name = "Relatório-de-Situação-{:02d}_{:02d}_{:02d}_{:04d}.pdf".format(latest_id+1, m_date.day, m_date.month, m_date.year)
    os.rename(report_filepath, new_name)
    
    return new_name


# Main
if __name__ == '__main__':

    # Getting the list of reports
    reports = get_reports_list(reports_folder)
    
    # Date of the last report
    latest_date, latest_id = get_latest_report_date_id(reports)

    # Getting the report's filename
    report = None
    for f in Path(__file__).parent.iterdir():
        if str(f).endswith('.pdf'):
            report = f

    # If no PDF file (download failed and error was not caught) 
    if report is None:
        sys.exit(-1)

    # Renaming the report
    new_name = rename_report(report, latest_date, latest_id)

    # Moving the report
    shutil.move(new_name, str(reports_folder / new_name))

    # Finishing 
    sys.exit(0)

