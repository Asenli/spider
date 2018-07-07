# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QichezhijiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collections = 'koubei'
    type = scrapy.Field()   #热门车型
    name = scrapy.Field()
    img = scrapy.Field()
    details = scrapy.Field()
    scores = scrapy.Field()
    people = scrapy.Field()

