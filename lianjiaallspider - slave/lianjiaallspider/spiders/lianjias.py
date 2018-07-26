# from scrapy import Selector, Request
# from scrapy.spiders import Spider
#
# from lianjiaallspider.items import LianJiaSpiderItem
#
#
# class LianJiaSpider(Spider):
#     name = 'lianjia'
#     #允许访问**域名
#     # allowed_domains =['lianjia.com']
#     start_lianjia_url = 'https://cd.lianjia.com/ershoufang/pg{page}'
#
#     def start_requests(self):
#         for i in range(1,101):
#             yield Request(self.start_lianjia_url.format(page=i))
#
#     def parse(self, response):
#         sel = Selector(response)
#
#         lis = sel.xpath('//html/body/div[4]/div[1]/ul/li[@class="clear"]')
#
#         for li in lis:
#             item = LianJiaSpiderItem()
#             item['house_code'] = li.xpath('./a/@data-housecode').extract()[0]
#             if li.xpath('./a/img/@data-original').extract():
#                 item['img_src'] = li.xpath('./a/img/@data-original').extract()[0]
#             if li.xpath('./div/div/a/text()').extract():
#                 item['title'] = li.xpath('./div/div/a/text()').extract()[0]
#                 item['estate'] = li.xpath('./div/div[2]/div/a/text()').extract()[0]
#                 item['info'] = li.xpath('./div/div[2]/div/text()').extract()
#                 item['price'] = li.xpath('./div[1]/div[6]/div[1]/span/text()').extract()[0] + li.xpath('./div[1]/div[6]/div[1]/text()').extract()[0]
#                 item['flood'] = li.xpath('./div/div[3]/div/text()').extract()
#                 item['tag'] = li.xpath('.//div[@class="tag"]/span/text()').extract()
#                 item['type'] = 'ershoufang'
#                 item['area'] = '成都'
#                 yield item
