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


# TEMP PREVISÃO 70
POP_ADULTA = (
    # 1629213 + # 0-17 (16!)
     731177 + # 18-24
    3178928 + # 25-49
    2059302 + # 50-64
    1545230 + # 65-79
     655739 # 80+
)
# Excluir confirmados (assume que já estão imunes)
EXCLUIR_CONFIRMADOS = True
PERC_IMUNIDADE = 70

def quando_imunidade(df, pop, dados=None):
    vacinados_dia_media = math.floor(df.doses2_7 / 7)
    inoculados_dia_media = math.floor(df.doses1_7 / 7)
    # coeficientes desactivados para ser mais melhor bom
    falta_vacinar = int(
        pop
        # assume vacinado com eficiencia 94%
        - (df.doses2) * 0.94
        # assume 1ª dose com eficiencia 60%
        - (df.doses1 - df.doses2) * 0.6
    )
    if dados is not None:
        falta_vacinar -= int(
            # assume "infetado só precisa de 1 dose"
            # inclui obitos de proposito
            dados.confirmados * 0.5
        )
    media_dia = (
        0
        + vacinados_dia_media * 0.94
        + inoculados_dia_media * 0.6
    )
    if dados is not None:
        media_dia += int(
           dados.confirmados_novos * 0.5
        )
    dias = math.ceil(falta_vacinar / media_dia)
    quando = date.today() + timedelta(days=dias)
    quando_f = quando.strftime("%-d de %B de %Y") # ('%Y-%m-%d')
    if True or consumer_key == 'DEBUG':
        print(
            f"quando_imunidade: dados_dia={str(df.name)[:10]}"
            f" vacinados_dia_media={f(vacinados_dia_media)}"
            f" inoculados_dia_media={f(inoculados_dia_media)}"
            f" para_vacinar={f(pop)}"
            f" falta_vacinar={f(falta_vacinar)}"
            f" dias={dias}"
            f" quando={quando_f}"
        )
        imunizados = int(dados.confirmados) + int(df.doses1)
        print(
            f"imunizados: {imunizados}"
            f" ({f(round(100 * int(imunizados) / POP_PT_2019, 2))}%)"
            f" confirmados: {f(int(dados.confirmados))}"
            f" ({f(round(100 * int(dados.confirmados) / POP_PT_2019, 2))}%)"
            f" dose1: {f(int(df.doses1))}"
            f" ({f(round(100 * int(df.doses1) / POP_PT_2019, 2))}%)"
        )
    return quando, falta_vacinar


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
        df["doses1_7"] = df.doses1.diff(7)
        df["doses2_7"] = df.doses2.diff(7)
        df_today = df.loc[today_f]
        yesterday = date.today() - timedelta(days=DAYS_OFFSET+1)
        yesterday_f = yesterday.strftime('%Y-%m-%d')
        df_yesterday = df.loc[yesterday_f]


        if EXCLUIR_CONFIRMADOS:
            # Aceder ao .csv dos dados
            file=path / 'data.csv'
            df_dados = pd.read_csv(file, parse_dates=[0], index_col=[0], infer_datetime_format=True, skip_blank_lines=False, dayfirst=True)

        pop_para_vacinar = POP_ADULTA * PERC_IMUNIDADE / 100.0 if PERC_IMUNIDADE else POP_ADULTA
        dados = None

        if EXCLUIR_CONFIRMADOS:
            dados = df_dados.iloc[[-2]]
        quando_ontem, falta_vacinar = quando_imunidade(df_yesterday, pop_para_vacinar, dados)

        if EXCLUIR_CONFIRMADOS:
            dados = df_dados.iloc[[-1]]
        quando, falta_vacinar = quando_imunidade(df_today, pop_para_vacinar, dados)

        # TEMP PREVISÃO 70
        if True or consumer_key == 'DEBUG':
            debug = (
                f"pop={f(POP_PT_2019)}"
                f" pop_vacinar={f(POP_PT_VACINAR)}"
                f" ({f(round(100 * POP_PT_VACINAR / POP_PT_2019, 2))}%)"
                f" pop_adulta={f(POP_ADULTA)}"
                f" ({f(round(100 * POP_ADULTA / POP_PT_2019, 2))}%)"
            )
            if EXCLUIR_CONFIRMADOS:
                debug += (
                    f" confirmados={f(int(dados.confirmados))}"
                    f" ({f(round(100 * dados.confirmados / POP_PT_2019, 2))}%)"
                    f" ativos={f(int(dados.ativos))}"
                    f" ({f(round(100 * dados.ativos / POP_PT_2019, 2))}%)"
                    f" recuperados={f(int(dados.recuperados))}"
                    f" ({f(round(100 * dados.recuperados / POP_PT_2019, 2))}%)"
                    f" obitos={f(int(dados.obitos))}"
                    f" ({f(round(100*dados.obitos/POP_PT_2019, 2))}%)"
                )
            debug += (
                f" para_vacinar={f(pop_para_vacinar)}"
                f" ({f(round(100 * pop_para_vacinar / POP_PT_2019, 2))}%)"
                f" falta_vacinar={f(falta_vacinar)}"
                f" ({f(round(100 * falta_vacinar / POP_PT_2019, 2))}%)"
                f" quando_ontem={quando_ontem.strftime('%-d de %B de %Y')}"
                f" quando={quando.strftime('%-d de %B de %Y')}"
            )
            print(debug)

        doses2, doses1 = df_today.doses2, df_today.doses1
        doses2_novas, doses1_novas = df_today.doses2_novas, df_today.doses1_novas
        pop = POP_PT_VACINAR

        # inclusão valor semanal ilhas
        if False:
            pop = POP_PT_2019
            # TODO ler do vacinas_detalhe.csv
            doses2 += 15614 + 9316
            doses1 += 30429 + 17367
            # novas? 7dias?

        dados_vacinas.update(
            {
                'percentagem': float(100 * doses2 / pop),
                'n_vacinados': f(int(doses2)),
                'novos_vacinados': f(int(doses2_novas), plus=True),
                'tendencia_vacinados': t(int(df_today.doses2_7 - df_yesterday.doses2_7)),
                'media_7dias': f(int(df_today.doses2_7 / 7)),
                'n_inoculados': f(int(doses1) - int(doses2)),
                'novos_inoculados': f(int(doses1_novas), plus=True),
                'tendencia_inoculados': t(int(df_today.doses1_7 - df_yesterday.doses1_7)),
                'media_7dias_inoculados': f(int(df_today.doses1_7 / 7)),
            }
        )
        return dados_vacinas
    elif consumer_key == 'DEBUG':
        return extrair_dados_vacinas(DAYS_OFFSET+1)
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
        (" %.2f%%" % (value*100)).replace(".", ",")
    )

