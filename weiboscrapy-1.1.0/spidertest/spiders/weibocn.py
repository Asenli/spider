import json
import re
import time

from scrapy import Request, Spider

from spidertest.items import UserItem, UserRelationItem, WeiboItem


class WeiboSpider(Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    #用户详情api
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&type=uid&containerid=100505{uid}'
    #关注列表api
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followerstagrecomm_-_{uid}&since_id={page}'
    #粉丝列表api
    fan_url =  'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'
    #微博列表api
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
    start_users = ['3261134763', '1230663070', '1234552257', '1730077315', '1656565920' , '1701887397']

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        """对用户信息进行解析"""
        """
        因为上面拼接的是接口地址  点text可以解析出其为字典形式 
        但是中文没有解译 所以用json.loads加载--json数据  
        将其转换成可视化的中文
        """
        result = json.loads(response.text)

        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()
            field_map = {
                  'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
                'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
            }
            for field, attr in field_map.items():
                user_item[field] = user_info.get(attr)

            yield user_item

            #关注
            uid = user_info.get('id')
            yield Request(self.follow_url.format(uid=uid,page=1),callback=self.parse_follows,meta={'page':1,'uid': uid})
            #粉丝数
            yield Request(self.fan_url.format(uid=uid,page=1), callback=self.parse_fans,
                          meta={'page':1, 'uid': uid})

            #微博文章
            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                          meta={'page': 1,'uid': uid})


    def parse_follows(self,response):
        """

        :param response: Response对象 解析用户关注
        :return:
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get('card_group'):
        #解析用户
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            #关注列表
            user_relation_item = UserRelationItem()
            follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')} for follow in follows]
            user_relation_item['id'] = uid
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []
            yield user_relation_item

            #下一页关注人
            page = response.meta.get('page')  + 1
            yield  Request(self.follow_url.format(uid=uid, page=page),
                           callback=self.parse_follows, meta={'page': page, 'uid': uid})

    def parse_fans(self, response):
        """
        解析用户粉丝
        :param response: Response对象
        :return:
        """

        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
                result.get('data').get('cards')[-1].get(
                        'card_group'):
            # 解析用户
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            # 粉丝列表
            user_relation_item = UserRelationItem()
            fans = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan in
                    fans]
            user_relation_item['id'] = uid
            user_relation_item['fans'] = fans
            user_relation_item['follows'] = []
            yield user_relation_item
            # 下一页粉丝
            page = response.meta.get('page') + 1
            yield Request(self.fan_url.format(uid=uid, page=page),
                          callback=self.parse_fans, meta={'page': page, 'uid': uid})


    def parse_weibos(self, response):
        """
        解析微博列表
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    weibo_item = WeiboItem()
                    field_map = {
                        'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                        'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
                        'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                        'thumbnail': 'thumbnail_pic',
                    }
                    for field, attr in field_map.items():
                        weibo_item[field] = mblog.get(attr)
                    weibo_item['user'] = response.meta.get('uid')
                    yield weibo_item
            # 下一页微博
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos,
                          meta={'uid': uid, 'page': page})


