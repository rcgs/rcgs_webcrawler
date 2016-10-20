import scrapy


class appSpider(scrapy.Spider):
    name = "meta"
    allowed_domains = ["apple.com"]
    start_urls = [
        'https://itunes.apple.com/jp/app/777-my-slots-machines-rich/id1059176208?mt=8'
        ]


    def parse(self, response):
        for sel in response.xpath('//div'):
            item = metaItem()
            item['title'] = sel.xpath('/span').extract()
            item['link'] = sel.xpath('a/@href').extract()
            yield item