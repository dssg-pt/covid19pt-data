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
    dados_extraidos["aumento_casos"]=round(dados_extraidos["novos_casos"]/dados_extraidos["total_casos"]*100,1)

    ##Óbitos
    dados_extraidos["total_obitos"]=int(df.obitos[-1])
    dados_extraidos["novos_obitos"]=int(df.obitos.diff()[-1])
    dados_extraidos["aumento_obitos"]=round(dados_extraidos["novos_obitos"]/dados_extraidos["total_obitos"]*100,2)

    ##Internados
    dados_extraidos["internados"] = int(df.internados[-1])
    dados_extraidos["variacao_internados"]=int(df.internados.diff()[-1])

    dados_extraidos["uci"] = int(df.internados_uci[-1])
    dados_extraidos["variacao_uci"]=int(df.internados_uci.diff()[-1])

    ##Ativos
    dados_extraidos["total_ativos"]=int(df.ativos[-1])
    dados_extraidos["novos_ativos"]=int(df.ativos.diff()[-1])
    dados_extraidos["aumento_ativos"]=round(dados_extraidos["novos_ativos"]/dados_extraidos["total_ativos"]*100,1)
    #Percentagem total
    dados_extraidos["perc_ativos"] = round(float(df.ativos.tail(1).values[0]/df.confirmados.tail(1).values[0]*100),1)

    ##Recuperados
    dados_extraidos["total_recuperados"]=int(df.recuperados[-1])
    dados_extraidos["novos_recuperados"]=int(df.recuperados.diff()[-1])
    dados_extraidos["aumento_recuperados"]=round(dados_extraidos["novos_recuperados"]/dados_extraidos["total_recuperados"]*100,1)
    #Percentagem total
    dados_extraidos["perc_recuperados"] = round(float(df.recuperados.tail(1).values[0]/df.confirmados.tail(1).values[0]*100),1)

    ## Regiões
    dados_extraidos["novos_lvt"]=int(df.confirmados_arslvt.diff()[-1])
    dados_extraidos["novos_norte"]=int(df.confirmados_arsnorte.diff()[-1])
    dados_extraidos["novos_algarve"]=int(df.confirmados_arsalgarve.diff()[-1])
    dados_extraidos["novos_centro"]=int(df.confirmados_arscentro.diff()[-1])
    dados_extraidos["novos_alentejo"]=int(df.confirmados_arsalentejo.diff()[-1])
    dados_extraidos["novos_acores"]=int(df.confirmados_acores.diff()[-1])
    dados_extraidos["novos_madeira"]=int(df.confirmados_madeira.diff()[-1])
    dados_extraidos["novos_obitos_lvt"]=int(df.obitos_arslvt.diff()[-1])
    dados_extraidos["novos_obitos_norte"]=int(df.obitos_arsnorte.diff()[-1])
    dados_extraidos["novos_obitos_algarve"]=int(df.obitos_arsalgarve.diff()[-1])
    dados_extraidos["novos_obitos_centro"]=int(df.obitos_arscentro.diff()[-1])
    dados_extraidos["novos_obitos_alentejo"]=int(df.obitos_arsalentejo.diff()[-1])
    dados_extraidos["novos_obitos_acores"]=int(df.obitos_acores.diff()[-1])
    dados_extraidos["novos_obitos_madeira"]=int(df.obitos_madeira.diff()[-1])

    #Aceder ao csv amostras
    path = Path(__file__).resolve().parents[2]
    file=path / 'amostras.csv'
    df_amostras = pd.read_csv(file,parse_dates=[0],index_col=[0],infer_datetime_format=True,skip_blank_lines=False,dayfirst=True)
    df_amostras.fillna(value=0)

    # amostras
    df["confirmados7"] = df.confirmados.diff(7)
    df_amostras["amostras7"] = df_amostras.amostras.diff(7)

    dados_extraidos["dia_amostras"] = df_amostras.index[-1].strftime("%d %b %Y")
    data_amostras = df[df.index == df_amostras.index[-1].strftime("%Y-%m-%d")]

    dados_extraidos["novas_amostras_pcr"] = int(df_amostras.amostras_pcr_novas[-1])
    dados_extraidos["novas_amostras_ag"] = int(df_amostras.amostras_antigenio_novas[-1])
    positividade = 100 * float(data_amostras.confirmados7[-1]) / float(df_amostras.amostras7[-1])
    dados_extraidos["perc_positividade"] = round(positividade, 1)
    dados_extraidos["icon_positividade"] = (
        "🟤" if positividade >= 20 else
        "🔴" if positividade >= 10 else
        "🟠" if positividade >= 5 else
        "🟡"
    )

    df["confirmados14"] = df.confirmados.diff(14)
    incidencia = int(df.confirmados14[-1] * 100 * 1000 / POP_PT)
    dados_extraidos["incidencia"] = incidencia 
    dados_extraidos["icon_incidencia"] = (
        "🟤" if incidencia >= 960 else
        "🔴" if incidencia >= 480 else
        "🟠" if incidencia >= 240 else
        "🟡"
    )

    for key in dados_extraidos.keys():
        valor = dados_extraidos[key]
        if type(valor) not in [int, float]: continue
        dados_extraidos[key] = f(valor)
        if key.startswith('variacao_') or key.startswith('novos_'):
            dados_extraidos[key] = f"+{dados_extraidos[key]}" if valor > 0 else f"{dados_extraidos[key]}"
        elif key.startswith('aumento_'):
            if valor > 0:
                dados_extraidos[key] = f"↑{dados_extraidos[key]}"
            elif valor < 0:
                dados_extraidos[key] = f"↓{dados_extraidos[key]}"

    return dados_extraidos

