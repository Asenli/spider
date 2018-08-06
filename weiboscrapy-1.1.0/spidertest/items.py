# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item, Field

import scrapy


class SpidertestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserItem(Item):
    #指明保存的表名
    collection = 'users'

    id = Field()
    name = Field()
    avatar = Field()
    cover = Field()
    gender = Field()
    description = Field()
    fans_count = Field()
    follows_count = Field()
    weibos_count = Field()
    verified = Field()
    verified_reason = Field()
    verified_type = Field()
    follows = Field()
    fans = Field()
    crawled_at = Field()


class UserRelationItem(Item):
    collection = 'users'

    id = Field()         # id是用户id
    follows = Field()   #用户关注列表
    fans = Field()      #粉丝列表


class WeiboItem(Item):
    collection = 'weibos'

    id = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    picture = Field()
    pictures = Field()
    source = Field()
    text = Field()
    raw_text = Field()
    thumbnail = Field()
    user = Field()
    created_at = Field()
    crawled_at = Field()


