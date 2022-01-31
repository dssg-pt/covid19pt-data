# -*- coding: utf-8 -*-
"""
@author: LgOliveira
"""
import re
import requests
from pathlib import Path

import locale
locale.setlocale(locale.LC_TIME, "pt_PT.UTF-8")


if __name__ == '__main__':

    url = 'https://covid19.min-saude.pt'

    response = requests.get(url=url)
    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from covid site. Error %s: $s' % response.status_code, response.text)

    # <a href="https://covid19.min-saude.pt/wp-content/uploads/2022/01/700_DGS_boletim_20220131.pdf" target="_blank">Ponto de Situação (31-01-2022)</a>
    matches = re.search((
        r'(https://covid19.min-saude.pt/wp-content/uploads/[0-9]+/[0-9]+/([0-9]+_DGS_boletim_([0-9]+)\.pdf))'
    ), response.text, re.MULTILINE | re.IGNORECASE)

    if not matches:
        print(response.text)
        raise("Link not found")
    link = matches.group(1)

    path = Path(__file__).resolve().parents[1]
    file=path / 'report_link.txt'
    with open(file,'r') as f:
        old_link = f.readline()

    if old_link != link:
        with open(file,'w') as f:
            f.write(link)
        print(f"UPDATED latest={old_link} link={link}")
