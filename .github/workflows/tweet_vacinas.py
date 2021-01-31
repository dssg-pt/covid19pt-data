# Imports
import os
import sys
import math
from datetime import date
from pathlib import Path
import pandas as pd
import tweepy

# ---
# Constants
POP_PT = 10295909 # População residente em PT, via https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_indicadores&contecto=pi&indOcorrCod=0008273&selTab=tab0

# To verify the tweet content without publishing, use export TWITTER_CONSUMER_KEY_VAC=DEBUG
consumer_key = os.environ['TWITTER_CONSUMER_KEY_VAC']
if consumer_key != 'DEBUG':
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET_VAC']
    access_token = os.environ['TWITTER_ACCESS_TOKEN_VAC']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET_VAC']

# ---
# Helper methods
def autenticar_twitter():
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    try:
        api = tweepy.API(auth)
        return api
    except Exception as e:
        print("Erro ao autenticar")
        print(e)
        pass

def extrair_dados_vacinas():

    # Começar a compôr o dicionário de dadis relevantes
    today = date.today()
    dados_vacinas={'data': today.strftime("%d de %B de %Y")}

    # Aceder ao .csv das vacinas
    path = Path(__file__).resolve().parents[2]
    file=path / 'vacinas.csv'
    df = pd.read_csv(file, parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True)
    
    # Verificar se há dados para o dia de hoje e se não são NaN
    today_f = today.strftime('%Y-%m-%d')
    if df.index[-1] == today and not math.isnan(df.loc[today_f].doses2):
        dados_vacinas.update(
            {
                'percentagem': (df.loc[today_f].doses2/POP_PT)*100, 
                'n_vacinados': int(df.loc[today_f].doses2),
            }
        )
        return dados_vacinas
    else: 
        return {}

def progress(value, length=30, title = "", vmin=0.00, vmax=100.00):
    """
    Text progress bar. Adapted from https://gist.github.com/rougier/c0d31f5cbdaac27b876c, Nicolas P. Rougier

    Parameters
    ----------
    value : float
        Current value to be displayed as progress

    vmin : float
        Minimum value

    vmax : float
        Maximum value

    length: int
        Bar length (in character)

    title: string
        Text to be prepend to the bar
    """

    # Block progression is 1/8
    blocks = ["", "▏","▎","▍","▌","▋","▊","▉","█"]
    vmin = vmin or 0.0
    vmax = vmax or 1.0
    lsep, rsep = "▏", "▕"

    # Normalize value
    value = min(max(value, vmin), vmax)
    value = (value-vmin)/float(vmax-vmin)
    
    v = value*length
    x = math.floor(v) # integer part
    y = v - x         # fractional part
    base = 0.125      # 0.125 = 1/8
    prec = 3
    i = int(round(base*math.floor(float(y)/base),prec)/base)
    bar = "█"*x + blocks[i]
    n = length-len(bar)
    bar = lsep + bar + " "*n + rsep

    return ("\r" + title + bar + " %.2f%%" % (value*100))

def compor_tweet(dados_vacinas):

    # Composing the tweet
    dados_vacinas.update({'progresso': progress(dados_vacinas['percentagem'])})

    tweet_message = (
        "💉🇵🇹  Percentagem da população vacinada a {data}: \n\n"
        "{progresso} \n\n"
        "{n_vacinados} vacinados"
        )

    texto_tweet = tweet_message.format(**dados_vacinas)

    return texto_tweet

def tweet_len(s):
    # quick hack to kind of count emojis as 2 chars
    # not 100% to spec
    return sum( (2 if ord(c)>0x2100 else 1) for c in s)

# ---
# Main 
if __name__ == '__main__':
    dados_vac = extrair_dados_vacinas()

    # If there's new data, tweet
    if dados_vac: 
        texto_tweet = compor_tweet(dados_vac)

        if consumer_key == 'DEBUG':
            print(f"Tweet 1 {tweet_len(texto_tweet)} '''\n{texto_tweet}\n'''")
            exit(0)

        api = autenticar_twitter()
        try:
            api.me()
        except Exception as ex:
            print("Erro na autenticação. Programa vai fechar")
            exit(0)

        # Update status and create thread
        try:
            tweet1 = api.update_status(status = texto_tweet)
        except Exception as e:
            print("Erro a enviar o tweet")
            print(e)
            pass
    # Otherwise, inform and exit
    else:
        print("No today data to tweet about")
        sys.exit()