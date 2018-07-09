import json
import re
import time

from scrapy import Spider, Selector, Request

# from qichezhijia.items import QichezhijiaItem
from qichezhijia.items import QichezhijiaItem, DealerItem, EveryOneDetailItem


class CarHome(Spider):
    name = 'carhome'

    one_url_base = 'https://dealer.autohome.com.cn'
    page_url = 'https://dealer.autohome.com.cn/chengdu/0/0/0/0/{page}/1/0/0.html'

    detail_url = 'https://dealer.autohome.com.cn/Price/_SpecConfig?DealerId={id1}&SpecId={id2}'
    # start_url = ['https://dealer.autohome.com.cn/chengdu']

    def start_requests(self):
        # 拿到所有页面的链接
        for page in range(1, 33):
            start_urls = self.page_url.format(page=page)
            print(start_urls)

            yield Request(start_urls, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        all_lists_urls = sel.xpath('/html/body/div[2]/div[3]/ul/li/a/@href').extract()
        #经销商名字
        dealer_name = sel.xpath('/html/body/div[2]/div[3]/ul/li/ul/li[1]/a/span/text()').extract()

        # 拿到各经销商的单独链接
        for one_list_url in all_lists_urls:
            # print('https:' + one_list_url)

            yield Request('https:' + one_list_url, callback=self.parse_dealer,
                          meta={'dealer_name': dealer_name,'href': 'https:' + one_list_url})


    def parse_dealer(self, response):
        #主推车型页面

        # 解析每一页去拿到各种型号的价格
        # 这里必须解码后面拿到倒计时时间才会是红外
        sel = Selector(response)
        item = DealerItem()
        item['dealer_name'] = response.meta.get('dealer_name')
        item['href'] = response.meta.get('href')
        yield item
        # 经销商主推车型
        main_car = sel.xpath('//*[@id="ztcx"]/div[2]/div/dl/dd/div[1]/a/text()').extract()
        # 主推车所有促销价格
        main_prices = sel.xpath('//*[@id="ztcx"]/div[2]/div/dl/dd/div[2]/p[1]/span/text()').extract()
        # 优惠价格
        discounts_prices = sel.xpath('//*[@id="ztcx"]/div[2]/div/dl/dd/div[2]/p[2]/span/text()').extract()
        # 车型
        car_type = sel.xpath('//*[@id="ztcx"]/div[2]/div/dl/dd/div[4]/p[1]/text()').extract()
        # 排量
        car_emissions = sel.xpath('//*[@id="ztcx"]/div[2]/div/dl/dd/div[4]/p[2]/text()').extract()

        for m, p, d, t, e in zip(main_car, main_prices, discounts_prices, car_type, car_emissions):
            item = QichezhijiaItem()
            item['main_car'] = m
            item['main_prices'] = p
            item['discounts_prices'] = d
            item['car_type'] = t
            item['car_emissions'] = e

            yield item
        #每辆车子详情的链接
        car_type_urls = sel.xpath('//*[@id="ztcx"]/div[2]/div/dl/dd/div[1]/a/@href').extract()

        for type_url in car_type_urls:
            car_type_url = self.one_url_base + type_url
            yield Request(car_type_url,callback=self.page_one_detail)

        #取出两个id参数 # 拼接单个车子详情页面ajax加载的信息表单页面链接再去解析表单
        id1_url = sel.xpath('//*[@id="ztcx"]/div[2]/div/dl/dt/a/@href').extract()
        if id1_url:
            for id_url in id1_url:

                id1 = id_url.split('/')[1]
                id2 = id_url.split('_')[1].split('.')[0]
                one_url = self.detail_url.format(id1=id1, id2=id2)
                yield Request(one_url, callback=self.parse_detail)

    def page_one_detail(self,response):
        # 单个车子页面详情包含了车况的
        item = EveryOneDetailItem()
        sel = Selector(response)
        #车名
        item['car_name'] = sel.xpath("//p[@class='topname-text']/text()").extract()[0]
        #裸车价价格
        # price = sel.xpath("/html/body/div[2]/div[3]/div/div/div[2]/ul[1]/li[1]/p[2]/span/text()").extract()[0]
        # #促销价
        # price_sale = sel.xpath("/html/body/div[2]/div[3]/div/div/div[2]/ul[1]/li[2]/p[2]/span/text()").extract()[0]
        yield item


    def parse_detail(self,response):
        #每个车的详情信息
        item = EveryOneDetailItem()
        sel = Selector(response)

        #厂商
        item['produce_store'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[1]/td/text()').extract()[0]
        #级别
        item['car_one_type'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[1]/td[2]/text()').extract()[0]
        #能源类型
        item['energy_type'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[2]/td[1]/text()').extract()[0]
        #最大功率
        item['max_kw'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[3]/td[2]/text()').extract()[0]
        #发动机马力
        item['engine'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[4]/td[2]/text()').extract()[0]
        #变速箱
        item['gearbox'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[5]/td[1]/text()').extract()[0]
        #长宽高
        item['size'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[5]/td[2]/text()').extract()[0]
        #车身结构
        item['structure'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[6]/td[1]/text()').extract()[0]
        #最高时速
        item['max_speed'] = sel.xpath('//*[@id="tab-10"]/div[2]/table/tbody/tr[6]/td[2]/text()').extract()[0]
        #环保标准
        item['environmental'] = sel.xpath('//*[@id="tab-10"]/div[6]/table/tbody/tr[11]/td[1]/text()').extract()[0]
        yield item

