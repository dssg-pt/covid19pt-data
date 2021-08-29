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


INCLUIR_NACIONAL=True

# Monday is 0 and Sunday is 6.
# Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
DOW = datetime.date.today().weekday()
INCLUIR_SEMANAL=INCLUIR_NACIONAL and DOW in [2]
# INCLUIR_SEMANAL=True  # DEBUG

# ---
# Constants
link_repo = "https://github.com/dssg-pt/covid19pt-data"

# Sites que comparem Portugal com outros países tipicamente usam a
# estimativas da UN ou Worldometers ou equivalente, para serem comparáveis
# https://population.un.org/wpp/
# https://www.worldometers.info/world-population/portugal-population/

# Valores de Portugal usam valores INE 2019 (2020 desde Agosto 2021) para
# ser comparáveis ARS e Concelhos e faixas etárias
# População 2020 via relatório semanal vacinação
# https://covid19.min-saude.pt/relatorio-de-vacinacao/
POP_PT = 10_298_253  # 2019 = 10_295_909
POP_PT_CONTINENTE = 9_802_133  # 2019 = 9_798_859

# https://github.com/blasf1/covid_vaccine_progress_bot/blob/main/adult_population_2020.csv
POP_PT_VACINAVEL = 9_205_956
POP_PT_NAO_VACINAVEL = POP_PT - POP_PT_VACINAVEL  # < 12 = 1_092_297

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
    today = datetime.date.today() - datetime.timedelta(days=DAYS_OFFSET)
    dados_vacinas={ 'data': today.strftime("%d %b %Y") }
    #print(f"Dados para {today} {dados_vacinas['data']}")

    # Aceder ao .csv das vacinas
    path = Path(__file__).resolve().parents[2]
    df = pd.read_csv(path / 'vacinas.csv',
        parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True
    )

    if not ajuste_semanal:
        pop = POP_PT_CONTINENTE
        df_last, data_detalhes = None, None
    else:
        pop = POP_PT
        df_detalhe = pd.read_csv(path / 'vacinas_detalhe.csv',
            parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True,
        )
        df_detalhe.drop([col for col in df_detalhe.columns if "_novas" in col], inplace=True, axis=1)
        data_last = df_detalhe[-1:].index
        df_last = df_detalhe.loc[ data_last ]
        data_detalhes = data_last.item().strftime("%d %b %Y")

        # relatório corresponde a segunda mas sai terça noite portanto 7+1=8 dias e várias horas
        relatorio_terca_noite = (datetime.datetime.now() - data_last.item()) < datetime.timedelta(days=9)
        if relatorio_terca_noite:
            INCLUIR_SEMANAL=INCLUIR_NACIONAL and DOW in [1, 2] # caso saia relatorio terça noite

    df["doses1_7"] = df.doses1.diff(7)
    df["doses2_7"] = df.doses2.diff(7)

    # Verificar se há dados para o dia de hoje e se não são NaN
    today_f = today.strftime('%Y-%m-%d')
    try:
        df_today = df.loc[today_f]
    except KeyError:
        df_today = None
    if df_today is not None and not math.isnan(df_today.doses2):
        yesterday = datetime.date.today() - datetime.timedelta(days=DAYS_OFFSET+1)
        yesterday_f = yesterday.strftime('%Y-%m-%d')
        try:
            df_yesterday = df.loc[yesterday_f]
            df_yesterday = None if np.isnan(df_yesterday['doses']) else df_yesterday
        except KeyError:
            df_yesterday = None
        has_yesterday = df_yesterday is not None and len(df_yesterday)
        has_7d_yesterday = has_yesterday and not np.isnan(df_yesterday['doses1_7']) and not np.isnan(df_yesterday['doses2_7'])
        has_7d_today = not np.isnan(df_today['doses1_7']) and not np.isnan(df_today['doses2_7'])

        doses1 = int(df_today['pessoas_inoculadas' if ajuste_semanal else 'doses1'])
        doses2 = int(df_today['pessoas_vacinadas_completamente' if ajuste_semanal else 'doses2'])
        vacinas = df_today['vacinas_novas' if ajuste_semanal else 'doses_novas'] if has_yesterday else None
        vacinas = int(vacinas) if vacinas is not None and not np.isnan(vacinas) else None
        dados_vacinas.update(
            {
                'percentagem': float(100 * doses2 / pop),
                'percentagem_vacinados': f(round(float(100 * doses2 / pop), CASAS_DECIMAIS)),
                'percentagem_inoculados': f(round(float(100 * doses1 / pop), CASAS_DECIMAIS)),
                'n_total': f(int(doses1)),
                'n_vacinados': f(int(doses2)),
                'n_inoculados': f(int(doses1) - int(doses2)),
                'vacinas': f(int(vacinas)) if has_yesterday and vacinas else None,
                # tweet 1
                'novos_vacinados': f(int(df_today['doses2_novas']), plus=True) if has_yesterday else None,
                'tendencia_vacinados': t(int(df_today['doses2_7'] - df_yesterday['doses2_7'])) if has_7d_today and has_7d_yesterday else '',
                'media_7dias': f(int(df_today['doses2_7'] / 7)) if has_7d_today else None,
                'novos_inoculados': f(int(df_today['doses1_novas']), plus=True) if has_yesterday else None,
                'tendencia_inoculados': t(int(df_today['doses1_7'] - df_yesterday['doses1_7'])) if has_7d_today and has_7d_yesterday else '',
                'media_7dias_inoculados': f(int(df_today['doses1_7'] / 7)) if has_7d_today else None,
                #
                'has_yesterday': bool(has_yesterday),
                'data_detalhes': data_detalhes,
                'df_last': df_last,
            }
        )
        return dados_vacinas
    elif consumer_key == 'DEBUG' or INCLUIR_SEMANAL:
        if DAYS_OFFSET > 7:
            print(f"Sem dados durante uma semana, desisto. {today}, a usar dia anterior {DAYS_OFFSET+1}")
            return {}
        # if running locally, also show tweet from yesterday for debugging
        print(f"Sem dados para {today}, a usar dia anterior {DAYS_OFFSET+1}")
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

    has_yesterday = dados_vacinas['has_yesterday']

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
        # populacao1_0_17 = 1_701_688
        for idade in ['80+', '65_79', '50_64', '25_49', '18_24', '0_17']:
            if idade == '0_17':
                pop = df_last[f'populacao1_{idade}'] - POP_PT_NAO_VACINAVEL
                doses2 = df_last[f'pessoas_vacinadas_completamente_{idade}']
                doses1 = df_last[f'pessoas_inoculadas_{idade}']
                perc2 = min(1, float(doses2 / pop))
                perc1 = min(1, float(doses1 / pop))
                idade = '12_17'
            else:
                # POP é de 2019 mas relatório já começa a falar em 2020 e estamos em 2021
                # portanto já se começa a ter mais de 100% nos escalões 80+ e 70
                perc2 = min(1, float(df_last[f'pessoas_vacinadas_completamente_perc_{idade}']))
                perc1 = min(1, float(df_last[f'pessoas_inoculadas_perc_{idade}']))
            vacinados = f(round( perc2 * 100.0, CASAS_DECIMAIS ))
            dose1 = f(round( max(0, float(perc1 - perc2)) * 100.0, CASAS_DECIMAIS ))
            falta = f(round( max(0, float(1 - perc1)) * 100.0, CASAS_DECIMAIS ))
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
            "\n(ajustado ao relatório semanal de {data_detalhes})"
        ) if tweet != 1 else ""

        tweet_message += (
            "\n\n{progresso}"
        ) if tweet == 1 else ""

        tweet_message += (
            "\n\n✌️{n_vacinados}"
            " com 2 doses"
        ) if tweet == 1 else (
            "\n\n💉≥{n_vacinados}"
            " vacinação completa"
        )
        if has_yesterday:
            tweet_message += (
                " ({novos_vacinados}{tendencia_vacinados}" +
                (" média 7d {media_7dias}" if dados_vacinas['media_7dias'] else '') +
                ")"
            ) if tweet == 1 else ""

        tweet_message += "" if tweet == 1 else (
            " ({percentagem_vacinados}%)"
        )

        tweet_message += (
            "\n🤞{n_inoculados}"
            " com 1 dose"
        ) if tweet == 1 else (
            "\n💉≥{n_inoculados}"
            " com 1ª dose"
        )
        if has_yesterday:
            tweet_message += (
                " ({novos_inoculados}{tendencia_inoculados}" +
                (" média 7d {media_7dias_inoculados}" if dados_vacinas['media_7dias_inoculados'] else '') +
                ")"
            ) if tweet == 1 else ""

        tweet_message += (
            "\n👍{n_total} com pelo menos 1 dose"
        ) if tweet == 1 else (
            "\n👍≥{n_total} com pelo menos 1 dose"
        )
        tweet_message += (
            " ({percentagem_inoculados}%)"
        )

        if has_yesterday:
            tweet_message += (
                "\n\n💉Vacinas diárias {vacinas}"
            ) if tweet == 1 else ""

    #tweet_message += (
    #    "\n\n#vacinaçãoCovid19"
    #) if tweet == 1 else ""

    total_tweets = 4 if INCLUIR_SEMANAL else 2 if INCLUIR_NACIONAL else 1
    if total_tweets > 1:
        tweet_message += (
            f"\n\n[{tweet}/{total_tweets}]"
        )
    tweet_message += (
        "\n➕Todos os dados em: {link_repo}"
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

    DAYS_OFFSET = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    dados_vac = extrair_dados_vacinas(DAYS_OFFSET)

    # If there's new data, tweet
    if dados_vac:
        texto_tweet = compor_tweet(dados_vac, tweet=1)
        dados_vac_2 = extrair_dados_vacinas(DAYS_OFFSET, ajuste_semanal=True) if INCLUIR_NACIONAL else {}
        texto_tweet_2 = compor_tweet(dados_vac_2, tweet=2) if INCLUIR_NACIONAL else ""
        texto_tweet_3 = compor_tweet(dados_vac_2, tweet=3) if INCLUIR_SEMANAL else ""
        texto_tweet_4 = compor_tweet(dados_vac_2, tweet=4) if INCLUIR_SEMANAL else ""

        if consumer_key == 'DEBUG':
            print(f"Tweet 1 {tweet_len(texto_tweet)} '''\n{texto_tweet}\n'''")
            if texto_tweet_2:
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
