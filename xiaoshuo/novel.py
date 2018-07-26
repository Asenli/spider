import asyncio
import re
import urllib.request
from urllib import parse


import aiohttp

import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


def get_index_html(url):
    # 首页解析页面
    rep = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(rep, timeout=180)
    return res.read().decode('utf8')


# def title_urls(url2):
#     #获取到所有标题
#     all_titles = re.findall(r'<li><a href="(.*?)" target="_blank" title=".*?', url2)
#     title_url = all_titles[:8]
#     return title_url

def next_urls(title_urls):
    # 获取翻页
    detail_urls = []
    htmls = get_index_html(title_urls)
    pages_pattern = re.findall(r'<option value=\'/soft/.*?/(.*?)\'.*?>第.*?页</option>', htmls)
    for every_url in pages_pattern:
        detail_urls.append('https://www.xuanshu.com/soft/sort0{}/{}'.format(i, every_url))
    return detail_urls


def title_url(detail_url):
    # 每一页 的所有小说
    htmls = get_index_html(detail_url)
    pattern = re.compile(
        r'<li>.*?<div class="s">.*?target="_blank">(.*?)</a><br />大小：(.*?)<br>.*?</em><br>更新：(.*?)</div>.*?<a href="(.*?)"><img.*?>(.*?)</a>.*?<div class="u">(.*?)</div>',
        re.S)
    items = re.findall(pattern, htmls)
    every_one_list = []
    for every_one in items:
        every_one_url = every_one[3]
        every_one_list.append('https://www.xuanshu.com{}'.format(every_one_url))
    # 获取每本书最终的下载链接页面
    return every_one_list


async def downlade(url):
    # 下载
    html = get_index_html(url)
    down_urls = re.findall(r'<a class="downButton" href=\'(.*?)\'', html)
    #小说下载链接
    # <a class="downButton" href=\'http://dzs.xuanshu.com/txt/强者恒强.txt\' title="《强者恒强》全集txt下载">
    txts = down_urls[1]
    # 获取txt下载链接并解码
    # *txt_url, name = txts.split('/')
    #小说名字
    txt_name =  (re.findall(r'<a class="downButton" .*? title="(.*?)">Txt格式下载</a>', html))[0]
    try:
        async with aiohttp.ClientSession() as session:
            # 伪装浏览器
            headers = {

                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',

                'Cache-Control': 'max-age=0',

                'Connection': 'keep-alive',

                'Referer': 'http://www.baidu.com/',

                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(txts) as resp:
                print(await resp.text())
    except:
        pass


if __name__ == '__main__':
    # urll = 'https://www.xuanshu.com{}'

    loop = asyncio.get_event_loop()
    for i in range(1, 11):
        url = 'https://www.xuanshu.com/soft/sort0%d/' % i
        detail_urls = next_urls(url)
        # print(detail_url)
        for every_one_page in detail_urls:
            #所有的页
            all_one_url = title_url(every_one_page)
            tasks = [downlade(one_url) for one_url in all_one_url]
            loop.run_until_complete(asyncio.wait(tasks))


