# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianJiaSpiderItem(scrapy.Item):
    collections = 'ershoufang'
    house_code = scrapy.Field()
    img_src = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    info = scrapy.Field()
    estate = scrapy.Field()
    price =scrapy.Field()
    flood =scrapy.Field()
    tag = scrapy.Field()

    type = scrapy.Field()   #新房/二手
    city = scrapy.Field()   #城市
    area = scrapy.Field()   #成都 区域