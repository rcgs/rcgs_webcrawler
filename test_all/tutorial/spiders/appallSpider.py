# coding: utf-8
import scrapy

from tutorial.items import appallItem
import re

class appallSpider(scrapy.Spider):
    name = "appall"
    allowed_domains = ["apple.com"]
    start_urls = [
        'https://itunes.apple.com/jp/app/pazuru-doragonzu/id493470467?mt=8',
        'https://itunes.apple.com/jp/app/line-dizuni-tsumutsumu/id724594093?mt=8',
        'https://itunes.apple.com/jp/app/abbies-dubai-777-casino-jackpot/id943047262?mt=8'
        ]


    def parse(self, response):
        for sel in response.xpath('//div[@id="main"]'):
            item = appallItem()
            item['title'] = self.fair_str(sel.xpath('//h1/text()').extract())
            item['developer'] = self.fair_str(sel.xpath('//div[@class="left"]/h2/text()').extract())
            item['description'] = self.fair_str(sel.xpath('//p[@itemprop="description"]/text()').extract())
            item['price'] = self.fair_str(sel.xpath('//div[@class="price"]/text()').extract())
            item['update'] = self.fair_str(sel.xpath('//li[@class="release-date"]/span/text()').extract())
            item['language'] = self.fair_str(sel.xpath('//li[@class="language"]/text()').extract())
            item['copyright'] = self.fair_str(sel.xpath('//li[@class="copyright"]/text()').extract())
            item['rating'] = self.fair_str(sel.xpath('//div[@class="app-rating"]/a/text()').extract())
            yield item

    def fair_str(self,string):
        #余分な文字列を削除

        string = re.sub(r"[~\[\']", "", str(string)) 
        string = re.sub(r"[\'\]$]", "", str(string))
        
        return string 

