# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QichezhijiaItem(scrapy.Item):

    collections = 'zhutui'
    main_car = scrapy.Field()   #热门车型
    main_prices = scrapy.Field()
    discounts_prices = scrapy.Field()
    car_type = scrapy.Field()
    car_emissions = scrapy.Field()


class DealerItem(scrapy.Item):

    collections = 'dealer'
    href = scrapy.Field()
    dealer_name = scrapy.Field()  # 哪家经销商


class EveryOneDetailItem(scrapy.Item):
    collections = 'EveyOne'

    produce_store = scrapy.Field()
    car_one_type = scrapy.Field()
    car_name = scrapy.Field()
    energy_type = scrapy.Field()
    max_kw = scrapy.Field()
    engine = scrapy.Field()
    gearbox = scrapy.Field()
    size = scrapy.Field()
    structure = scrapy.Field()
    max_speed = scrapy.Field()
    environmental = scrapy.Field()
