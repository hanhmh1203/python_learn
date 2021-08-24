import scrapy
from scrapy import item
from scrapy.crawler import CrawlerProcess


class ReadToLeadSpider(scrapy.Spider):
    name = 'ReadToLead'
    start_urls = [
        'https://readtoolead.com/category/lifestyle/religion/'
    ]

    def parse(self, response):
        for i in response.css("div.td-block-span6"):
            for j in i.css("div.td-module-thumb"):
                __title = j.css("a::attr(title)").get()
                __link = j.css("a::attr(href)").get()
                __thumb = j.css("img").xpath("@src").extract_first()
                print(f"title {__title}")
                print(f"link {__link}")
                print(f"thumb {__thumb}")

            # chapter['title'] = __title
            # chapter['link'] = __link
        # pass

    def parse_chapter(self, i):
        pass


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ReadToLeadSpider)

    process.start()
