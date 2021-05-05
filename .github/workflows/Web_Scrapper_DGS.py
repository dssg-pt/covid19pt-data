# -*- coding: utf-8 -*-
"""
Created on Thu May 28 18:17:11 2020

@author: LgOliveira
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from pathlib import Path
import fileinput
import locale
locale.setlocale(locale.LC_TIME, "pt_PT.UTF-8")
import sys

# Get the link of TODAY
def links_of_day(path,text_to_find,day):
    date=day.strftime("%Y%m%d")
    with requests.get(path) as r:
        soup=BeautifulSoup(r.text,"lxml")
        
        for link in soup.find_all('a'):
            l=link.get('href')
            if l and text_to_find in l and date in l and l.endswith(".pdf"):
                return l
                
    return None

# Get the latest day on the data.csv file
def get_latest_day():
    path = Path(__file__).resolve().parents[2]
    file=path / 'data.csv'
    df= pd.read_csv(file)
    day=df.iloc[-1,0]
    return day

#Save on .txt file
def save_link_txt(text_to_save):
    path = Path(__file__).resolve().parents[1]
    file=path / 'report_link.txt'
    with open(file,'w') as f:
        f.write(text_to_save)

def update_readme(date_now):
    path = Path(__file__).resolve().parents[2]
    filepath = path / 'README.md'
    search_string = "📅️ **Última actualização**:"
    new_string = "📅️ **Última actualização**: {} de {} de {}, {}\n".format(date_now.day, date_now.strftime('%B').capitalize(), date_now.year, date_now.strftime('%H:%M'))

    for line in fileinput.input([filepath], inplace=True):
        if line.strip().startswith(search_string):
            line = new_string
        sys.stdout.write(line)

if __name__ == '__main__':
    
    # Today
    DAYS_OFFSET = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    date=(datetime.today() - timedelta(days=DAYS_OFFSET))

    # The link
    link=links_of_day('https://covid19.min-saude.pt/relatorio-de-situacao/', "DGS_boletim", date)

    # The latest report in the file data.csv
    latest=get_latest_day()

    # Check if latest day on data.csv is not today and if the link exists
    if link and (latest != date.strftime("%d-%m-%Y")):
        save_link_txt(link)
        update_readme(datetime.now())
        print(f"UPDATED latest={latest} today={date.strftime('%d-%m-%Y')} link={link}")
    else:
        print(f"NO CHANGES latest={latest} today={date.strftime('%d-%m-%Y')} link={link}")
