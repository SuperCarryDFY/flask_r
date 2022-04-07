# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent


class xywy_spider(object):
    def __init__(self):
        self.url = 'http://y.wksc.com/search/?q={}'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def get_html(self, word):
        self.url = self.url.format(parse.quote(word))
        res = requests.get(url=self.url, headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        html = res.text
        # print(type(html))
        
        with open('5.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        return html

    def parse_html(self, word):
        html = self.get_html(word)
        if html:
            p = etree.HTML(html)
            # -------------------------------
            blocks = p.xpath("//*[@class='h-drugs-item']")
            blocks_list_dic = []
            print('len_blocks',len(blocks))
            for block in blocks:
                iname = ''.join(block.xpath("./div[1]/div/h3/a/text()")).strip()
                # 获得iprice
                iprice = ''.join(block.xpath("./div[1]/div[3]/span/strong/text()")).strip()
                if iprice == '':
                    continue

                # 获得isrc
                isrc = ''.join(block.xpath("./div[1]/div[2]/p[2]/text()")).strip()
                
                # 获得iinfo
                # iinfo = ''.join(block.xpath("./div[1]/div[2]/p[1]/text()")).strip()
                # 获得ipic
                ipic = ''.join(block.xpath("./div[1]/div[1]/a/img/@src")).strip()

                dic = {"name":iname,"src":isrc,"price":iprice,"ipic":ipic}
                print(dic)
                blocks_list_dic.append(dic)
            
            # -----------------------
            return blocks_list_dic


    def run(self, word):
        result = self.parse_html(word)
        return result



