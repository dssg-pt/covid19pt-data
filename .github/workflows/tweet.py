
import pandas as pd
from datetime import datetime
import os
from pathlib import Path
import tweepy 

link_repo = "https://github.com/dssg-pt/covid19pt-data"
  
# Login
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_SECRET']

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


    ##Número total de casos
    dados_extraidos["total_casos"]=df.confirmados[-1]

    #novos casos
    dados_extraidos["novos_casos"]=int(df.confirmados.diff()[-1])
    dados_extraidos["aumento_casos"]=round(dados_extraidos["novos_casos"]/dados_extraidos["total_casos"]*100,1)

    ##Óbitos
    dados_extraidos["total_obitos"]=df.obitos[-1]
    dados_extraidos["novos_obitos"]=int(df.obitos.diff()[-1])
    dados_extraidos["aumento_obitos"]=round(dados_extraidos["novos_obitos"]/dados_extraidos["total_casos"]*100,2)


    ##Internados
    dados_extraidos["internados"] = int(df.internados[-1])
    dados_extraidos["variacao_internados"]=int(df.internados.diff()[-1])

    dados_extraidos["uci"] = int(df.internados_uci[-1])
    dados_extraidos["variacao_uci"]=int(df.internados_uci.diff()[-1])


    ##Recuperados
    #novos recuperados
    dados_extraidos["total_recuperados"]=int(df.recuperados[-1])
    dados_extraidos["novos_recuperados"]=int(df.recuperados.diff()[-1])
    dados_extraidos["aumento_recuperados"]=round(dados_extraidos["novos_recuperados"]/dados_extraidos["total_casos"]*100,1)
    #Percentagem total
    dados_extraidos["perc_recuperados"] = round(df.recuperados.tail(1).values[0]/df.confirmados.tail(1).values[0]*100,1)

    ## Regiões
    dados_extraidos["novos_lvt"]=int(df.confirmados_arslvt.diff()[-1])
    dados_extraidos["novos_norte"]=int(df.confirmados_arsnorte.diff()[-1])
    dados_extraidos["novos_algarve"]=int(df.confirmados_arsalgarve.diff()[-1])
    dados_extraidos["novos_centro"]=int(df.confirmados_arscentro.diff()[-1])
    dados_extraidos["novos_alentejo"]=int(df.confirmados_arsalentejo.diff()[-1])
    dados_extraidos["novos_acores"]=int(df.confirmados_acores.diff()[-1])
    dados_extraidos["novos_madeira"]=int(df.confirmados_madeira.diff()[-1])

    return dados_extraidos


def compor_tweets(dados_para_tweets):

    # Main tweet

    tweet_message = ("🆕 Dados #COVID19PT atualizados [{dia}]:\n"
"📍Novos casos: {novos_casos}(↑{aumento_casos}%) | Total: {total_casos}\n"
"📍Novos óbitos: {novos_obitos}(↑{aumento_obitos}%) | Total: {total_obitos} \n"
"📍Novos recuperados: {novos_recuperados}(↑{aumento_recuperados}%) | Total: {total_recuperados} \n" 
"📍Em Internamento: {internados}({variacao_internados})\n"
"📍Em UCI: {uci}({variacao_uci})\n"
"\n"
"👍 Recuperados {perc_recuperados}% dos casos [1/3]")

    # Thread
    second_tweet = "🔎 Novos casos por região: \n \
📍 Norte: {novos_norte} \n \
📍 Centro: {novos_centro} \n \
📍 LVT: {novos_lvt} \n \
📍 Alentejo: {novos_alentejo} \n \
📍 Algarve: {novos_algarve} \n \
📍 Açores: {novos_acores} \n \
📍 Madeira: {novos_madeira} \n \
[2/3]"

    third_tweet = ("Dados nacionais, por concelho e de amostras actualizados no nosso GitHub \n [3/3]" + link_repo)

    texto_tweet_1 = tweet_message.format(**dados_para_tweets)
    texto_tweet_2 = second_tweet.format(**dados_para_tweets)

    return texto_tweet_1, texto_tweet_2, third_tweet



if __name__ == '__main__':
    api = autenticar_twitter()
    dados_extraidos = extrair_dados_ultimo_relatorio()    
    texto_tweet_1, texto_tweet_2, texto_tweet_3 = compor_tweets(dados_extraidos)

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
    



