# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent
import json


class vidspider(object):
    def __init__(self):
        self.url = 'https://v.qq.com/x/search/?q={}'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def get_html(self, word):
        self.url = self.url.format(parse.quote(word))
        res = requests.get(url=self.url, headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        html = res.text.encode('utf-8')

        # print(type(html))
        # with open('1.txt', 'wb') as f:
        #     f.write(html)
        return html

    def parse_html(self, word):
        html = self.get_html(word)
        if html:
            p = etree.HTML(html)
            blocks = p.xpath(
                "//div[@class='result_item result_item_h']")
            text_list_dic = []
            for block in blocks:
                # 得到vid
                url = block.xpath("./h2[@class='result_title']/a/@href")[0]
                vid = url[-16:-5]
                # 得到head
                head = block.xpath("./a/img/@alt")[0].replace('\x05', '').replace('\x06', '')
                # 得到date
                date = block.xpath("./div[@class='result_info']/div[@class='info_line'][1]/div[@class='info_item info_item_odd']/span[@class='content']/text()")[0]
                # 得到组合src
                proturl = "http://vv.video.qq.com/getinfo?vids={}&platform=101001&charge=0&otype=json".format(vid)
                res = requests.get(url=proturl, headers=self.headers, timeout=5)
                res.encoding = 'utf-8'
                html = res.text
                # print(html[13:])
                portdic = json.loads(html[13:-1])
                # print(portdic)
                fn = portdic["vl"]["vi"][0]["fn"]
                fvkey = portdic["vl"]["vi"][0]["fvkey"]
                url0 = portdic["vl"]["vi"][0]["ul"]["ui"][0]["url"]
                src = url0 + fn + '?vkey=' + fvkey

                # 得到字典
                dic = {'head': head.strip('\n'),'date':date, 'vid': vid,'src':src}
                # print("字典：", dic)
                text_list_dic.append(dic)
            return text_list_dic

    def run(self, word):
        return self.parse_html(word)





