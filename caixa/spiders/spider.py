import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import CcaixaItem
from itemloaders.processors import TakeFirst
import json

base = 'https://caixanoticias.caixa.gov.br/wp-json/wp/v2/posts?post-format_exclude=1309,1310,48,49,43,1311&per_page=12&page={}&order=desc'

class CcaixaSpider(scrapy.Spider):
    name = 'caixa'
    page = 1
    start_urls = [base.format(page)]

    def parse(self, response):
        data = json.loads(response.text)
        for index in range(len(data)):
            date = data[index]['date'].split('T')[0]
            title = data[index]['title']['rendered']
            content = data[index]['content']['rendered'] + data[index]['excerpt']['rendered']
            content = remove_tags(content)

            item = ItemLoader(item=CcaixaItem(), response=response)
            item.default_output_processor = TakeFirst()

            item.add_value('title', title)
            item.add_value('link', response.url)
            item.add_value('content', content)
            item.add_value('date', date)

            yield item.load_item()

        if not 'code' in data:
            self.page += 1
            yield response.follow(base.format(self.page), self.parse)