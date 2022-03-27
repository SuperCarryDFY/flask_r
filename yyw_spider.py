from email import header
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent


class yyw_spider(object):
    def __init__(self):
        self.url = 'https://www.111.com.cn/search/search.action?keyWord={}'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def geturl(self,word):
        parse_word = parse.quote(word)
        length = len(parse_word)
        parse_word_list = list(parse_word)
        length2 = int(length/3*5)
        for i in range(1,length2,5):
            parse_word_list.insert(i,'2')
            parse_word_list.insert(i+1,'5')
        # print(''.join(parse_word_list))
        return ''.join(parse_word_list)

    def get_html(self, word):
        self.url = self.url.format(self.geturl(word))
        # print(self.url)
        res = requests.get(url=self.url, headers=self.headers, timeout=5)
        res.encoding = 'gbk'
        html = res.text
        return html
        # print(type(html))
        
        # with open('4.txt', 'w', encoding='utf-8') as f:
        #     f.write(html)
        # return html

    def parse_html(self, word):
        html = self.get_html(word)
        if html:
            p = etree.HTML(html)
            # -------------------------------
            blocks = p.xpath("//*[@id='plist']/div[2]/div[1]/ul/li")
            blocks_list_dic = []
            # print('len_blocks',len(blocks))
            for block in blocks:
                iname = ''.join(block.xpath("./div[1]/p[2]/a/text()")).strip()
                # 获得isrc
                isrc = ''.join(block.xpath("./div[1]/div/span/text()")).strip()
                if isrc == '' :
                    isrc = ''.join(block.xpath("./div[1]/div[2]/span[2]/a/text()")).strip()
                if isrc == '':
                    isrc = ''.join(block.xpath("./div[1]/div[1]/span[2]/a/text()")).strip()
                # 获得iprice
                iprice = ''.join(block.xpath("./div[1]/p[1]/span/text()")).strip()
                # 获得ipic
                ipic = ''.join(block.xpath("./div[1]/a/img/@src")).strip()
                dic = {"name":iname,"src":isrc,"price":iprice,"ipic":ipic}
                print(dic)
                blocks_list_dic.append(dic)
            
            # -----------------------
            return blocks_list_dic


    def run(self, word):
        result = self.parse_html(word)
        return result

