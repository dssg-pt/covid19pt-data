# Imports
import os
import sys
import math
from datetime import date, timedelta
from pathlib import Path
import pandas as pd
import tweepy
import locale
try:
    locale.setlocale(locale.LC_TIME, "pt_PT.utf8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "pt_PT")

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

def extrair_dados_vacinas(DAYS_OFFSET=0):
    # Começar a compôr o dicionário de dados relevantes
    today = date.today() - timedelta(days=DAYS_OFFSET)
    dados_vacinas={'data': today.strftime("%-d de %B de %Y")}

    # Aceder ao .csv das vacinas
    path = Path(__file__).resolve().parents[2]
    file=path / 'vacinas.csv'
    df = pd.read_csv(file, parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True)

    # Verificar se há dados para o dia de hoje e se não são NaN
    today_f = today.strftime('%Y-%m-%d')
    if df.index[-1] == today and not math.isnan(df.loc[today_f].doses2):
        df["doses_7"] = df.doses.diff(7)
        df["doses1_7"] = df.doses1.diff(7)
        df["doses2_7"] = df.doses2.diff(7)
        df_today = df.loc[today_f]
        yesterday = date.today() - timedelta(days=DAYS_OFFSET+1)
        yesterday_f = yesterday.strftime('%Y-%m-%d')
        df_yesterday = df.loc[yesterday_f]

        dados_vacinas.update(
            {
                'percentagem': float(100*df_today.doses2/POP_PT),
                'n_vacinados': f(int(df_today.doses2)),
                'novos_vacinados': f(int(df_today.doses2_novas), plus=True),
                'tendencia_vacinados': t(int(df_today.doses2_7 - df_yesterday.doses2_7)),
                'n_inoculados': f(int(df_today.doses1) - int(df_today.doses2)),
                'novos_inoculados': f(int(df_today.doses1_novas), plus=True),
                'tendencia_inoculados': t(int(df_today.doses1_7 - df_yesterday.doses1_7)),
            }
        )
        return dados_vacinas
    elif consumer_key == 'DEBUG':
        return extrair_dados_vacinas(DAYS_OFFSET+1)
    else:
        return {}

def f(valor, plus=False):
    r = format(valor, ",").replace(".","!").replace(",",".").replace("!",",")
    return f"+{r}" if plus and valor > 0 else r

def t(valor):
    return "↑" if valor > 0 else "↓" if valor < 0 else ""

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
    bar = lsep + bar + "·"*n + rsep

    return (
        title + bar + 
        (" %.3f%%" % (value*100)).replace(".", ",")
    )

def compor_tweet(dados_vacinas):

    # Composing the tweet
    dados_vacinas.update({'progresso': progress(dados_vacinas['percentagem'])})

    tweet_message = (
        "💉🇵🇹  Percentagem da população vacinada a {data}: \n\n"
        "{progresso}"
        "\n\n"
        # "victory hand" is an original emoji \u270c and needs an extra space
        # on the console, but doesn't on twitter
        # "cross fingers" is a new emoji U+1F91E and does not need space
        "✌️{n_vacinados} vacinados com a 2ª dose"
        " ({novos_vacinados}{tendencia_vacinados})"
        "\n\n"
        "🤞{n_inoculados} inoculados com a 1ª dose"
        " ({novos_inoculados}{tendencia_inoculados})"
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
            print(f"Erro na autenticação. Programa vai fechar: {ex}")
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
