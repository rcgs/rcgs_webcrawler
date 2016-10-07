
from tutorial.items import appItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from lxml import  html
import scrapy
from scrapy import log
import  re

class appSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["apple.com"]
    start_urls = ['https://itunes.apple.com/jp/genre/ios-gemu/id6014?mt=8&letter=A']
    #start_urls=["https://itunes.apple.com/jp/genre/ios-gemu/id6014?letter=R&mt=8&page=5"]
    #rules = [Rule(LinkExtractor(),callback='parse_data)]

    Rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[@class='paginate-more']",)), callback="parse", follow=True),)

    def parse(self, response):
        site = html.fromstring(response.body_as_unicode())
        item = appItem()
        item["link"]=response.url


        xpath_next = "//div[2]/ul[2]/li/a[@class='paginate-more']/@href"
        nextpage = response.xpath(xpath_next).extract()
        item["next"]=nextpage
        #log.msg("nextpage is" + nextpage, levenl=log.DEBUG)
        if nextpage :
            log.msg("nextpage", level = log.DEBUG)
            next_url = str(nextpage)
            next_url = re.sub(r"[~\[\']", "", next_url)
            next_url = re.sub(r"[\'\]$]", "", next_url)
            request = scrapy.Request(url=next_url)
            yield request

        yield item




        #for sel in response.xpath('//div[@id="selectedgenre"]//div/ul/li'):
        #    item = appItem()
        #    item['title'] = sel.xpath('a/text()').extract()
        #    item['link'] = sel.xpath('a/@href').extract()

        #    log.msg("WORKING\n", level=log.DEBUG)

        #    yield item

        """
        scrapyのデータを時価で取得すると['   ']という感じで行末行頭に余分な文字が
        発生するため削除を行う関数
        """

    def fair_str(string)
        string = re.sub(r"[~\[\']", "", string) 
        string = re.sub(r"[\'\]$]", "", string)
        return str(string) #unicodeに変換して返す
