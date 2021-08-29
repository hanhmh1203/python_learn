import time

import scrapy
from scrapy import item
from scrapy.crawler import CrawlerProcess
from src.scrapy.journeyinlife.journey.journey.items import Item, JourneyItem
from scrapy import Selector


class JourneySpider(scrapy.Spider):
    name = 'journey_in_life'
    start_urls = [
        'https://www.journeyinlife.net/search/label/phrase'
    ]
    page_number = 3
    page_start = 1

    def parse(self, response):
        print(response.url)
        # number  = response.css('#page-rc-tooltip::text').extract_first()
        # number = response.css('div[id=\'page-rc-tooltip\']::text').get()
        # number = response.css('//div[contains(@id,\'page-rc-tooltip\')]').get()

        # text = response.xpath('//*[@id="page-rc-tooltip"]').getall()

        # text = response.css('#page-rc-tooltip > span:nth-child(1)').get()
        # print(f'text: {text}')
        # number = text.xpath('//*[starts-with(@id, \"page-rc-tooltip\")]').get()
        # print(f'vcl: {number}')
        # //*[@id="page-rc-tooltip"]/span[1]
        # number = response.css('//*[contains(text(), \'Page(1\')]').get()
        # print(number)

        # __content = response.xpath('//*[@id="main"]/div[1]')
        # print(f'size: {len(response.xpath("div.col-md-4"))}')
        # print(f'size: {len(__content.css("div.col-md-4"))}')
        # x = response.xpath("//div[@class='row']/div[contains(@class,'col-md-4')]").getall()
        # x = response.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/div[2]').getall()
        # sel = Selector(text='#main > div.widget.Blog > div:nth-child(2) > div.row')
        # a = sel.css('div')
        # x = response.xpath('//div[contains(@class,"col-md-4")]').get()
        # print(f'{x}')

        # response.css('a.has--img img').css("img").xpath("@alt").extract_first()
        count = 0
        for i in response.css('article.card'):
            if count == 12:
                break
            count += 1
            print(count)
            web_item = JourneyItem()
            __title = i.css("img").xpath("@alt").extract_first()
            __thumb = i.css("img").xpath("@data-src").extract_first()

            __link = i.css('div.title').css("a::attr(href)").get()
            print(__title)
            print(__link)
            # print(__thumb)

            #
            #     web_item['title'] = __title
            #     web_item['link'] = __link
            #     web_item['thumb'] = __thumb
            #     print(__title)
            # request = scrapy.Request(__link, self.parse_detail)
            # request.cb_kwargs['web_item'] = web_item
            # yield request
        if self.page_start == self.page_number:
            return
        time.sleep(5)
        self.page_start += 1
        next_url = self.start_urls[0] + f'?v=full&page={self.page_start}'
        yield scrapy.Request(next_url, callback=self.parse)

    # ?v = full & page = 1
    # print(web_item.link)
    # print(web_item.thumb)
    # j = i.css("div.td-module-thumb")
    # __title = j.css("a::attr(title)").get()
    # __link = j.css("a::attr(href)").get()
    # __thumb = j.css("img").xpath("@src").extract_first()

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

    # for i in response.css('div.td-pb-span12'):
    #     j = i.css("div.td-module-thumb")
    #     __title = j.css("a::attr(title)").get()
    #     __link = j.css("a::attr(href)").get()
    #     __thumb = j.css("img").xpath("@src").extract_first()
    #
    #     print(f"title {__title}")
    #     print(f"link {__link}")
    #     print(f"thumb {__thumb}")


def parse_detail(self, response, web_item):
    page = response.css('div.entry-body')
    __image = page.css("img").xpath("@src").extract_first()
    web_item['image'] = __image
    web_item['content'] = page.xpath("//div[@style=\"text-align: justify;\"]//text()").getall()
    print(web_item['title'])


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(JourneySpider)

    process.start()
