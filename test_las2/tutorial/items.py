import scrapy

class appallItem(scrapy.Item):
    #Title DB
    
    OpenID =scrapy.Field()
    SerialID = scrapy.Field()
    GameCenter = scrapy.Field()
    title = scrapy.Field()
    developer = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    update = scrapy.Field()
    size = scrapy.Field()
    data_entity = scrapy.Field()
    language = scrapy.Field()
    copyright = scrapy.Field()
    icon_img = scrapy.Field()
    rating = scrapy.Field()
    rate_note = scrapy.Field()
    compatibility = scrapy.Field()
    link = scrapy.Field()
    
    #VersionDB
    OpenID = scrapy.Field()
    VerID = scrapy.Field()
    version = scrapy.Field()
    update_time = scrapy.Field()
    update_contents = scrapy.Field()


    #EvaluationDB
    OpenID = scrapy.Field()
    EvalID = scrapy.Field()
    current_eval = scrapy.Field()
    all_eval = scrapy.Field()
    top_accounting = scrapy.Field()
class metaItem(scrapy.Item):
    categoly = scrapy.Field()
    value = scrapy.Field()
