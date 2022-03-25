# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent


class pricespider(object):
    def __init__(self):
        self.JDurl = 'https://search.jd.com/Search?keyword={}&enc=utf-8'
        self.headers = {
            "User-Agent": UserAgent().firefox,
            "Cookie":"shshshfpa=169abe7a-903e-d223-b2f8-9c128809a51b-1644230950; shshshfpb=kfSJME5Kw4u7976fDhzaVRQ; areaId=2; PCSYCityID=CN_310000_310100_0; pinId=SVmil3tkWpfFSEPeUv_NA7V9-x-f3wj7; pin=jd_4aa3e903d802b; unick=jd_4aa3e903d802b; _tp=95plABzmImNeO4Jev5klk%2BNJ%2F4ofpX1FArno%2FCVDrEk%3D; _pst=jd_4aa3e903d802b; user-key=723a6122-9d73-4085-b470-9a58d119cdff; ipLoc-djd=2-2817-61075-0; shshshfp=bfcd1847c51a3ed41a8222b2d011cbd9; ip_cityCode=2817; wlfstk_smdl=ko2ju7m3wa6sed1o7q5hel1yg4dzhpm1; TrackID=1sKKPwZA6iip-644zb7BOkt97L4SJXAvyuQ6GCn1mAZWlLPVe8d-kBqX2sHaPfVZCfljTGYY3YHQJ-IyihhInal6eOkkl-gjM4NI_b3k9jQg; ceshi3.com=000; cn=0; token=8877ab766c1e3fba25878b8f49910dc1,3,915678; __tk=f39bdd9761b854642f1fc8c0e962e32d,3,915678; __jdc=122270672; __jdu=16481061363191853629939; __jda=122270672.16481061363191853629939.1648106136.1648220821.1648220896.3; __jdb=122270672.1.16481061363191853629939|3.1648220896; __jdv=122270672|baidu|-|organic|notset|1648220896480; thor=906D48BF5B2881EFEF427D78EBAE363D7718D3ED64D92B9AAB043C535495D51FC32B49DA99990A5F023BCE8B12D08544A8F31F938429600418CC71CCABBAD74EE2D8F4EEA0083669CA76CF3CF159A187D5C401ED5B7B486CC622C739990C63D98DF3DB1ECC5D26E0F351F4474F27C51CA3937913F41F20573FC76E3A4F925D5BB0BE3A9B077F8268A45E9D58FDE5AE813646D751EB964AFF37565FA0ACA46AF2; 3AB9D23F7A4B3C9B=APCYEGE4DAONR3WTTSOS2ZZI3G6I6OXZ5O3LVQHG2KQXHSWUIVQZZL6ILR7KWNQDY2KFRP3F32XQ2SEKCAAZFPWWLM; shshshsID=1ef7c49a2b4826841df2ff401d8caa0d_10_1648220914592"
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