def compor_tweets(dados_para_tweets):

    # Main tweet
    tweet_message = (
        "🆕Dados #COVID19PT atualizados [{dia}]:\n"
        "🫂Novos casos: {novos_casos} ({aumento_casos}%) | Total: {total_casos}\n"
        "🪦Novos óbitos: {novos_obitos} ({aumento_obitos}%) | Total: {total_obitos}\n"
        "\n"
        "🦠Ativos: {total_ativos} ({novos_ativos})\n"
        "🚑Internados: {internados} ({variacao_internados})\n"
        "🏥Em UCI: {uci} ({variacao_uci})\n"
        "\n"
        "👍Recuperados {perc_recuperados}% dos casos\n"
        "[1/3]")

    # Thread
    second_tweet = (
        "🔎Novos casos e novos óbitos por região:\n"
        "📍Norte: {novos_norte} | {novos_obitos_norte}\n"
        "📍Centro: {novos_centro} | {novos_obitos_centro}\n"
        "📍LVT: {novos_lvt} | {novos_obitos_lvt}\n"
        "📍Alentejo: {novos_alentejo} | {novos_obitos_alentejo}\n"
        "📍Algarve: {novos_algarve} | {novos_obitos_algarve}\n"
        "📍Açores: {novos_acores} | {novos_obitos_acores}\n"
        "📍Madeira: {novos_madeira} | {novos_obitos_madeira}\n"
        "[2/3]")

    third_tweet = (
        "📅 Últimas amostras [{dia_amostras}]\n"
        "🧪 PCR: {novas_amostras_pcr} | Antigénio: {novas_amostras_ag}\n"
        "{icon_positividade} Positividade 7 dias: {perc_positividade}%\n"
        "{icon_incidencia} Incidência nacional, 14 dias por 100k: {incidencia}\n"
        "\n"
        "Todos os dados e muito mais no nosso repositório:\n"
        "[3/3] {link_repo}")

    dados_para_tweets["link_repo"] = link_repo
    texto_tweet_1 = tweet_message.format(**dados_para_tweets)
    texto_tweet_2 = second_tweet.format(**dados_para_tweets)
    texto_tweet_3 = third_tweet.format(**dados_para_tweets)

    return texto_tweet_1, texto_tweet_2, texto_tweet_3

def tweet_len(s):
    # quick hack to kind of count emojis as 2 chars
    # not 100% to spec
    return sum( (2 if ord(c)>0x2100 else 1) for c in s)


if __name__ == '__main__':
    dados_extraidos = extrair_dados_ultimo_relatorio()
    texto_tweet_1, texto_tweet_2, texto_tweet_3 = compor_tweets(dados_extraidos)

    if consumer_key == 'DEBUG':
        print(f"Tweet 1 {tweet_len(texto_tweet_1)} '''\n{texto_tweet_1}\n'''")
        print(f"Tweet 2 {tweet_len(texto_tweet_2)} '''\n{texto_tweet_2}\n'''")
        print(f"Tweet 3 {tweet_len(texto_tweet_3)} '''\n{texto_tweet_3}\n'''")
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
