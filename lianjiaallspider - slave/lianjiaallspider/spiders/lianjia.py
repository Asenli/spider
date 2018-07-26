import json

from scrapy_redis.spiders import RedisSpider
from scrapy import Selector, Request
from scrapy.spiders import Spider

from lianjiaallspider.items import LianJiaSpiderItem


class LianJiaSpider(RedisSpider):

    name = 'lianjia'
    #允许访问**域名
    redis_key = 'lianjia:start_urls'

    def parse(self,response):

        sel = Selector(response)
        lis = sel.xpath('//html/body/div[4]/div[1]/ul/li[@class="clear"]')

        for li in lis:
            item = LianJiaSpiderItem()
            item['house_code'] = li.xpath('./a/@data-housecode').extract()[0]
            if li.xpath('./a/img/@data-original').extract():
                item['img_src'] = li.xpath('./a/img/@data-original').extract()[0]
            if li.xpath('./div/div/a/text()').extract():
                item['title'] = li.xpath('./div/div/a/text()').extract()[0]
                item['estate'] = li.xpath('./div/div[2]/div/a/text()').extract()[0]
                item['info'] = li.xpath('./div/div[2]/div/text()').extract()
                item['price'] = li.xpath('./div[1]/div[6]/div[1]/span/text()').extract()[0] + li.xpath('./div[1]/div[6]/div[1]/text()').extract()[0]
                item['flood'] = li.xpath('./div/div[3]/div/text()').extract()
                item['tag'] = li.xpath('.//div[@class="tag"]/span/text()').extract()
                item['type'] = 'ershoufang'
                item['city'] = '成都'
                item['area'] = response.meta.get('name')
                yield item

        def split_house_info(self, info):
            return [i.strip() for i in info.split('|')[1:]]