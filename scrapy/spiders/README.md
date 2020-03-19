
# Web Scraper para FAQ ISPUP

Requirements:

    1. scrapy

Spiders localizados em: scrapy/spiders

Para iniciar o scrap das perguntas e resposta do https://www.covid19portugal.pt/:

    $ cd scrapy/spiders
    $ runspider covid19portugalFAQ.py 


Será gerado uma lista em formato json em: extra/covid19portugalFAQ/covid19portugalFAQ.json
