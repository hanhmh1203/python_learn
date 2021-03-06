import shub as shub
import scrapy
from scrapy import item
from scrapy.crawler import CrawlerProcess
import ItemQuotes


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # start_urls = [
    #     'http://quotes.toscrape.com/tag/humor/',
    # ]
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            test_item = ItemQuotes.ItemQuote()
            test_item['text'] = quote.css('span.text::text').get()
            test_item['author'] = quote.css('small.author::text').get(),
            test_item['tags'] = quote.css('div.tags a.tag::text').getall(),
            print(test_item.text)
            print(test_item.author)
            print(test_item.tags)
            # yield {
            #     'text': quote.css('span.text::text').get(),
            #     'author': quote.css('small.author::text').get(),
            #     'tags': quote.css('div.tags a.tag::text').getall(),
            # }


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(QuotesSpider)

    process.start()
