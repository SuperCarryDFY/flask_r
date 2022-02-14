# coding:utf-8
import requests
from lxml import etree
from urllib import parse
from fake_useragent import UserAgent
# import numpy as np




class zhaoyaospider(object):
    def __init__(self):
        self.url = 'http://www.35yao.com/invest/list-htm-catid-{}-page-{}.html'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }
        self.classify_dict = {"儿科": 7, "妇科": 8, "耳鼻喉/口腔": 9, "骨伤科": 10, "皮肤科": 11, "呼吸": 12, "消化": 36, "心脑血管": 13, "循环系统": 14,
                 "神经系统": 15, "内科": 18, "外科": 19, "降糖降压降脂": 47, "元素/营养补充": 48, "美容养颜": 49, "减肥瘦身": 50, "改善睡眠": 51,
                 "延缓衰老": 52, "补肾壮阳": 53}
        self.classify_list = [['儿科', '妇科', '耳鼻喉/口腔', '骨伤科', "皮肤科", "呼吸", "消化"],
                 ["内科", "外科", '儿科', '妇科', "耳鼻喉/口腔", "骨伤科", "皮肤科"],
                 ["降糖降压降脂", "元素/营养补充", "美容养颜", "减肥瘦身", "改善睡眠", "延缓衰老", "补肾壮阳"]]

    def get_html(self, word):
        for index in range(1, 3):
            self.urlindex = self.url.format(self.classify_dict[word], index)
            res = requests.get(url=self.urlindex, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            html = res.text
            yield html

    def parse_html(self, word):
        blocks_list_dic = []
        page = 0
        for html in self.get_html(word):
            page += 1
            # print(page)
            p = etree.HTML(html)
            blocks = p.xpath(
                "//tr")
            # print(page, blocks)
            if not blocks:
                print("endpage", page)
                break
            for block in blocks:
                iname = block.xpath("./td[3]/ul/li[1]/a/strong[@class='px14']//text()")
                iname = ''.join(iname)
                img_url = block.xpath("./td[1]/div/a/img/@src")[0]
                dic = {"name": iname, "img_url": img_url}
                blocks_list_dic.append(dic)
                # print(dic)
        return blocks_list_dic

    def run(self):
        classify_result = []
        for cl in self.classify_list:
            iresult_list = []
            for word in cl:
                iresult_list.append(self.parse_html(word))
            classify_result.append(iresult_list)
        # print(classify_result)
        # l = np.array(classify_result)
        # print(l.shape)
        return [self.classify_list, classify_result]
        # result = self.parse_html(word)
        # print(result)
