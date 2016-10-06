import scrapy
import re
from webproject.items import WebProjectItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.depth import DepthMiddleware
from scrapy import log
import pymysql

class Webspider(CrawlSpider):






    name="itunespider"
    cursol = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                db="test_spider",
                charset ="utf8",
                autocommit=True
         ).cursor()
    allowed_domains = ["apple.com"]
    start_urls = ['https://itunes.apple.com/jp/genre/ios-gemu/id6014?mt=8&letter=A&page=1#page']

    allow_list = [r"/ios-gemu/"]
    deny_list = []
    #allow_list_parse = []
    # deny_list_parse = []


    rules = [
        Rule(LinkExtractor(allow=allow_list,deny=deny_list), callback='parse_data',follow=True)
    ]

    #rules = (
        #crawling rule
        #Rule(LinkExtractor(allow=allow_list,deny=deny_list),callback='parse_data',follow=True),
        #parsing page rule
        #Rule(LinkExtractor(allow=allow_list_parse,deny=deny_list_parse),callback='parse_data',follow=True)
    #)

    def parse_data(self,response):

        for sel in response.xpath('//div[@id="selectedgenre"]//div/ul/li'):
            item = WebProjectItem()
            #self.logger.info(response.url)
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()

            yield item

        #次のページへのリンクを取得するXpath
        xpath_next = ("/html/body[@class='geo-jp ac-platter-content lang-ja-jp lang-ja"
                      " ac-gn-current-music itunes-not-detected']"
                      "/div[@id='main']/div[@id='content']/div[@class='padder']"
                      "/div[@id='selectedgenre']/ul[@class='list paginate'][1]/li[19]/a/@href")
        nextpage = response.xpath(xpath_next)
        #log.msg("nextpage is" + nextpage, levenl=log.DEBUG)
        if nextpage :
            url = nextpage
            yield scrapy.Request(url, callback = self.parse_data)
