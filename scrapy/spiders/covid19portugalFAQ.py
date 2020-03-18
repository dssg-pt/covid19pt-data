import json
from w3lib.html import remove_tags
from scrapy.exceptions import CloseSpider
import scrapy
import time


class covid19portugalFAQ(scrapy.Spider):
    name = 'covid19portugal'

    start_urls = ['https://www.covid19portugal.pt/p/1/']

    def __init__(self):
        self.page = 1

        self.already_fetched = []

        self.file = open('../../extra/covid19portugalFAQ/covid19portugalFAQ.json', 'a+')

        self.file.writelines('[')

        super(covid19portugalFAQ, self).__init__()

    def parse(self, response):
        new_questions = 0

        for question_row in response.css('.t-row'):
            url = question_row.css('.clean-link::attr(href)').extract()
            url = url[len(url) - 1]

            if url not in self.already_fetched:
                yield scrapy.Request(
                    response.urljoin(url),
                    callback=self.parse_question_page
                )
                new_questions += 1

            self.already_fetched.append(url)

        self.page += 1

        #Going to FAQ next page
        next_page_url = 'https://www.covid19portugal.pt/p/' + str(self.page)
        request = scrapy.Request(url=next_page_url, callback=self.parse)

        if new_questions == 0:
            raise CloseSpider('All questions fetched')

        #Preventing multiple request at same time
        time.sleep(5)
        yield request


    def parse_question_page(self, response):
        self.file.writelines(json.dumps({
            'question': remove_tags(response.css('.title > p > strong').get()),
            'answer': remove_tags(response.css('.answer').get())
        }))

    def close(spider, reason):
        spider.file.writelines(']')