import json

from scrapy import Selector, Request
from scrapy.spiders import Spider

from lianjiaallspider.items import LianJiaSpiderItem
from lianjiaallspider.pipelines import MasterItem


class LianJiaSpider(Spider):
    name = 'lianjia'

    #允许访问**域名
    # allowed_domains =['lianjia.com']
    domains_url = 'https://cd.lianjia.com'
    start_lianjia_url = 'https://cd.lianjia.com/ershoufang'

    def start_requests(self):

        yield Request(self.start_lianjia_url)

    def parse(self, response):
        sel = Selector(response)

        ershoufang_area = sel.xpath('//div[@data-role="ershoufang"]')
        area_info = ershoufang_area.xpath('./div/a')
        for area in area_info:
            area_href = area.xpath('./@href').extract()[0]
            area_name = area.xpath('./text()').extract()[0]

            yield Request(self.domains_url + area_href,
                          callback=self.parse_house_info,
                          meta={'name': area_name,'href': area_href})

    def parse_house_info(self, response):

        sel = Selector(response)
        page_box = sel.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        total_page = json.loads(page_box[0]).get('totalPage')
        for i in range(1,int(total_page)+1):
            item = MasterItem()
            item['url'] = self.domains_url + response.meta.get('href') + 'pg' + str(i)
            yield item

