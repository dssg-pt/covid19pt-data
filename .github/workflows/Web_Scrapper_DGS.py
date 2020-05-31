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

# Get the link of TODAY
def links_of_day(path,text_to_find,day):
    date=day.strftime("%d/%m/%Y")
    l=''
    with requests.get(path) as r:
        soup=BeautifulSoup(r.text,"lxml")
        
        for link in soup.find_all('a'):
            if ( text_to_find in link.get_text()) & (date in link.get_text()):
                l=link.get('href')
                
        return l

# Get the latest day on the data.csv file
def get_latest_day():
    path = Path(__file__).resolve().parents[2]
    file=path / 'data.csv'
    df= pd.read_csv(file).sort_values(by='data',ascending=False)
    day=df.iloc[0,0]
    return day

#Save on .txt file
def save_link_txt(text_to_save):
    path = Path(__file__).resolve().parents[0]
    file=path / 'report_link.txt'
    with open(file,'w') as f:
        f.write(text_to_save)

if __name__ == '__main__':
    # Today
    date=(datetime.today())
    
    link=links_of_day('https://covid19.min-saude.pt/relatorio-de-situacao/',"Relatório de Situação",date)

    latest=get_latest_day()
    # Check if latest day on data.csv is today and if the link exists
    if ( datetime.strptime(latest, '%d/%m/%y')!=date.strftime("%d/%m/%Y")) & (link!=''):
        save_link_txt(link)

    
        