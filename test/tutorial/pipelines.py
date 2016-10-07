# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from  scrapy import log

class TutorialPipeline(object):
    def process_item(self, item, spider):
        log.msg("WORKING\n",level=log.DEBUG)

        return item
