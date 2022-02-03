# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent
import json

class spider(object):
    def __init__(self):
        self.url = 'http://www.35yao.com/invest/search.php?kw={}'
        # 青霉素 'http://www.35yao.com/invest/search.php?kw=%E9%9D%92%E9%9C%89%E7%B4%A0'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def get_html(self, word):
        self.url = self.url.format(parse.quote(word))
        # print(self.url)
        res = requests.get(url=self.url, headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        html = res.text
        '''
        with open('2.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        '''
        return html

    def parse_html(self, word):
        html = self.get_html(word)
        if html:
            p = etree.HTML(html)
            blocks = p.xpath(
                "//tr/td[3]/ul")
            blocks_list_dic = []
            for block in blocks:
                iname = block.xpath("./li[1]/a/strong[@class='px14']//text()")
                iname = ''.join(iname)
                icompany = block.xpath("./li[3]/a/text()")[0]
                iurl = block.xpath("./li[1]/a/@href")[0]
                dic = {"name": iname, "company": icompany, "url": iurl}
                blocks_list_dic.append(dic)
                # print(dic)
            return blocks_list_dic

    def run(self, word):
        result = self.parse_html(word)
        return result
        # print(result)

