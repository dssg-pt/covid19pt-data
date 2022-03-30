# Imports
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys
from pathlib import Path
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
POP_PT = 10_347_892  # 2020 = 10_298_253  # 2019 = 10_295_909

# vacinas_detalhe
POP_ARS = {
    'norte':     3_582_397,  # 3_559_952,  # 3_568_835,  # 3.57M
    'centro':    1_659_900,  # 1_657_882,  # 1_650_394,  # 1.65M
    'lvt':       3_681_581,  # 3_683_759,  # 3_674_534,  # 3.67M
    'alentejo':    468_802,  #   462_569,  #   466_690,  # 0.46M
    'algarve':     467_495,  #   437_971,  #   438_406,  # 0.44M
    'madeira':     251_060,  #   253_924,  #   254_254,  # 0.25M
    'acores':      236_657,  #   242_202,  #   242_796,  # 0.24M
}

POP_IDADE = {
    '0_9':     433332 + 461299,  #  0-04 + 05-09
    '10_19':   507646 + 549033,  # 10-14 + 15-19
    '20_29':   544575 + 547505,  # 20-24 + 25-29
    '30_39':   571355 + 679093,  # 30-34 + 35-39
    '40_49':   792670 + 782555,  # 40-44 + 45-49
    '50_59':   747581 + 734540,  # 50-54 + 55-59
    '60_69':   672758 + 620543,  # 60-64 + 65-69
    '70_79':   544016 + 429107,  # 70-74 + 75-79
    '80_plus': 352218 + 316442,  # 80-84 + 85 ou mais
}

# TENDENCIA = ["↑", "↓"]
TENDENCIA = ["⬈", "⬊", "⬌"]

# ---
flatten = lambda t: [item for sublist in t for item in sublist]
idades = ['0_9', '10_19', '20_29', '30_39', '40_49', '50_59', '60_69', '70_79', '80_plus']

idades_diff = 1 # 2 se faltar um dia de dados

