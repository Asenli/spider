# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

from qichezhijia.items import QichezhijiaItem, DealerItem, EveryOneDetailItem


class QichezhijiaPipeline(object):
    def process_item(self, item, spider):
        return item


class PymongocarhomePipeline(object):

    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        #两个表的collection
        self.collection = db[DealerItem.collections]
        self.collection2 = db[QichezhijiaItem.collections]
        self.collection3 = db[EveryOneDetailItem.collections]

    def process_item(self,item,spider):
        #经销商数据保存
        if isinstance(item, DealerItem):
            self.collection.update({'dealer_name': item['dealer_name']}, {'$set': item}, True)
            return item

        elif isinstance(item,QichezhijiaItem):
            #主营车信息保存   用上面的collection2
            self.collection2.update({'main_car': item['main_car']}, {'$set': item}, True)
            return item
        elif isinstance(item,EveryOneDetailItem):
            #保存每辆车信息
            self.collection3.update({'car_name':item['car_name']},{'$set': item},True)
            return item