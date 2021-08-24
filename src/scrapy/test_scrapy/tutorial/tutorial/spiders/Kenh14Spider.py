import scrapy

import datetime


class Kenh14Spider(scrapy.Spider):
    name = "kenh14"

    def start_requests(self):
        urls = [
            'http://kenh14.vn/fashion/lam-dep.chn',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = {

            'title': response.css('.kbw-content,  h1.kbwc-title::text').extract_first().strip(),

            'author': response.css('.kbw-content .kbwc-meta .kbwcm-author::text').extract_first().strip(),

            'source': 'kenh14',

            'content': response.css('.klw-new-content').extract_first().strip(),

            'link': response.request.url,

            'modifiedDate': datetime.now()

        }

        print(str(result))

        for next_page in response.css('.kbw-content a::attr(href)').extract():
            yield response.follow(next_page, self.parse)
