import scrapy
from scrapy import item
from scrapy.crawler import CrawlerProcess


class JourneySpider(scrapy.Spider):
    name = 'journey_in_life'
    start_urls = [
        'https://readtoolead.com/category/lifestyle/religion/'
    ]

    def parse(self, response):
        for i in response.css("div.td-block-span6"):
            j = i.css("div.td-module-thumb")
            __title = j.css("a::attr(title)").get()
            __link = j.css("a::attr(href)").get()
            __thumb = j.css("img").xpath("@src").extract_first()

            # print(f"title {__title}")
            # print(f"link {__link}")
            # print(f"thumb {__thumb}")
            # __author = i.css("span.td-post-author-name").css('a::text').get()
            # __date = i.css('time::attr(datetime)').get()
            # print(f"author {__author}")
            # print(f"date {__date} \n")
        # chapter['title'] = __title
        # chapter['link'] = __link
        # pass

        for i in response.css('div.td-pb-span12'):
            j = i.css("div.td-module-thumb")
            __title = j.css("a::attr(title)").get()
            __link = j.css("a::attr(href)").get()
            __thumb = j.css("img").xpath("@src").extract_first()

            print(f"title {__title}")
            print(f"link {__link}")
            print(f"thumb {__thumb}")

    def parse_chapter(self, i):
        pass


# td_module_mx5 td-animation-stack td-big-grid-post-0 td-big-grid-post td-big-thumb
# td_module_mx6 td-animation-stack td-big-grid-post-1 td-big-grid-post td-small-thumb
if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ReadToLeadSpider)

    process.start()