def compor_tweet(dados_vacinas):

    # Composing the tweet
    progresso = progress(dados_vacinas['percentagem'], length=15)
    dados_vacinas.update({'progresso': progresso})

    # note: "victory hand" is an first generation emoji \u270c and may
    # look tiny and seem to have no spacing, with some fonts, whilst
    # "cross fingers" is a new emoji U+1F91E and looks better.
    # On twitter both will be ok.

    tweet_message = (
        "💉População 🇵🇹 (continente) vacinada a {data}: \n\n"
        "{progresso}"
        "\n"
        "\n"
        "✌️{n_vacinados} vacinados"
        " ({novos_vacinados}{tendencia_vacinados},"
        " média 7 dias {media_7dias})"
        "\n"
        "\n"
        "🤞Mais {n_inoculados} inoculados com 1ª dose"
        " ({novos_inoculados}{tendencia_inoculados},"
        " média 7 dias {media_7dias_inoculados})"
        "\n"
        "\n➕Todos os dados em: {link_repo}"
    )

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

    # debug progress bar
    if False and consumer_key == 'DEBUG':
        step = 0.5
        for i in range(0, 1 + math.ceil(100 / step)):
            j = min(100, i * step)
            p = progress(j, length=20)
            #p = progress(j, length=20, vmin=0.00, vmax=100.00, goal=PERC_IMUNE)
            print(p)
        sys.exit(0)

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
