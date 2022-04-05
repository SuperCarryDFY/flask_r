# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent


class pricespider(object):
    def __init__(self):
        self.JDurl = 'https://search.jd.com/Search?keyword={}'
        self.TBurl = 'https://s.taobao.com/search?q={}'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def get_JDhtml(self, word):
        self.url = self.JDurl.format(parse.quote(word))
        # print(self.url)
        res = requests.get(url=self.url, headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        html = res.text
        # print(type(html))
        
        with open('2.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        
        return html

    def parse_JDhtml(self, word):
        html = self.get_JDhtml(word)
        if html:
            p = etree.HTML(html)
            blocks = p.xpath("//*[@id='J_goodsList']/ul/li")
            blocks_list_dic = []
            print(len(blocks))
            for block in blocks:
                # 获得iname
                iname = block.xpath("./div/div[3]/a/em")[0]
                iname = iname.xpath('string(.)').strip().replace('\n','')
                # print(iname)
                # 获得isrc
                isrc = block.xpath("./div/div[5]/span/a/text()")
                if isrc == [] :
                    isrc = "来源未知"
                else:
                    isrc = isrc[0]
                # 获得iprice
                iprice = block.xpath("./div/div[2]/strong/i/text()")[0]
                # 获得ipic
                ipic = block.xpath("./div/div[1]/a/img/@data-lazy-img")[0]
                ipic = 'https:'+ ipic
                dic = {"name":iname,"src":isrc,"price":iprice,"ipic":ipic}
                print(dic)
                blocks_list_dic.append(dic)
            return blocks_list_dic

    def run(self, word):
        result = self.get_JDhtml(word)
        return result
