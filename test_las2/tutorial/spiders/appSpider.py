
from tutorial.items import appallItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from lxml import  html
import scrapy
from scrapy import log
import  re

class appSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["apple.com"]
    start_urls = [
        'https://itunes.apple.com/jp/genre/ios-gemu/id6014?mt=8&letter=A'
        #'https://itunes.apple.com/jp/genre/ios-gemu/id6014?mt=8&letter=B'
    ]
    #start_urls=["https://itunes.apple.com/jp/genre/ios-gemu/id6014?letter=R&mt=8&page=5"]
    #rules = [Rule(LinkExtractor(),callback='parse_data)]
    SerialID =None
    VerID = None
    EvalID = None
    table_name ="test_spider"
    start_number=0
    
    def __init__(self,*args,**kwargs):

        try:
            self.connection = pymysql.connect(
                host="localhost",
                user="root",
                password="root",
                db="test_spider",
                charset ="utf8",
                autocommit=True
            )
        except:
            log.msg("ERROR CONNECTING TO MYSQL", level=log.ERROR)
        
        sql = "SELECT COUNT(*) FROM %s ;" % self.table_name.encode("utf8")
        self.connection.execute(sql)
        result = self.fetch()
        self.start_number = result
    
        self.SerialID = self.get_ID(self.start_number,"AP")
        self.VerID = self.get_ID(self.start_number,"APV")
        self.EvalID = self.get_ID(self.start_number,"APE")

    def parse(self, response):
        for sel in response.xpath('//div[@id="selectedgenre"]//div/ul/li'):
            #self.logger.info(response.url)
            link = sel.xpath('a/@href').extract()
            link = self.fair_str(link)
            log.msg(link,_level=log.DEBUG)
            
            yield scrapy.Request(url=link,callback=self.parse_page)

        

        xpath_next = "//div[2]/ul[2]/li/a[@class='paginate-more']/@href"
        nextpage = response.xpath(xpath_next).extract()
        next=nextpage
        #log.msg("nextpage is" + nextpage, levenl=log.DEBUG)
        if nextpage :
            log.msg("nextpage", level = log.DEBUG)
            next_url = str(nextpage)
            next_url = re.sub(r"[~\[\']", "", next_url)
            next_url = re.sub(r"[\'\]$]", "", next_url)
            request = scrapy.Request(url=next_url)
            yield request

 



    def parse_page(self, response):
        #for sel in response.xpath('//div[@id="main"]'):
        #self.SerialID=self.get_ID(100,"AP") 
        item = appallItem()
            #titleDB

            #正規表現抽出
        item["OpenID"] = self.fair_str(response.url,self.regexp,(r"[a-z]{2}[0-9]+"))
        #return item
        item['SerialID'] = self.SerialID()
                #有無判定
        item['GameCenter']=self.fair_str(response.xpath('//div[2]/div/div/div/div/div[@class="gc-badge app-badge"]/span/text()').extract(),self.check_none)
        item['title'] = self.fair_str(response.xpath('//h1/text()').extract())
        item['developer'] = self.fair_str(response.xpath('//div[@class="left"]/h2/text()').extract())
        item['description'] = self.fair_str(response.xpath('//p[@itemprop="description"]/text()').extract())
        item['price'] = self.fair_str(response.xpath('//div[@class="price"]/text()').extract())
        item['update'] = self.fair_str(response.xpath('//li[@class="release-date"]/span/text()').extract())
            #正規表現抽出
        item['size'] = self.fair_str(response.xpath('//div/div/div[3]/div[1]/ul/li[5]/text()').extract(),self.regexp,r"[0-9]+[.][0-9]+|[0-9]+")
            #正規表現抽出
        item['data_entity'] = self.fair_str(response.xpath('//div/div/div[3]/div[1]/ul/li[5]/text()').extract(),self.regexp,r"[A-Za-z]+$")
        item['language'] = self.fair_str(response.xpath('//li[@class="language"]/text()').extract())
        item['copyright'] = self.fair_str(response.xpath('//li[@class="copyright"]/text()').extract())
        item['icon_img'] = self.fair_str(response.xpath('//div[@class="lockup product application"]/a/div[@class="artwork"]/meta/@content').extract(),self.check_none)
        #//div[5]/div/div/div/div/div/a/div[@class="artwork"]/img/@src
        
        item['rating'] = self.fair_str(response.xpath('//div[@class="app-rating"]/a/text()').extract())
#有無判定
     
        item['rate_note'] = self.fair_str(response.xpath('//body/div/div/div/div/div/div/div/ul[@class="list app-rating-reasons"]/li/text()').extract(),self.check_none)
        item['compatibility'] = self.fair_str(response.xpath('//p/span[@itemprop="operatingSystem"]/text()').extract())
        item['link'] = self.fair_str(response.url)

        #VersionDB
        item['VerID']=self.VerID()
        #item['version']
        #item['update_time']
        #item['update_contents']

        #EvaluationDB
        item['EvalID']=self.EvalID()
                #有無判定
        item['current_eval'] = self.fair_str(response.xpath('//div[3]/div[2]/div[@class ="rating"][1]/@aria-label[1]').extract(),self.check_none)
                #有無判定
        item['all_eval'] = self.fair_str(response.xpath('//div[3]/div[2]/div[@class ="rating"][2]/@aria-label[1]').extract(),self.check_none)
                #有無判定
        item['top_accounting'] = self.fair_str(response.xpath('//div[@class="extra-list in-app-purchases"]/ol/li/span/text()').extract(),self.check_none)
                #yield item
        return item




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

    def fair_str(self,string,function=None,regexp=None):
        #余分な文字列を削除

        string = re.sub(r"[~\[\']", "", str(string)) 
        string = re.sub(r"[\'\]$]", "", str(string))
        
        if function is not None and regexp is None:#追加の関数があった場合
            string = function(string) 
        

        if function is not None and regexp is not None:#正規表現のパターンが入力されていた場合
            string =function(string,regexp)
        

        return string 

    def check_none(self,string):
        log.msg(string,level=log.DEBUG)
        if string is "":
            string = ";none"
        log.msg(string,level=log.DEBUG)
        return string

    def regexp(self,string,regexp):
        log.msg(string,level=log.DEBUG)
        match = re.search(regexp,string)
        if match is not None:
            string = match.group()
        
        return string
    
    def get_ID(self,last_number,IDname="AP"):#一つ前の件数を取得し代入
        num =last_number
        ID_type = IDname
        
        def closure():
            nonlocal num
            nonlocal ID_type

            max_size = 12 #桁の最大数 
            num +=1 #インクリメント

            strnum = str(num)#文字列として保存
            for var in range(0,max_size - len(strnum)): #最大桁数と現在の数字の桁数の差分の回数繰り返し、0で埋める
                strnum = "0" + strnum

            ID = ID_type+strnum
            return ID


        return closure