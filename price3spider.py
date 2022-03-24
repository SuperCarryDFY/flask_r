# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent


class pricespider(object):
    def __init__(self):
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def getinfo(self,iurl):
        res = requests.get(url=iurl,headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        html = res.text
        info = {}
        if html:
            p = etree.HTML(html)
            blocks = p.xpath('//*[@id="detail"]/div[2]/div[2]/div[1]/div/dl/dl')
            for block in blocks:
                key = block.xpath("./dt/text()")[0]
                value = block.xpath("./dd/text()")[0]
                info[key] = value
        return info
