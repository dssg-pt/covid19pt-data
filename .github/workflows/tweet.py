# Imports
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
import tweepy
import locale
try:
    locale.setlocale(locale.LC_TIME, "pt_PT.utf8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "pt_PT")

# Constants
link_repo = "https://github.com/dssg-pt/covid19pt-data"
POP_PT = 10295909 # População residente em PT, via https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_indicadores&contecto=pi&indOcorrCod=0008273&selTab=tab0

# Login
# to verify the tweet content without publishing, use
# export TWITTER_CONSUMER_KEY=DEBUG
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
if consumer_key != 'DEBUG':
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

def f(valor):
    return format(valor, ",").replace(".","!").replace(",",".").replace("!",",")

ICONS = {
    # OMS recomenda 5 ; Portugal tem média 10 ; picos da onda passam 15
    "positividade": [15, 10, 5],
    # incidencia 14 dias por 100k
    "incidencia": [960, 480, 240],
    # confirmados_novos = (incidencia / 14 dias) / 100k * população
    "confirmados": [7060, 3530, 1765],
}

def icon(valor, tipo):
    return (
        "🟤" if valor >= ICONS[tipo][0] else
        "🔴" if valor >= ICONS[tipo][1] else
        "🟠" if valor >= ICONS[tipo][2] else
        "🟡"
    )

def calc_tendencia(df):
    """ Retorna a diferença da média 7 dias do ultimo dia para o dia anterior """
    diff7 = df.diff(7)
    return float(diff7[-1] - diff7[-2])

def autenticar_twitter():
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    try:
        api = tweepy.API(auth)
        return api
    except Exception as e:
        print("Erro a autenticar")
        print(e)
        pass

def extrair_dados_ultimo_relatorio():
    dados_extraidos={}

    #Aceder ao csv
    path = Path(__file__).resolve().parents[2]
    file=path / 'data.csv'
    df = pd.read_csv(file,parse_dates=[0],index_col=[0],infer_datetime_format=True,skip_blank_lines=False,dayfirst=True)
    df.fillna(value=0)

    # Formatar datas
    hoje=df.data_dados[-1]
    dados_extraidos["dia"] = datetime.strptime(hoje, '%d-%m-%Y %H:%M').strftime("%d %b %Y")

    ##Casos
    dados_extraidos["total_casos"]=int(df.confirmados[-1])
    dados_extraidos["novos_casos"]=int(df.confirmados.diff()[-1])
    dados_extraidos["novos_casos_tendencia"]=calc_tendencia(df.confirmados)

    ##Óbitos
    dados_extraidos["total_obitos"]=int(df.obitos[-1])
    dados_extraidos["novos_obitos"]=int(df.obitos.diff()[-1])
    dados_extraidos["novos_obitos_tendencia"]=calc_tendencia(df.obitos)

    ##Internados
    dados_extraidos["internados"] = int(df.internados[-1])
    dados_extraidos["internados_tendencia"] = calc_tendencia(df.internados)
    dados_extraidos["variacao_internados"]=int(df.internados.diff()[-1])

    dados_extraidos["uci"] = int(df.internados_uci[-1])
    dados_extraidos["uci_tendencia"] = calc_tendencia(df.internados_uci)
    dados_extraidos["variacao_uci"]=int(df.internados_uci.diff()[-1])

    ##Ativos
    dados_extraidos["total_ativos"]=int(df.ativos[-1])
    dados_extraidos["total_ativos_tendencia"]=calc_tendencia(df.ativos)
    dados_extraidos["novos_ativos"]=int(df.ativos.diff()[-1])
    #Percentagem total
    dados_extraidos["perc_ativos"] = round(float(100*df.ativos[-1]/df.confirmados[-1]),1)

    ##Recuperados
    dados_extraidos["total_recuperados"]=int(df.recuperados[-1])
    dados_extraidos["total_recuperados_tendencia"]=calc_tendencia(df.recuperados)
    dados_extraidos["novos_recuperados"]=int(df.recuperados.diff()[-1])
    #Percentagem total
    dados_extraidos["perc_recuperados"] = round(float(100*df.recuperados[-1]/df.confirmados[-1]),1)

    ## Regiões
    for k in ['lvt', 'norte', 'algarve', 'centro', 'alentejo', 'acores', 'madeira']:
        k2 = k if k in ['acores', 'madeira'] else f"ars{k}"
        dados_extraidos[f"novos_{k}"]=int(df[f"confirmados_{k2}"].diff()[-1])
        dados_extraidos[f"novos_{k}_tendencia"]=calc_tendencia(df[f"confirmados_{k2}"])
        dados_extraidos[f"novos_obitos_{k}"]=int(df[f"obitos_{k2}"].diff()[-1])
        dados_extraidos[f"novos_obitos_{k}_tendencia"]=calc_tendencia(df[f"obitos_{k2}"])

    # médias 7 e 14 dias
    df["confirmados1"] = df.confirmados.diff(1)
    df["confirmados7"] = df.confirmados.diff(7)
    df["confirmados14"] = df.confirmados.diff(14)

    #Aceder ao csv amostras
    path = Path(__file__).resolve().parents[2]
    file=path / 'amostras.csv'
    df_amostras = pd.read_csv(file,parse_dates=[0],index_col=[0],infer_datetime_format=True,skip_blank_lines=False,dayfirst=True)
    df_amostras.fillna(value=0)

    # médias 7 dias
    df_amostras["amostras1"] = df_amostras.amostras.diff(1)
    df_amostras["amostras7"] = df_amostras.amostras.diff(7)

    # amostras
    dados_extraidos["dia_amostras"] = df_amostras.index[-1].strftime("%d %b %Y")
    dados_extraidos["novas_amostras_pcr"] = int(df_amostras.amostras_pcr_novas[-1])
    dados_extraidos["novas_amostras_pcr_tendencia"] = calc_tendencia(df_amostras.amostras_pcr_novas)
    dados_extraidos["novas_amostras_ag"] = int(df_amostras.amostras_antigenio_novas[-1])
    dados_extraidos["novas_amostras_ag_tendencia"] = calc_tendencia(df_amostras.amostras_antigenio_novas)

    positividade7 = 100 * float(df[df.index == df_amostras.index[-1].strftime("%Y-%m-%d")].confirmados7[-1]) / float(df_amostras.amostras7[-1])
    dados_extraidos["perc_positividade7"] = round(positividade7, 1)
    dados_extraidos["icon_positividade7"] = icon(positividade7, "positividade")
    positividade7_anterior = 100 * float(df[df.index == df_amostras.index[-1-1].strftime("%Y-%m-%d")].confirmados7[-1]) / float(df_amostras.amostras7[-1-1])
    dados_extraidos["perc_positividade7_anterior"] = round(positividade7_anterior, 1)

    confirmados14 = int(df.confirmados14[-1] / 14)
    dados_extraidos["confirmados14"] = confirmados14
    dados_extraidos["icon_confirmados14"] = icon(confirmados14, "confirmados")
    confirmados14_anterior = int(df.confirmados14[-1-1] / 14) # previous day
    dados_extraidos["confirmados14_anterior"] = confirmados14_anterior

    confirmados7 = int(df.confirmados7[-1] / 7)
    dados_extraidos["confirmados7"] = confirmados7
    dados_extraidos["icon_confirmados7"] = icon(confirmados7, "confirmados")
    confirmados7_anterior = int(df.confirmados7[-1-1] / 7) # previous day
    dados_extraidos["confirmados7_anterior"] = confirmados7_anterior

    confirmados1 = int(df.confirmados1[-1] / 1)
    dados_extraidos["confirmados1"] = confirmados1
    dados_extraidos["icon_confirmados1"] = icon(confirmados1, "confirmados")
    confirmados1_anterior = int(df.confirmados1[-1-1] / 1) # previous day
    dados_extraidos["confirmados1_anterior"] = confirmados1_anterior

    incidencia14 = int(df.confirmados14[-1] * 100 * 1000 / POP_PT)
    dados_extraidos["incidencia14"] = incidencia14
    dados_extraidos["icon_incidencia14"] = icon(incidencia14, "incidencia")
    incidencia14_anterior = int(df.confirmados14[-1-1] * 100 * 1000 / POP_PT) # previous day
    dados_extraidos["incidencia14_anterior"] = incidencia14_anterior

    incidencia7 = int(df.confirmados7[-1] * 2 * 100 * 1000 / POP_PT)
    dados_extraidos["incidencia7"] = incidencia7
    dados_extraidos["icon_incidencia7"] = icon(incidencia7, "incidencia")
    incidencia7_anterior = int(df.confirmados7[-1-1] * 2 * 100 * 1000 / POP_PT) # previous day
    dados_extraidos["incidencia7_anterior"] = incidencia7_anterior

    for key in dados_extraidos.keys():
        valor = dados_extraidos[key]
        if type(valor) not in [int, float]:
            if not type(valor) in [str]:
                print(f"skip {key} {valor} {type(valor)}")
            continue
        dados_extraidos[key] = f(valor)
        if key.startswith('variacao_') or key.startswith('novos_'):
            dados_extraidos[key] = f"+{dados_extraidos[key]}" if valor > 0 else f"{dados_extraidos[key]}"
        elif key.startswith('aumento_'):
            if valor > 0:
                dados_extraidos[key] = f"↑{dados_extraidos[key]}"
            elif valor < 0:
                dados_extraidos[key] = f"↓{dados_extraidos[key]}"
        if key.startswith('perc_'):
            dados_extraidos[key] = f"{dados_extraidos[key]}%"
        if f"{key}_tendencia" in dados_extraidos:
            tendencia = dados_extraidos[f"{key}_tendencia"]
            if tendencia > 0:
                dados_extraidos[key] = f"{dados_extraidos[key]}↑"
            elif tendencia < 0:
                dados_extraidos[key] = f"{dados_extraidos[key]}↓"
        elif f"{key}_anterior" in dados_extraidos:
            valor_anterior = dados_extraidos[f"{key}_anterior"]
            if valor > valor_anterior:
                dados_extraidos[key] = f"{dados_extraidos[key]}↑"
            elif valor < valor_anterior:
                dados_extraidos[key] = f"{dados_extraidos[key]}↓"

    return dados_extraidos

def compor_tweets(dados_para_tweets):

    # Main tweet
    tweet_message = (
        "🆕Dados #COVID19PT atualizados [{dia}]:\n"
        "🫂Novos casos: {novos_casos} | Total: {total_casos}\n"
        "🪦Novos óbitos: {novos_obitos} | Total: {total_obitos}\n"
        "\n"
        "🦠Ativos: {total_ativos} ({novos_ativos})\n"
        "🚑Internados: {internados} ({variacao_internados})\n"
        "🏥Em UCI: {uci} ({variacao_uci})\n"
        "\n"
        "👍Recuperados {perc_recuperados} dos casos\n"
        "\n"
        "[1/3]"
    )

    # Thread
    second_tweet = (
        "🔎Por região, novos casos e novos óbitos:\n"
        "📍Norte: {novos_norte} · {novos_obitos_norte}\n"
        "📍Centro: {novos_centro} · {novos_obitos_centro}\n"
        "📍LVT: {novos_lvt} · {novos_obitos_lvt}\n"
        "📍Alentejo: {novos_alentejo} · {novos_obitos_alentejo}\n"
        "📍Algarve: {novos_algarve} · {novos_obitos_algarve}\n"
        "📍Açores: {novos_acores} · {novos_obitos_acores}\n"
        "📍Madeira: {novos_madeira} · {novos_obitos_madeira}\n"
        "\n"
        "[2/3]"
    )

    third_tweet = (
        "📈Incidência nacional por 100k:\n"
        "{icon_incidencia14}14 dias: {incidencia14}\n"
        "{icon_incidencia7}7 dias: {incidencia7}\n"
        "\n"
        "📅Amostras [{dia_amostras}]\n"
        "🧪PCR: {novas_amostras_pcr} | Antigénio: {novas_amostras_ag}\n"
        "{icon_positividade7}Positividade (7 dias): {perc_positividade7}\n"
        "\n"
        "[3/3]"
        "\n"
        "\n"
        "Todos os dados no nosso repositório:\n"
        "{link_repo}"
    )

    resto = (
        "🫂Casos diários, média últimos:\n"
        "{icon_confirmados1}1 dia: {confirmados1}\n"
        "{icon_confirmados7}7 dias: {confirmados7}\n"
        "{icon_confirmados14}14 dias: {confirmados14}\n"
        "\n"
        "[./.]"
    )

    dados_para_tweets["link_repo"] = link_repo
    texto_tweet_1 = tweet_message.format(**dados_para_tweets)
    texto_tweet_2 = second_tweet.format(**dados_para_tweets)
    texto_tweet_3 = third_tweet.format(**dados_para_tweets)
    texto_resto = resto.format(**dados_para_tweets)

    return texto_tweet_1, texto_tweet_2, texto_tweet_3, texto_resto

def tweet_len(s):
    # quick hack to kind of count emojis as 2 chars - not 100% to spec
    return sum( (2 if ord(c)>0x2100 else 1) for c in s)


if __name__ == '__main__':
    dados_extraidos = extrair_dados_ultimo_relatorio()
    texto_tweet_1, texto_tweet_2, texto_tweet_3, texto_resto = compor_tweets(dados_extraidos)

    if consumer_key == 'DEBUG':
        print(f"Tweet 1 {tweet_len(texto_tweet_1)} '''\n{texto_tweet_1}\n'''\n")
        print(f"Tweet 2 {tweet_len(texto_tweet_2)} '''\n{texto_tweet_2}\n'''\n")
        print(f"Tweet 3 {tweet_len(texto_tweet_3)} '''\n{texto_tweet_3}\n'''\n")
        print(f"Resto {tweet_len(texto_resto)} '''\n{texto_resto}\n'''\n")
        exit(0)

    api = autenticar_twitter()
    try:
      api.me()
    except Exception as ex:
        print(f"Erro na autenticação. Programa vai fechar: {ex}")
        exit(0)

    # Update status and create thread
    try:
        tweet1 = api.update_status(status = texto_tweet_1)
        tweet1Id = tweet1.id_str
        tweet2=api.update_status(texto_tweet_2, tweet1Id)
        tweet2Id = tweet2.id_str
        api.update_status(texto_tweet_3, tweet2Id)
    except Exception as e:
        print("Erro a enviar o tweet")
        print(e)
        pass
