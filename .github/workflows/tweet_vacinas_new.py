# Imports
import os
import sys
import math
import datetime
from pathlib import Path
import pandas as pd
import numpy as np
import locale
try:
    locale.setlocale(locale.LC_TIME, "pt_PT.utf8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "pt_PT")


link_repo = "https://github.com/dssg-pt/covid19pt-data"

POP_PT = 10_347_892
POP_PT_CONTINENTE = 9_860_175
POP_VACINAVEL = 9_234_166
#POP_0_11 = 1_113_726

POP_80 = 352218 + 316442  # 80-84 + 85 ou mais
POP_70 = 544016 + 429107  # 70-74 + 75-79
#POP_65 = 620543
#POP_REFORCO_65PLUS = POP_65 + POP_70 + POP_80
#POP_REFORCO_12_64 = POP_VACINAVEL - POP_REFORCO_65PLUS
POP_60 = 672758 + 620543
POP_50 = 747581 + 734540
POP_REFORCO_50PLUS = POP_80 + POP_70 + POP_60 + POP_50
POP_REFORCO_12_49 = POP_VACINAVEL - POP_REFORCO_50PLUS

POP_05_12 = POP_PT - POP_VACINAVEL - 433332
print(POP_05_12)


POP_IDADE = {
    '0_9':     433332 + 461299,  #  0-04 + 05-09
    '10_19':   507646 + 549033,  # 10-14 + 15-19
    '20_29':   544575 + 547505,  # 20-24 + 25-29
    '30_39':   571355 + 679093,  # 30-34 + 35-39
    '40_49':   792670 + 782555,  # 40-44 + 45-49
    '50_59':   747581 + 734540,  # 50-54 + 55-59
    '60_69':   672758 + 620543,  # 60-64 + 65-69
    '65_69':        0 + 620543,  #     0 + 65-69
    '70_79':   544016 + 429107,  # 70-74 + 75-79
    '80_plus': 352218 + 316442,  # 80-84 + 85 ou mais
}

TENDENCIA = ["⬈", "⬊", "⬌"]
GTE = '≥'
CASAS_DECIMAIS = 1

# Note: to debug the tweet content without publishing, use
# export TWITTER_CONSUMER_KEY_VAC=DEBUG
consumer_key = os.environ['TWITTER_CONSUMER_KEY_VAC']
if consumer_key != 'DEBUG':
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET_VAC']
    access_token = os.environ['TWITTER_ACCESS_TOKEN_VAC']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET_VAC']

# ---
# Helper methods
def autenticar_twitter():
    import tweepy
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    try:
        return tweepy.API(auth)
    except Exception as e:
        print("Erro ao autenticar", e)
        pass

def f(valor, plus=False):
    if valor is None: 
        return "+?" if plus else ""
    valor = valor if type(valor) == int else round(float(valor), CASAS_DECIMAIS)
    r = format(valor, ",").replace(".","!").replace(",",".").replace("!",",")
    return f"+{r}" if plus and valor > 0 else r

def tweet_len(s):
    # quick hack to kind of count emojis as 2 chars. not 100% to spec
    return sum( (2 if ord(c)>0x2100 else 1) for c in s)

def t(valor):
    valor = valor if type(valor) == int else float(valor)
    return (
        TENDENCIA[0] if valor > 0
        else TENDENCIA[1] if valor < 0
        else TENDENCIA[2] if valor == 0 and len(TENDENCIA) > 2
        else ""
    )

def compose_tweets(DAYS_OFFSET=0):

    path = Path(__file__).resolve().parents[2]
    df = pd.read_csv(path / 'vacinas.csv',
        parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True
    )

    d = df.tail(DAYS_OFFSET + 1)[-1:]

    data = d.index.item().strftime("%d %b %Y")
    n_vacinados = int(d['pessoas_vacinadas_completamente'])
    n_vacinados_novas = int(d['pessoas_vacinadas_completamente_novas'])
    p_vacinados = 100.0 * n_vacinados / POP_PT
    p_vacinaveis = 100.0 * n_vacinados / POP_VACINAVEL

    n_vacinados_c = int(d['pessoas_vacinadas_completamente_continente'])
    n_vacinados_c_novas = int(d['pessoas_vacinadas_completamente_continente_novas'])
    p_vacinados_c = 100.0 * n_vacinados_c / POP_PT_CONTINENTE

    n_iniciados_05_12 = int(d['vacinação_iniciada_05_11'])
    n_iniciados_05_12_novas = int(d['vacinação_iniciada_05_11_novas'])
    p_iniciados_05_12 = 100.0 * n_iniciados_05_12 / POP_05_12

    n_vacinas = int(d['vacinas'])
    n_vacinas_novas = int(d['vacinas_novas'])
    p_vacinas = 100.0 * n_vacinas / POP_PT

    n_reforco_80 = int(d['reforço_80mais'])
    n_reforco_80_novas = int(d['reforço_80mais_novas'])
    p_reforco_80 = 100.0 * n_reforco_80 / POP_80
    n_reforco_70 = int(d['reforço_70_79'])
    n_reforco_70_novas = int(d['reforço_70_79_novas'])
    p_reforco_70 = 100.0 * n_reforco_70 / POP_70
    #n_reforco_65 = int(d['reforço_65_69'])
    #n_reforco_65_novas = int(d['reforço_65_69_novas'])
    #p_reforco_65 = 100.0 * n_reforco_65 / POP_65
    has_60_novas = not math.isnan(d['reforço_60_69_novas'])
    n_reforco_60 = int(d['reforço_60_69'])
    n_reforco_60_novas = int(d['reforço_60_69_novas']) if has_60_novas else None
    p_reforco_60 = 100.0 * n_reforco_60 / POP_60
    n_reforco_50 = int(d['reforço_50_59'])
    n_reforco_50_novas = int(d['reforço_50_59_novas']) if has_60_novas else None
    p_reforco_50 = 100.0 * n_reforco_50 / POP_50

    n_reforco = int(d['pessoas_reforço'])
    n_reforco_novas = int(d['pessoas_reforço_novas'])
    p_reforco = 100.0 * n_reforco / POP_PT_CONTINENTE

    n_reforco_resto = n_reforco - n_reforco_80 - n_reforco_70 - n_reforco_60 - n_reforco_50
    if has_60_novas:
        n_reforco_resto_novas = n_reforco_novas - n_reforco_80_novas - n_reforco_70_novas - n_reforco_60_novas - n_reforco_50_novas
    else:
        n_reforco_resto_novas = None
    p_reforco_resto = 100.0 * n_reforco_resto / POP_REFORCO_12_49

    n_gripe = int(d['pessoas_gripe'])
    n_gripe_novas = int(d['pessoas_gripe_novas'])
    p_gripe = 100.0 * n_gripe / POP_PT_CONTINENTE

    #n_vacinas_reforco = int(d['vacinas_reforço_e_gripe'])
    n_vacinas_reforco_novas = int(d['vacinas_reforço_e_gripe_novas'])
    #p_vacinas_reforco = int(n_vacinas_reforco / POP_REFORCO * 100_000)

    tweet_1 = (
        f"💉População 🇵🇹 vacinada até {data}:"
        f"\n"
        f"\nNacional"
        f"\nInoculações: {GTE}{f(n_vacinas)} {f(n_vacinas_novas, True)} {GTE}{f(p_vacinas)}%"
        f"\nVacinados: {GTE}{f(n_vacinados)} {f(n_vacinados_novas, True)} {GTE}{f(p_vacinados)}%"
        f"\nVacinados 12+: {GTE}{f(p_vacinaveis)}%"
        f"\n"
        f"\nContinente"
        f"\nVacinados: {f(n_vacinados_c)} {f(n_vacinados_c_novas, True)} {f(p_vacinados_c)}%"
        f"\nReforço: {f(n_reforco)} {f(n_reforco_novas, True)} {f(p_reforco)}%"
        f"\nIniciada 5-12: {f(n_iniciados_05_12)} {f(n_iniciados_05_12_novas, True)} {f(p_iniciados_05_12)}%"
        f"\n\n[1/2]"
    )
    tweet_2 = (
        f"💉População 🇵🇹 reforço até {data}:"
        f"\n80+: {f(n_reforco_80)} {f(n_reforco_80_novas, True)} {f(p_reforco_80)}%"
        f"\n70s: {f(n_reforco_70)} {f(n_reforco_70_novas, True)} {f(p_reforco_70)}%"
        f"\n60s: {f(n_reforco_60)} {f(n_reforco_60_novas, True)} {f(p_reforco_60)}%"
        f"\n50s: {f(n_reforco_50)} {f(n_reforco_50_novas, True)} {f(p_reforco_50)}%"
        f"\n12-49: {f(n_reforco_resto)} {f(n_reforco_resto_novas, True)} {f(p_reforco_resto)}%"
        f"\n"
        f"\nGripe: {f(n_gripe)} {f(n_gripe_novas, True)} {f(p_gripe)}%"
        f"\n"
        f"\nInoculações diárias: {f(n_vacinas_reforco_novas, True)}"
        f"\n\n[2/2]"
        f"\n\n➕Todos os dados em: {link_repo}"
    )
    return [tweet_1, tweet_2]


# ---
# Main
if __name__ == '__main__':

    DAYS_OFFSET = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    tweets = compose_tweets(DAYS_OFFSET)
    if not tweets:
        print("No today data to tweet about")
        sys.exit()

    if consumer_key == 'DEBUG':
        for i, tweet in enumerate(tweets):
            print(f"Tweet {i+1} {tweet_len(tweet)} '''\n{tweet}\n'''")
        exit(0)

    api = autenticar_twitter()
    try:
        api.me()
    except Exception as ex:
        print(f"Erro na autenticação. Programa vai fechar: {ex}")
        exit(0)

    # Update status and create thread
    try:
        prev_tweet = None
        for i, tweet in enumerate(tweets):
            print(f"Tweet {i+1} {tweet_len(tweet)} '''\n{tweet}\n'''")
            prev_tweet = api.update_status(tweet, prev_tweet)
            prev_tweet = prev_tweet.id_str

    except Exception as e:
        print("Erro a enviar o tweet", e)
        pass

