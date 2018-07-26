# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import redis
import scrapy
from scrapy.conf import settings

from lianjiaallspider.items import LianJiaSpiderItem


class LianjiaspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class PymongoLinjiaPipeline(object):

    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'],
                                   port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[LianJiaSpiderItem.collections]

    def process_item(self, item, spider):
        if isinstance(item, LianJiaSpiderItem):
            self.collection.update({'house_code':item['house_code']},{'$set':item}, True)
        return item


class MasterItem(scrapy.Item):
    url = scrapy.Field()


class MasterPipeline(object):
    def __init__(self):
        self.r = redis.Redis(host='127.0.0.1', port=6379)

    def process_item(self,item,spider):
        self.r.lpush('lianjia:start_urls', item['url'])
