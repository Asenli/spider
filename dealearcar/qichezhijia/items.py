# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QichezhijiaItem(scrapy.Item):


    collections = 'zhutui'
    dealer_name = scrapy.Field()  # 哪家经销商

    main_car = scrapy.Field()   #热门车型
    main_prices = scrapy.Field()
    discounts_prices = scrapy.Field()
    car_type = scrapy.Field()
    car_emissions = scrapy.Field()


