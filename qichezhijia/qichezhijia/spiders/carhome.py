import json
import time

from scrapy import Spider, Selector, Request
from scrapy.http import HtmlResponse
from selenium import webdriver

from qichezhijia.items import QichezhijiaItem


class CarHome(Spider):
    name = 'carhome'
    # allowed_domains = ['www.autohome.com.cn']
    # start_urls = ['https://www.autohome.com.cn/chengdu/']
    all_url = 'https://k.autohome.com.cn/'

    start_user_pages = ['suva01/', 'suva1/', 'suvb1/', 'suvc1/', 'suvd1/', 'a001/', 'a01/', 'a1/', 'b1/', 'c1/', 'd1/',
                        'mpv1/', 's1/', 'p1', 'mb1']

    def start_requests(self):
        for paaa in self.start_user_pages:
            time.sleep(1)
            yield Request(self.all_url + paaa, callback=self.parse)
            time.sleep(1)

    def parse(self, response):
        sel = Selector(response)
        # 车型名

        name = sel.xpath('/html/body/div[2]/div[2]/div/div/div[2]/dl/dd/ul/li/div[2]/a/text()').extract()
        img = sel.xpath('/html/body/div[2]/div[2]/div/div/div[2]/dl/dd/ul/li/div[1]/a/img/@src').extract()

        details = sel.xpath('/html/body/div[2]/div[2]/div/div/div[2]/dl/dd/ul/li/div[2]/a/@href').extract()
        scores = sel.xpath('/html/body/div[2]/div[2]/div/div/div[2]/dl/dd/ul/li/div[3]/a/span[2]/text()').extract()
        people = sel.xpath('/html/body/div[2]/div[2]/div/div/div[2]/dl/dd/ul/li/div[4]/a/text()').extract()

        # print(name,details_urls,score,people)

        for n,d, s, p,i in zip(name,details, scores, people,img):
            item = QichezhijiaItem()
            # print(n,self.all_url + d, s + '分', p + '人')
            item['name'] = n
            item['img'] = i
            item['details'] = self.all_url + d
            item['scores'] = s
            item['people'] = p
            item['type'] = '热门车型'
            yield item
    