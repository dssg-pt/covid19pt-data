
import pandas as pd
from datetime import datetime
import emoji
import os
from pathlib import Path
import tweepy 
  
# Login

consumer_key ="mfSrAmZfZ481JXLQL2VlWLPFB"

consumer_secret ="GUNBMljUWNgQvJLHQrTJ4vbpldzRuMWVyNSFpsuKm3F3FErT2k"

access_token ="1267747147472089088-lawkJn3xrI5trNyRWcFZDKvZE9lVQX"

access_token_secret ="dwJrTwzIaq76duxp2j7ghp1gvp0TmTse6s3uNxtgAJ1mS"

#consumer_key = os.environ['TWITTER_CONSUMER_KEY']
#consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
#access_token = os.environ['TWITTER_ACCESS_TOKEN']
#access_token_secret = os.environ['TWITTER_ACCESS_SECRET']
  
# authentication of consumer key and secret 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
# authentication of access token and secret 
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth) 
  
# extrair dados
path = Path(__file__).resolve().parents[2]
file=path / 'data.csv'

df = pd.read_csv(file,parse_dates=[0],index_col=[0],infer_datetime_format=True,skip_blank_lines=False,dayfirst=True)
df.fillna(value=0)


# Get date and format
hoje=df.data_dados[-1]
hoje_datetime = datetime.strptime(hoje, '%d-%m-%Y %H:%M').strftime("%d %b %Y")

##Número total de casos
total_casos=df.confirmados[-1]

#novos casos
novos_casos=int(df.confirmados.diff()[-1])
aumento_casos=round(novos_casos/total_casos*100,1)

##Óbitos
total_obitos=df.obitos[-1]
novos_obitos=int(df.obitos.diff()[-1])
aumento_obitos=round(novos_obitos/total_casos*100,2)

##Internados
novos_obitos=int(df.obitos.diff()[-1])
aumento_obitos=round(novos_obitos/total_casos*100,2)

##Internados
internados = int(df.internados[-1])
variacao_internados=int(df.internados.diff()[-1])

uci = int(df.internados_uci[-1])
variacao_uci=int(df.internados_uci.diff()[-1])


##Recuperados
#novos recuperados
total_recuperados=int(df.recuperados[-1])
novos_recuperados=int(df.recuperados.diff()[-1])
aumento_recuperados=round(novos_recuperados/total_casos*100,1)
#Percentagem total
perc_recuperados = round(df.recuperados.tail(1).values[0]/df.confirmados.tail(1).values[0]*100,1)

## Regiões
novos_lvt=int(df.confirmados_arslvt.diff()[-1])
novos_norte=int(df.confirmados_arsnorte.diff()[-1])
novos_algarve=int(df.confirmados_arsalgarve.diff()[-1])
novos_centro=int(df.confirmados_arscentro.diff()[-1])
novos_alentejo=int(df.confirmados_arsalentejo.diff()[-1])
novos_acores=int(df.confirmados_acores.diff()[-1])
novos_madeira=int(df.confirmados_madeira.diff()[-1])

## Compose messages
link_repo = "https://github.com/dssg-pt/covid19pt-data"

# Main tweet
tweet_message = ((emoji.emojize(":NEW_button:"))+" Dados #COVID19PT atualizados [" + hoje_datetime + "]:  \
\n "+(emoji.emojize(":round_pushpin:"))+"Novos casos: " + str(novos_casos) + "(↑" + str(aumento_casos) +"%)"+ " | Total: "+ str(total_casos)+\
"\n "+(emoji.emojize(":round_pushpin:"))+"Novos óbitos: " + str(novos_obitos) + "(↑" + str(aumento_obitos) +"%)"+ " | Total: "+ str(total_obitos)+ \
"\n "+(emoji.emojize(":round_pushpin:"))+"Novos recuperados: " + str(novos_recuperados) + "(↑" + str(aumento_recuperados) +"%)"+ " | Total: "+ str(total_obitos)+\
"\n "+(emoji.emojize(":round_pushpin:"))+"Em Internamento: " + str(internados) + "(" + str(variacao_internados) +")"+ \
"\n "+(emoji.emojize(":round_pushpin:"))+"Em UCI: " + str(uci) + "(" + str(variacao_uci) +")"+ \
"\n \n"+(emoji.emojize(":thumbs_up:"))+" Recuperados " + str(perc_recuperados)+"% dos casos  \n[1/3]" \
)

# Thread

second_tweet = ((emoji.emojize(":magnifying_glass_tilted_right:"))+"  Novos casos por região: \
\n "+(emoji.emojize(":round_pushpin:"))+" Norte: " + str(novos_norte) 
+ "\n "+(emoji.emojize(":round_pushpin:"))+" Centro: " + str(novos_centro) 
+ "\n "+(emoji.emojize(":round_pushpin:"))+" LVT: " + str(novos_lvt) 
+ "\n "+(emoji.emojize(":round_pushpin:"))+" Alentejo: " + str(novos_alentejo) 
+ "\n "+(emoji.emojize(":round_pushpin:"))+" Algarve: " + str(novos_algarve)
+ "\n "+(emoji.emojize(":round_pushpin:"))+" Açores: " + str(novos_acores)
+ "\n "+(emoji.emojize(":round_pushpin:"))+" Madeira: " + str(novos_madeira) + "\n [2/3] ")

third_tweet = ("Dados nacionais, por concelho e de amostras actualizados no nosso GitHub \n [3/3]" + link_repo)


# Update status and create thread

tweet1 = api.update_status(status = tweet_message)
tweet1Id = tweet1.id_str

tweet2=api.update_status(second_tweet, tweet1Id)
tweet2Id = tweet2.id_str

api.update_status(third_tweet, tweet2Id)