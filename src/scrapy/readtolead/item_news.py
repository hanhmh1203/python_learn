from scrapy.item import Item, Field


class ItemNews(Item):
    title = Field()
    link = Field()
    thumb = Field()
    content_vn = Field()
    content_en = Field()

