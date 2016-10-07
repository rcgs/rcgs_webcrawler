import scrapy

class appItem(scrapy.Item):
    #title = scrapy.Field()
    link = scrapy.Field()
    next = scrapy.Field()

class metaItem(scrapy.Item):
    categoly = scrapy.Field()
    value = scrapy.Field()
