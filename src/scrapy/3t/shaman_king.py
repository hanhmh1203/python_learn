import scrapy
from scrapy import item
from scrapy.crawler import CrawlerProcess
from item_chapter import item_chapter
from pipelines import ScrapyPipeline


class OnePieceCrawlers(scrapy.Spider):
    name = 'shaman_king'
    start_urls = [
        'http://truyentranhtuan.com/shaman-king/'
    ]

    def parse(self, response):
        page = 'home_parse'
        filename = '%s.html' % page
        chapter = item_chapter()
        # list_chapter = list()
        pipe = ScrapyPipeline()
        for i in response.css("span.chapter-name"):
            __title = i.css("a::text").get()
            __link = i.css("a::attr(href)").get()
            chapter['title'] = __title
            chapter['link'] = __link
            # list_chapter.append(chapter)

            pipe.process_item(chapter)

        pipe.close_spider()
    # print(list_chapter

    def parse_chapter(self, i):
        chapter = item_chapter()
        chapter.title = i.css("a::text").get()
        chapter.link = i.css("a::attr(href)").get()
        # print(chapter)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(OnePieceCrawlers)

    process.start()
