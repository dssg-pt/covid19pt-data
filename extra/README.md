# 🧱 Estrutura

O repositório está organizado da seguinte forma:
+ `noticias/`: Dados da categoria "Notícias"
+ `populacional/`: Dados da categoria "Populacional"
+ `saude/`: Dados da categoria "Saúde", até agora do Portal Transparência SNS. 
+ `medidas_governamentais/`: Dados das medidas governamentais ordenadas por data
+ `covid19portugalFAQ/`: Dados das perguntas mais frequentes do website oficial do ISPUP, covid19portugal.pt
+ `prociv/`: Dados das ocorrências da Proteção Civil. 

## 📰 Notícias

Contém: 

+ `download_listanoticias_publico.ipynb`: notebook Python para fazer download da data, título e descrição de notícias do Público relacionadas com Coronavírus.
+ `download_news_sample_observador.csv`: notebook Python para fazer download da data, título, descrição e conteúdo de notícias do Observador com a temática de Coronavírus.
com o coronavírus. (Um obrigado ao Rui Barros pela ajuda!)
+ `news_sample.csv`: Exemplo de um output do notebook de download de dados do Público.
+ `news_sample_observador.csv`: Exemplo de um output do notebook de download de dados do Observador.

## 🧑 Populacional

Contém dois datasets descritivos da população portuguesa, do PORDATA:

- [Densidade Populacional](https://www.pordata.pt/Municipios/Densidade+populacional-452)
- [Índice de dependência de idosos](https://www.pordata.pt/Municipios/%C3%8Dndice+de+depend%C3%AAncia+de+idosos-461)

É fornecido o ficheiro acima, para 2018, e uma versão simplificada em CSV, contendo as contagens para as regiões NUTS II (Usadas pela DGS para reportar os casos)

## 🏥 Saúde

Contém três datasets do Portal Transparência SNS24, na sua versão original e numa versão limpa e pré-processada por nós. O dicionário de dados encontra-se dentro de cada pasta, ficando a faltar os scripts para download a partir de uma API.

- [Atividade do Síndrome Gripal nos Cuidados de Saúde Primários](https://transparencia.sns.gov.pt/explore/dataset/atendimentos-nos-csp-gripe/export/?disjunctive.ars&sort=dia)
- [Atividade Operacional SNS24](https://transparencia.sns.gov.pt/explore/dataset/atividade-operacional-sns-24/table/?sort=periodo)
- [Atividade Prestação SNS 24 para a Síndrome Gripal](https://transparencia.sns.gov.pt/explore/dataset/atividade-prestacao-sns-24-para-a-sindrome-gripal/table/?sort=periodo)






## :bank: Medidas Governamentais

Contém csv contendo as medidas governamentais tomadas em cada data desde o início do surto. Baseado em:

- [Website da República Portuguesa](https://www.portugal.gov.pt/)
- [Pandemia de COVID-19 em Portugal](https://pt.m.wikipedia.org/wiki/Pandemia_de_COVID-19_em_Portugal)

## 🗃️ Proteção Civil

Contém um ficheiro com as ocorrências da Proteção Civil, extraída a partir da [Central de Dados](https://github.com/centraldedados/protecao_civil/). 

