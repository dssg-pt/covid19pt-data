# Imports
import os
import sys
import math
from datetime import date, timedelta
from pathlib import Path
import pandas as pd
import locale
try:
    locale.setlocale(locale.LC_TIME, "pt_PT.utf8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "pt_PT")

INCLUIR_SEMANAL=False

# ---
# Constants
link_repo = "https://github.com/dssg-pt/covid19pt-data"

# População residente em PT final 2019, via
# https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_indicadores&contecto=pi&indOcorrCod=0008273&selTab=tab0
# Coerente com a soma da população dos concelhos, vide POP_ARS abaixo
POP_PT_2019 = 10295909

# Internacional, estimativa
# https://www.worldometers.info/world-population/portugal-population/
# 2021-02-14=10.178.145 2020=10.196.709 2019=10.226.187
# Público usa "projeção UN / OWID para 2020" = 10196707
# https://population.un.org/wpp/
# POP_PT = 10196709

# https://covid19.min-saude.pt/relatorio-de-vacinacao/
POP_PT_VACINAR = 9798859

# TENDENCIA = ["↑", "↓"]
TENDENCIA = ["⬈", "⬊", "⬌"]

CASAS_DECIMAIS=1

REGIONS={
    'arsnorte': 'Norte',
    'arscentro': 'Centro',
    'arslvt': 'LVT',
    'arsalentejo': 'Alentejo',
    'arsalgarve': 'Algarve',
    'madeira': 'Madeira',
    'açores': 'Açores'
}

# Note: to debug the tweet content without publishing, use
# export TWITTER_CONSUMER_KEY_VAC=DEBUG
consumer_key = os.environ['TWITTER_CONSUMER_KEY_VAC']
if consumer_key != 'DEBUG':
    import tweepy
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

def extrair_dados_vacinas(DAYS_OFFSET=0, ajuste_semanal=False):
    # Começar a compôr o dicionário de dados relevantes
    today = date.today() - timedelta(days=DAYS_OFFSET)
    dados_vacinas={
        # 'data': today.strftime("%-d de %B de %Y"),
        'data': today.strftime("%d %b %Y"),
        }

    # Aceder ao .csv das vacinas
    path = Path(__file__).resolve().parents[2]
    df = pd.read_csv(path / 'vacinas.csv',
        parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True
    )

    if not ajuste_semanal:
        pop = POP_PT_VACINAR
        suffix = ''
        ajuste_doses1, ajuste_doses2 = 0, 0
        data_detalhes = None
        df_last = None
    else:
        pop = POP_PT_2019
        suffix = '_nacional'

        df_detalhe = pd.read_csv(path / 'vacinas_detalhe.csv',
            parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True,
        )
        df = pd.merge(df, df_detalhe, how="outer", on="data", suffixes=("", "_detalhe"))
        df = df.ffill()
        df = df.assign(
            # https://github.com/owid/covid-19-data/blob/b796c2144748d2b70fad2a0c8d5d581d2adeab7b/scripts/scripts/vaccinations/automations/batch/portugal.py
            doses_nacional = df.doses + df.doses_madeira + df.doses_açores,
            doses1_nacional = df.doses1 + df.doses1_madeira + df.doses1_açores,
            doses2_nacional = df.doses2 + df.doses2_madeira + df.doses2_açores,
        )

        data_detalhes = df_detalhe[-1:].index
        df_last = df.loc[ data_detalhes ]
        data_detalhes = data_detalhes.item().strftime("%d %b %Y")

        df['doses1_nacional_novas'] = df['doses1_nacional'].diff(1)
        df['doses2_nacional_novas'] = df['doses2_nacional'].diff(1)
        df['doses1_nacional_7'] = df['doses1_nacional'].diff(7).div(7)
        df['doses2_nacional_7'] = df['doses2_nacional'].diff(7).div(7)

        # Janssen
        ajuste_doses1 = int(df_last['doses1_continente'] - df_last['doses1'])
        ajuste_doses2 = int(df_last['doses2_continente'] - df_last['doses2'])
        print(f"Ajuste dose1={ajuste_doses1} dose2={ajuste_doses2}")

    # Verificar se há dados para o dia de hoje e se não são NaN
    today_f = today.strftime('%Y-%m-%d')
    if df.index[-1] == today and not math.isnan(df.loc[today_f].doses2):
        # print(f"today={today_f} last_index={df.index[-1]} offset={DAYS_OFFSET}")
        df["doses1_7"] = df.doses1.diff(7)
        df["doses2_7"] = df.doses2.diff(7)
        df_today = df.loc[today_f]
        yesterday = date.today() - timedelta(days=DAYS_OFFSET+1)
        yesterday_f = yesterday.strftime('%Y-%m-%d')
        df_yesterday = df.loc[yesterday_f]

        doses1 = int(df_today[f'doses1{suffix}'])
        doses2 = int(df_today[f'doses2{suffix}'])
        dados_vacinas.update(
            {
                'percentagem': float(100 * (doses2+ajuste_doses2) / pop),
                'percentagem_vacinados': f(round(float(100 * (doses2+ajuste_doses2) / pop), CASAS_DECIMAIS)),
                'percentagem_inoculados': f(round(float(100 * doses1 / pop), CASAS_DECIMAIS)),
                'n_total': f(int(doses1)),
                'n_vacinados': f(int( (doses2+ajuste_doses2) )),
                'n_inoculados': f(int(doses1) - int( (doses2+ajuste_doses2) )),
                'novos_vacinados': f(int(df_today[f'doses2{suffix}_novas']), plus=True),
                'tendencia_vacinados': t(int(df_today[f'doses2{suffix}_7'] - df_yesterday[f'doses2{suffix}_7'])),
                'media_7dias': f(int(df_today[f'doses2{suffix}_7'] / 7)),
                'novos_inoculados': f(int(df_today[f'doses1{suffix}_novas']), plus=True),
                'tendencia_inoculados': t(int(df_today[f'doses1{suffix}_7'] - df_yesterday[f'doses1{suffix}_7'])),
                'media_7dias_inoculados': f(int(df_today[f'doses1{suffix}_7'] / 7)),
                'data_detalhes': data_detalhes,
                'df_last': df_last,
            }
        )
        return dados_vacinas
    elif consumer_key == 'DEBUG':
        # if running locally, also show tweet from yesterday for debugging
        return extrair_dados_vacinas(DAYS_OFFSET+1, ajuste_semanal=ajuste_semanal)
    else:
        return {}

def f(valor, plus=False):
    if valor is None: return None
    valor = valor if type(valor) == int else float(valor)
    r = format(valor, ",").replace(".","!").replace(",",".").replace("!",",")
    return f"+{r}" if plus and valor > 0 else r

def t(valor):
    valor = valor if type(valor) == int else float(valor)
    return (
        TENDENCIA[0] if valor > 0
        else TENDENCIA[1] if valor < 0
        else TENDENCIA[2] if valor == 0 and len(TENDENCIA) > 2
        else ""
    )

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

    # blocks = ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]
    # vertical blocks are more clear on showing progress - x+y axis!
    blocks = ["▁", "▂", "▃", "▄", "▅", "▆", "▇"]
    lsep, rsep = "▏", "▕"

    # Normalize value
    vmin, vmax = vmin or 0.0, vmax or 1.0
    value = min(max(value, vmin), vmax)
    value = (value-vmin)/float(vmax-vmin)

    v = value * length
    x = math.floor(v) # integer part
    y = v - x         # fractional part
    base = 1 / len(blocks)
    prec = 3
    i = int(round(base*math.floor(float(y)/base),prec)/base)
    # 100% would make this len*block + 1 so we substr
    bar = ("█" * x + blocks[i])[:length]
    n = length - len(bar)

    remaining = ""
    if n > 0:
        remaining = "▁" * n

    bar = lsep + bar + remaining + rsep

    return (
        title + bar +
        (f" %.{CASAS_DECIMAIS}f%%" % (value*100)).replace(".", ",")
    )

def compor_tweet(dados_vacinas, tweet=1):

    # Composing the tweet
    progresso = progress(dados_vacinas['percentagem'], length=15)
    dados_vacinas.update({'progresso': progresso})

    # note: "victory hand" is an first generation emoji \u270c and may
    # look tiny and seem to have no spacing, with some fonts, whilst
    # "cross fingers" is a new emoji U+1F91E and looks better.
    # On twitter both will be ok.


    tweet_message = ""

    if tweet == 3:
        tweet_message += (
            "💉População 🇵🇹 Nacional por idade {data_detalhes}:"
        )
        tweet_message += "\n"
        tweet_message += (
            "\n(vacinados, mais 1ª dose, em falta)"
        )
        tweet_message += "\n"

        df_last = dados_vacinas['df_last']
        for idade in ['80+', '65_79', '50_64', '25_49', '18_24']:
            perc2 = df_last[f'doses2_perc_{idade}']
            perc1 = df_last[f'doses1_perc_{idade}']
            vacinados = f(round( perc2 * 100.0, CASAS_DECIMAIS ))
            dose1 = f(round( (perc1 - perc2) * 100.0, CASAS_DECIMAIS ))
            falta = f(round( (1 - perc1) * 100.0, CASAS_DECIMAIS ))
            idade = idade.replace("_", "-")
            tweet_message += (
                f"\n{idade}: {vacinados}% {dose1}% {falta}%"
            )
    elif tweet == 4:
        tweet_message += (
            "💉Variação 🇵🇹 por região {data_detalhes}:"
        )
        tweet_message += "\n"
        tweet_message += (
            "\n(vacinados e 1ª dose, pp em relação a nacional)"
        )
        tweet_message += "\n"

        df_last = dados_vacinas['df_last']
        doses1, doses2 = float(df_last['doses1_perc']), float(df_last['doses2_perc'])
        for region in ['arsnorte', 'arscentro', 'arslvt', 'arsalentejo', 'arsalgarve', 'madeira', 'açores']:
            d1, d2 = float(df_last[f'doses1_perc_{region}']), float(df_last[f'doses2_perc_{region}'])
            #print(f"region={region} vacinados: {round( (d2-doses2)*100, 1)}pp 1ª dose: {round((d1-doses1)*100, 1)}pp")
            tweet_message += (
                f"\n{REGIONS[region]}: {f(round( (d2-doses2)*100, 1), True)} {f(round((d1-doses1)*100, 1), True)}"
            )

    else:
        tweet_message += (
            "💉População 🇵🇹 Continente {data}:"
        ) if tweet == 1 else (
            "💉População 🇵🇹 Nacional incluindo ilhas {data}:"
        ) if tweet == 2 else ""

        tweet_message += (
            "\n\n(ajustado ao relatório semanal de {data_detalhes})"
        ) if tweet != 1 else ""

        tweet_message += (
            "\n\n{progresso}"
        ) if tweet == 1 else ""

        tweet_message += (
            "\n\n✌️{n_vacinados}"
            " vacinados com 2 doses"
        ) if tweet == 1 else (
            "\n\n💉≥{n_vacinados}"
            " vacinação completa"
        )
        tweet_message += (
            " ({novos_vacinados}{tendencia_vacinados}"
            " média 7d {media_7dias})"
        ) if tweet == 1 else (
            " ({percentagem_vacinados}%)"
        )

        tweet_message += (
            "\n\n🤞Mais {n_inoculados}"
            " com 1 dose"
        ) if tweet == 1 else (
            "\n\n💉Mais ≥{n_inoculados}"
            " com 1ª dose"
        )
        tweet_message += (
            " ({novos_inoculados}{tendencia_inoculados}"
            " média 7d {media_7dias_inoculados})"
        ) if tweet == 1 else ""

        tweet_message += (
            "\n\n👍Total {n_total} inoculados"
        ) if tweet == 1 else (
            "\n\n👍Total ≥{n_total} inoculados"
        )
        tweet_message += (
            " ({percentagem_inoculados}%)"
        )

    tweet_message += (
        "\n\n#vacinaçãoCovid19"
    ) if tweet == 1 else ""

    total_tweets = 4 if INCLUIR_SEMANAL else 2
    tweet_message += (
        f"\n\n[{tweet}/{total_tweets}]"
    )
    tweet_message += (
        "\n\n➕Todos os dados em: {link_repo}"
    ) if tweet == total_tweets else ""

    dados_vacinas["link_repo"] = link_repo
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
        texto_tweet = compor_tweet(dados_vac, tweet=1)
        dados_vac_2 = extrair_dados_vacinas(ajuste_semanal=True)
        texto_tweet_2 = compor_tweet(dados_vac_2, tweet=2)
        texto_tweet_3 = compor_tweet(dados_vac_2, tweet=3) if INCLUIR_SEMANAL else ""
        texto_tweet_4 = compor_tweet(dados_vac_2, tweet=4) if INCLUIR_SEMANAL else ""

        if consumer_key == 'DEBUG':
            print(f"Tweet 1 {tweet_len(texto_tweet)} '''\n{texto_tweet}\n'''")
            print(f"Tweet 2 {tweet_len(texto_tweet_2)} '''\n{texto_tweet_2}\n'''")
            if texto_tweet_3:
                print(f"Tweet 3 {tweet_len(texto_tweet_3)} '''\n{texto_tweet_3}\n'''")
            if texto_tweet_4:
                print(f"Tweet 4 {tweet_len(texto_tweet_4)} '''\n{texto_tweet_4}\n'''")
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
            if texto_tweet_2:
                tweet2 = api.update_status(texto_tweet_2, tweet1.id_str)
            if texto_tweet_3:
                tweet3 = api.update_status(texto_tweet_3, tweet2.id_str)
            if texto_tweet_4:
                tweet4 = api.update_status(texto_tweet_4, tweet3.id_str)

        except Exception as e:
            print("Erro a enviar o tweet")
            print(e)
            pass
    # Otherwise, inform and exit
    else:
        print("No today data to tweet about")
        sys.exit()
