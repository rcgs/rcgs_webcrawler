# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from  scrapy import log

class TutorialPipeline(object):
    def __init__(self):
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




    def process_item(self, item, spider):
        log.msg("WORKING\n",level=log.DEBUG)

        self.cursol=self.connection.cursor()

        title = str(item["title"])
        title = re.sub(r"[~\[\']", "", title)
        title = re.sub(r"[\'\]$]", "", title)
        link = str(item["link"])
        link = re.sub(r"[~\[\']", "", link)
        link = re.sub(r"[\'\]$]", "", link)

        sql = ('INSERT INTO spider_test (title, link) VALUES ("%s","%s");' % (title,link)).encode("utf8")
        log.msg(str(item["title"]) + "\n", lvel=log.INFO)
        log.msg(str(item["link"]) + "\n", level=log.INFO)


        self.cursol.execute(sql)
        self.cursol.close()
        return item
