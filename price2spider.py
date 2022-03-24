# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent


class pricespider(object):
    def __init__(self):
        self.JDurl = 'https://search.jd.com/Search?keyword={}&enc=utf-8'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def get_JDhtml(self, word):
        self.url = self.JDurl.format(parse.quote(word))
        # print(self.url)
        res = requests.get(url=self.url, headers=self.headers, timeout=5)
        res.encoding = 'utf-8'
        html = res.text
        # print(html)
        with open('2.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        
        return html

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


    def parse_JDhtml(self, word):
        html = self.get_JDhtml(word)
        if html:
            p = etree.HTML(html)
            blocks = p.xpath('//*[@id="J_goodsList"]/ul/li')
            blocks_list_dic,i = [],0
            # print(len(blocks))
            for block in blocks:
                i = i+1
                if i>30:
                    break
                # 获得iname
                iname = block.xpath("./div/div[3]/a/em")[0]
                iname = iname.xpath('string(.)').strip().replace('\n','')
                # print('iname',iname)
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
                # 获得详细url
                iurl = block.xpath("./div/div[1]/a/@href")[0]
                iurl = 'https:'+iurl
                info = self.getinfo(iurl)

                dic = {"name":iname,"src":isrc,"price":iprice,"ipic":ipic,"info":info}
                print(dic)
                blocks_list_dic.append(dic)
            return blocks_list_dic

    def run(self, word):
        result = self.parse_JDhtml(word)
        return result