# Note: to debug the tweet content without publishing, use
# export TWITTER_CONSUMER_KEY=DEBUG
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
if consumer_key != 'DEBUG':
    import tweepy
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    access_token = os.environ['TWITTER_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

def r(valor, decimals=0):
    return round(float(valor), decimals) if decimals else round(float(valor))

def f(valor):
    """ format number in portuguese locale """
    valor = valor if type(valor) == int else float(valor)
    return format(valor, ",").replace(".","!").replace(",",".").replace("!",",")

# ajuste incidencia7 para ficar comparável com 14
INCIDENCIA7_14=True

# usa incidencia 7 dias quando a variação é muito volátil
INCIDENCIA7=True

# ICONS[key] = [5 values]
ICONS = {}
# OMS recomenda 5 ; Portugal tem média 10 ; picos da onda passaram 15
ICONS["positividade"] = [10, 5, 4, 1]
# incidencia 14 dias por 100k
ICONS["incidencia14"] = [480, 240, 120, 60]
# incidencia 7 dias por 100k (metade de incidencia14)
ICONS["incidencia7"] = ICONS["incidencia14"] if INCIDENCIA7_14 else [r(x/2) for x in ICONS["incidencia14"]]
# confirmados = incidencia / 14 dias / 100k * população
ICONS["confirmados"] = [r(float(x) / 14 / 100000 * POP_PT ) for x in ICONS["incidencia14"]]

def icon(valor, tipo):
    return (
        "🟤" if valor >= ICONS[tipo][0] else  # ≥ 10 | ≥ 480
        "🔴" if valor >= ICONS[tipo][1] else  # ≥  5 | ≥ 240
        "🟠" if valor >= ICONS[tipo][2] else  # ≥  4 | ≥ 120
        "🟡" if valor >= ICONS[tipo][3] else  # ≥  1 | ≥  60
        "🟢"                                  # <  1 | <  60
    )

def calc_tendencia(df, diff=7, skip=1, name="", OFFSET=0):
    """ Retorna a diferença da média 7 dias do ultimo dia para o dia anterior """
    IGNORE = 1
    df = df.diff(diff) if diff else df
    val1, val2 = float(df[-1 - OFFSET]), float(df[-1 - OFFSET - skip])
    diff = val1 - val2
    if diff == 0: return 0

    # perc = 100.0 * abs(diff) / min(abs(val1), abs(val2)) if val1 and val2 else 0
    perc = 100.0 * abs(diff) / abs(val2) if val2 else IGNORE
    if perc < IGNORE:
        print(f"name={name} val1={val1} val2={val2} diff={diff} perc={perc}")
    return diff if perc >= IGNORE else 0

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

def extrair_dados_ultimo_relatorio(OFFSET=0):
    dados_extraidos={}

    #Aceder ao csv
    path = Path(__file__).resolve().parents[2]
    file=path / 'data.csv'
    df = pd.read_csv(file,parse_dates=[0],index_col=[0],infer_datetime_format=True,skip_blank_lines=False,dayfirst=True)
    df.fillna(value=0)

    # Formatar datas
    hoje=df.data_dados[-1 - OFFSET]
    dados_extraidos["dia"] = datetime.strptime(hoje, '%d-%m-%Y %H:%M').strftime("%d %b %Y")

    ##Casos
    dados_extraidos["total_casos"]=r(df.confirmados[-1 - OFFSET])
    dados_extraidos["novos_casos"]=r(df.confirmados.diff()[-1 - OFFSET])
    dados_extraidos["novos_casos_tendencia"]=calc_tendencia(df.confirmados, name='novos_casos', OFFSET=OFFSET)

    ##Óbitos
    dados_extraidos["total_obitos"]=r(df.obitos[-1 - OFFSET])
    dados_extraidos["novos_obitos"]=r(df.obitos.diff()[-1 - OFFSET])
    dados_extraidos["novos_obitos_tendencia"]=calc_tendencia(df.obitos, name='obitos', OFFSET=OFFSET)

    ##Internados
    dados_extraidos["internados"] = r(df.internados[-1 - OFFSET])
    dados_extraidos["internados_tendencia"] = calc_tendencia(df.internados, name='internados', OFFSET=OFFSET)
    dados_extraidos["variacao_internados"]=r(df.internados.diff()[-1 - OFFSET])

    dados_extraidos["uci"] = r(df.internados_uci[-1 - OFFSET])
    dados_extraidos["uci_tendencia"] = calc_tendencia(df.internados_uci, name='uci', OFFSET=OFFSET)
    dados_extraidos["variacao_uci"]=r(df.internados_uci.diff()[-1 - OFFSET])

    ##Ativos
    dados_extraidos["total_ativos"]=r(df.ativos[-1 - OFFSET])
    dados_extraidos["total_ativos_tendencia"]=calc_tendencia(df.ativos, name='ativos', OFFSET=OFFSET)
    dados_extraidos["novos_ativos"]=r(df.ativos.diff()[-1 - OFFSET])
    #Percentagem total
    dados_extraidos["perc_ativos"] = r(float(100*df.ativos[-1 - OFFSET]/df.confirmados[-1 - OFFSET]),1)

    ##Recuperados
    if np.isnan(df.recuperados[-1 - OFFSET]):
        dados_extraidos["total_recuperados"]=0
        dados_extraidos["total_recuperados_tendencia"]=0
        dados_extraidos["novos_recuperados"]=0
        dados_extraidos["perc_recuperados"]=0
    else:
        dados_extraidos["total_recuperados"]=r(df.recuperados[-1 - OFFSET])
        dados_extraidos["total_recuperados_tendencia"]=calc_tendencia(df.recuperados, name='recuperados', OFFSET=OFFSET)
        dados_extraidos["novos_recuperados"]=r(df.recuperados.diff()[-1 - OFFSET])
        #Percentagem total
        dados_extraidos["perc_recuperados"] = r(float(100*df.recuperados[-1 - OFFSET]/df.confirmados[-1 - OFFSET]),1)

    ## Regiões
    for k in ['lvt', 'norte', 'algarve', 'centro', 'alentejo', 'acores', 'madeira']:
        k2 = k if k in ['acores', 'madeira'] else f"ars{k}"
        dados_extraidos[f"novos_casos_{k}"]=r(df[f"confirmados_{k2}"].diff()[-1 - OFFSET])
        dados_extraidos[f"novos_casos_{k}_tendencia"]=calc_tendencia(df[f"confirmados_{k2}"], name=f'novos_casos_{k}', OFFSET=OFFSET)
        dados_extraidos[f"novos_obitos_{k}"]=r(df[f"obitos_{k2}"].diff()[-1 - OFFSET])
        dados_extraidos[f"novos_obitos_{k}_tendencia"]=calc_tendencia(df[f"obitos_{k2}"], name=f'novos_obitos_{k}', OFFSET=OFFSET)
        if INCIDENCIA7:
            incidencia14 = 2 * float(df[f"confirmados_{k2}"].diff(7)[-1 - OFFSET]) * 100 * 1000 / POP_ARS[k]
        else:
            incidencia14 = float(df[f"confirmados_{k2}"].diff(14)[-1 - OFFSET]) * 100 * 1000 / POP_ARS[k]
        dados_extraidos[f"incidencia_{k}"] = r(incidencia14, 0)
        dados_extraidos[f"incidencia_{k}_tendencia"] = calc_tendencia(df[f"confirmados_{k2}"], 14, name=f'incidencia_{k}', OFFSET=OFFSET)
        dados_extraidos[f"icon_{k}"] = icon(incidencia14, "incidencia14")

    ## Idades
    try:
        for k in idades:
            df[f"confirmados_{k}"] = df[f"confirmados_{k}_f"] + df[f"confirmados_{k}_m"]
            k2 = k
            dados_extraidos[f"novos_casos_{k}"]=r(df[f"confirmados_{k2}"].diff(idades_diff)[-1 - OFFSET])
            dados_extraidos[f"novos_casos_{k}_tendencia"]=calc_tendencia(df[f"confirmados_{k2}"], skip=idades_diff, name=f'novos_casos_{k}', OFFSET=OFFSET)
            if INCIDENCIA7:
                more_offset = 0
                while np.isnan(df[f"confirmados_{k2}"].diff(7)[-1 - OFFSET - more_offset]):
                    more_offset += 1
                incidencia14 = 2 * float(df[f"confirmados_{k2}"].diff(7)[-1 - OFFSET - more_offset]) * 100 * 1000 / POP_IDADE[k]
            else:
                more_offset = 0
                while np.isnan(df[f"confirmados_{k2}"].diff(14)[-1 - OFFSET - more_offset]):
                    more_offset += 1
                incidencia14 = float(df[f"confirmados_{k2}"].diff(14)[-1 - OFFSET - more_offset]) * 100 * 1000 / POP_IDADE[k]
            dados_extraidos[f"incidencia_{k}"] = r(incidencia14, 0)
            dados_extraidos[f"incidencia_{k}_tendencia"] = calc_tendencia(df[f"confirmados_{k2}"], 14, skip=idades_diff, name=f'incidencia_{k}', OFFSET=OFFSET)
            dados_extraidos[f"icon_{k}"] = icon(incidencia14, "incidencia14")
    except ValueError as e:
        print(f"WARN: sem idades confirmados {e}")
        dados_extraidos["sem_idades_confirmados"] = True
    try:
        for k in idades:
            df[f"obitos_{k}"] = df[f"obitos_{k}_f"] + df[f"obitos_{k}_m"]
            k2 = k
            dados_extraidos[f"novos_obitos_{k}"]=r(df[f"obitos_{k2}"].diff(idades_diff)[-1 - OFFSET])
            dados_extraidos[f"novos_obitos_{k}_tendencia"]=calc_tendencia(df[f"obitos_{k2}"], skip=idades_diff, name=f'novos_obitos_{k}', OFFSET=OFFSET)
    except ValueError as e:
        print(f"WARN: sem idades obitos {e}")
        dados_extraidos["sem_idades_obitos"] = True

    # diff e médias 7 e 14 dias
    for k in [7, 14]:
        df[f"confirmados{k}"] = df.confirmados.diff(k)
        df[f"obitos{k}"] = df.obitos.diff(k)

    #Aceder ao csv amostras
    path = Path(__file__).resolve().parents[2]
    file=path / 'amostras.csv'
    df_amostras = pd.read_csv(file,parse_dates=[0],index_col=[0],infer_datetime_format=True,skip_blank_lines=False,dayfirst=True)
    df_amostras.fillna(value=0)

    # diff e médias 7 dias
    for k in [7]:
        df_amostras[f"amostras{k}"] = df_amostras.amostras.diff(k)

    # amostras
    dados_extraidos["dia_amostras"] = df_amostras.index[-1 - OFFSET].strftime("%d %b")
    dados_extraidos["novas_amostras_pcr"] = r(df_amostras.amostras_pcr_novas[-1 - OFFSET])
    dados_extraidos["novas_amostras_pcr_tendencia"] = calc_tendencia(df_amostras.amostras_pcr_novas, name='novas_amostras_pcr', OFFSET=OFFSET)
    dados_extraidos["novas_amostras_ag"] = r(df_amostras.amostras_antigenio_novas[-1 - OFFSET])
    dados_extraidos["novas_amostras_ag_tendencia"] = calc_tendencia(df_amostras.amostras_antigenio_novas, name='novas_amostras_ag', OFFSET=OFFSET)

    more_offset = 0
    while len(df[df.index == df_amostras.index[-1 - OFFSET - more_offset].strftime("%Y-%m-%d")]) == 0:
        more_offset += 1
    positividade7 = 100 * float(df[df.index == df_amostras.index[-1 - OFFSET - more_offset].strftime("%Y-%m-%d")].confirmados7[-1]) / float(df_amostras.amostras7[-1 - more_offset])
    dados_extraidos["perc_positividade7"] = r(positividade7, 1)
    dados_extraidos["icon_positividade7"] = icon(positividade7, "positividade")
    positividade7_anterior = 100 * float(df[df.index == df_amostras.index[-1 - OFFSET - more_offset -1].strftime("%Y-%m-%d")].confirmados7[-1]) / float(df_amostras.amostras7[-1 - more_offset -1])
    dados_extraidos["perc_positividade7_anterior"] = r(positividade7_anterior, 1)

    for d in [14, 7]:
        for k in ["confirmados", "obitos"]:
            # val = float(df[f"{k}{d}"][-1 - OFFSET])  # total 14/7 dias, não médias
            val = float(df[f"{k}{d}"][-1 - OFFSET] / d)  # média diária 14/7 dias
            dados_extraidos[f"novos_{k}{d}"] = r(val)
            if k == 'confirmados': dados_extraidos[f"icon_{k}{d}"] = icon(val, "confirmados")
            dados_extraidos[f"novos_{k}{d}_tendencia"] = calc_tendencia(df[f"{k}{d}"], diff=None, name=f'novos_{k}{d}', OFFSET=OFFSET)

        val = float(df[f"confirmados{d}"][-1 - OFFSET] * 100 * 1000 / POP_PT)
        if INCIDENCIA7_14:
            val = val * 2 if d == 7 else val  # not 100% correct, but easier to compare with incidencia 14
        dados_extraidos[f"incidencia{d}"] = r(val, 0)
        dados_extraidos[f"icon_incidencia{d}"] = icon(val, f"incidencia{d}")
        dados_extraidos[f"incidencia{d}_tendencia"] = calc_tendencia(df[f"confirmados{d}"], diff=None, name=f'incidencia_{d}', OFFSET=OFFSET)

    #----

    cols_obitos_lt50 = flatten([ [f"obitos_{x}_f", f"obitos_{x}_m"] for x in idades[0:5]])
    obitos_lt50 = r(df.loc[:, cols_obitos_lt50].diff(idades_diff).sum(axis=1).tail(1))
    obitos_lt50_7d = r(df.loc[:, cols_obitos_lt50].diff(7).sum(axis=1).tail(1))
    dados_extraidos["novos_obitos_lt50"] = obitos_lt50
    dados_extraidos["novos_obitos_lt50_tendencia"] = calc_tendencia(df.loc[:, cols_obitos_lt50].diff(idades_diff).sum(axis=1), diff=None, skip=idades_diff, name='novos_obitos_lt50', OFFSET=OFFSET)
    dados_extraidos["novos_obitos_lt50_7d"] = obitos_lt50_7d
    dados_extraidos["novos_obitos_lt50_7d_tendencia"] = calc_tendencia(df.loc[:, cols_obitos_lt50].diff(7).sum(axis=1), diff=None, skip=idades_diff, name='novos_obitos_lt50_7d', OFFSET=OFFSET)

    # -----
    # cols_confirmados_lt60 = flatten([ [f"confirmados_{x}_f", f"confirmados_{x}_m"] for x in idades[0:7]])
    # cols_confirmados_ge60 = flatten([ [f"confirmados_{x}_f", f"confirmados_{x}_m"] for x in idades[6:]])

    # confge60 = r(df.loc[:, cols_confirmados_lt60].diff(idades_diff).sum(axis=1).tail(1))
    # conflt60 = r(df.loc[:, cols_confirmados_ge60].diff(idades_diffc).sum(axis=1).tail(1))

    # -----

    for key in dados_extraidos.keys():
        valor = dados_extraidos[key]
        if type(valor) not in [int, float]:
            if not type(valor) in [str, bool]:
                print(f"skip {key} {valor} {type(valor)}")
            continue
        dados_extraidos[key] = f(valor)
        if (key.startswith('variacao_') or key.startswith('novos_') or key.startswith('novas_')) and valor > 0:
            dados_extraidos[key] = "+" + dados_extraidos[key]

        if key.startswith('perc_'):
            dados_extraidos[key] = f"{dados_extraidos[key]}%"
        if f"{key}_tendencia" in dados_extraidos:
            tendencia = dados_extraidos[f"{key}_tendencia"]
            if tendencia > 0: dados_extraidos[key] += TENDENCIA[0]
            elif tendencia < 0: dados_extraidos[key] += TENDENCIA[1]
            elif valor != 0 and tendencia == 0 and len(TENDENCIA) > 2: dados_extraidos[key] += TENDENCIA[2]
        elif f"{key}_anterior" in dados_extraidos:
            valor_anterior = dados_extraidos[f"{key}_anterior"]
            if valor > valor_anterior: dados_extraidos[key] += TENDENCIA[0]
            elif valor < valor_anterior: dados_extraidos[key] += TENDENCIA[1]

    return dados_extraidos

def compor_tweets(dados_para_tweets):

    sem_idades_confirmados = dados_para_tweets.get("sem_idades_confirmados", False)
    sem_idades_obitos = dados_para_tweets.get("sem_idades_obitos", False)
    sem_idades = sem_idades_confirmados # and sem_idades_obitos

    dados_para_tweets["num_tweets"] = 3 if sem_idades else 4

    # Main tweet
    tweet_message = (
        "🆕Dados #COVID19PT 🇵🇹 a {dia}:\n"
        "\n"
        "🫂Novos casos: {novos_casos} | Total: {total_casos}\n"
        "🪦Novos óbitos: {novos_obitos} | Total: {total_obitos}\n"
    )
    if not sem_idades_obitos:
        tweet_message += (
            "⚱️Óbitos ≤49 anos: {novos_obitos_lt50} | 7d: {novos_obitos_lt50_7d}\n"
        )
    tweet_message += (
        "\n"
        "🦠Ativos: {total_ativos} ({novos_ativos})\n"
        "🚑Internados: {internados} ({variacao_internados})\n"
        "🏥UCI: {uci} ({variacao_uci})\n"
        "\n"
        "👍Recuperados: {perc_recuperados} dos casos\n"
    )
    tweet_message += (
        "\n"
        "[1/{num_tweets}]"
    )

    second_tweet = (
        "🔎Por Região incidência, novos casos, óbitos:\n"
        "{icon_norte}Norte {incidencia_norte} {novos_casos_norte} {novos_obitos_norte}\n"
        "{icon_centro}Centro {incidencia_centro} {novos_casos_centro} {novos_obitos_centro}\n"
        "{icon_lvt}LVT {incidencia_lvt} {novos_casos_lvt} {novos_obitos_lvt}\n"
        "{icon_alentejo}Alentejo {incidencia_alentejo} {novos_casos_alentejo} {novos_obitos_alentejo}\n"
        "{icon_algarve}Algarve {incidencia_algarve} {novos_casos_algarve} {novos_obitos_algarve}\n"
        "{icon_madeira}Madeira {incidencia_madeira} {novos_casos_madeira} {novos_obitos_madeira}\n"
        "{icon_acores}Açores {incidencia_acores} {novos_casos_acores} {novos_obitos_acores}\n"
        "\n"
        "[2/{num_tweets}]"
    )
    if tweet_len(second_tweet) >= 280:
        third_tweet = second_tweet.replace(':', '')

    if sem_idades:
        third_tweet = ""
    else:
        third_tweet = "🔎Por Idade incidência, novos casos"
        if sem_idades_obitos:
            third_tweet += ":\n"
        else:
            third_tweet += ", óbitos:\n"
        for k in idades:
            k2 = "00" if k == "0_9" else "80" if k == "80_plus" else k[0:2]
            icon = f"icon_{k}"
            incidencia = f"incidencia_{k}"
            novos_casos = f"novos_casos_{k}"
            novos_obitos = f"novos_obitos_{k}"
            icon = "{"+icon+"}"
            icon = "" # 2022.01.20 tweet excede 280 caracteres e a incidencia está entre 1.500 e 10.000
            third_tweet += icon+k2+" {"+incidencia+"} {"+novos_casos+"}"
            if sem_idades_obitos:
                third_tweet += "\n"
            else:
                third_tweet += " {"+novos_obitos+"}\n"
        third_tweet += (
            "\n"
            "[3/{num_tweets}]"
        )


    fourth_tweet = (
        "🔎Nacional: incidência, média diária novos casos, óbitos:\n"
        "{icon_incidencia14}14 dias: {incidencia14} {novos_confirmados14} {novos_obitos14}\n"
        "{icon_incidencia7}7 dias eq: {incidencia7} {novos_confirmados7} {novos_obitos7}\n"
        "\n"
        "📅Amostras [{dia_amostras}]:\n"
        "🧪PCR: {novas_amostras_pcr} | Antigénio: {novas_amostras_ag}\n"
        "{icon_positividade7}Positividade (7d): {perc_positividade7}\n"
        "\n"
        "[{num_tweets}/{num_tweets}]"
        "\n"
        "\n➕Todos os dados em: {link_repo}"
    )

    if sem_idades:
        third_tweet, fourth_tweet = fourth_tweet, ""

    dados_para_tweets["link_repo"] = link_repo
    texto_tweet_1 = tweet_message.format(**dados_para_tweets)
    texto_tweet_2 = second_tweet.format(**dados_para_tweets)
    texto_tweet_3 = third_tweet.format(**dados_para_tweets)
    texto_tweet_4 = fourth_tweet.format(**dados_para_tweets)

    return texto_tweet_1, texto_tweet_2, texto_tweet_3, texto_tweet_4

def tweet_len(s):
    # quick hack to kind of count emojis as 2 chars - not 100% to spec
    return sum( (2 if ord(c)>0x2100 else 1) for c in s)


if __name__ == '__main__':
    OFFSET = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    dados_extraidos = extrair_dados_ultimo_relatorio(OFFSET)
    texto_tweet_1, texto_tweet_2, texto_tweet_3, texto_tweet_4 = compor_tweets(dados_extraidos)

    if consumer_key == 'DEBUG':
        print(f"Tweet 1 {tweet_len(texto_tweet_1)} '''\n{texto_tweet_1}\n'''\n")
        print(f"Tweet 2 {tweet_len(texto_tweet_2)} '''\n{texto_tweet_2}\n'''\n")
        print(f"Tweet 3 {tweet_len(texto_tweet_3)} '''\n{texto_tweet_3}\n'''\n")
        if texto_tweet_4:
            print(f"Tweet 4 {tweet_len(texto_tweet_4)} '''\n{texto_tweet_4}\n'''\n")
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
        tweet2 = api.update_status(texto_tweet_2, tweet1Id)
        tweet2Id = tweet2.id_str
        tweet3 = api.update_status(texto_tweet_3, tweet2Id)
        if texto_tweet_4:
            tweet3Id = tweet3.id_str
            tweet4 = api.update_status(texto_tweet_4, tweet3Id)
    except Exception as e:
        print("Erro a enviar o tweet")
        print(e)
        pass
