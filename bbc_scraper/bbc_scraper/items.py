import scrapy

class BbcHeadlineItem(scrapy.Item):
    headline = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()
    category = scrapy.Field()
