import json
import time

from scrapy import Spider, Selector, Request

# from qichezhijia.items import QichezhijiaItem
from qichezhijia.items import QichezhijiaItem


class CarHome(Spider):
    name = 'carhome'

    # all_url = 'https://k.autohome.com.cn/'
    page_url = 'https://dealer.autohome.com.cn/chengdu/0/0/0/0/{page}/1/0/0.html'

    # start_url = ['https://dealer.autohome.com.cn/chengdu']

    def start_requests(self):
        # 拿到所有页面的链接
        for page in range(1, 33):
            start_urls = self.page_url.format(page=page)
            yield Request(start_urls, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        all_lists_urls = sel.xpath('/html/body/div[2]/div[3]/ul/li/a/@href').extract()
        dealer_name = sel.xpath('/html/body/div[2]/div[3]/ul/li/ul/li[1]/a/span/text()').extract()
        # 拿到各经销商的单独链接
        for one_list_url in all_lists_urls:
            print('https:' + one_list_url)
            yield Request('https:' + one_list_url, callback=self.parse_dealer)

    def parse_dealer(self, response):
        # 解析每一页去拿到各种型号的价格
        # 这里必须解码后面拿到倒计时时间才会是红外
        sel = Selector(response)

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
