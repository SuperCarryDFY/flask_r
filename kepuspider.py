# coding:utf-8
import requests
from lxml import etree
from fake_useragent import UserAgent

'''
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
'''


class kepuspider(object):
    def __init__(self):
        self.url = 'http://lxjk.people.cn/GB/404218/429396/index.html'
        self.headers = {
            "User-Agent": UserAgent().firefox
        }

    def get_html(self, url):
        res = requests.get(url=self.url, headers=self.headers, timeout=5)
        res.encoding = 'gb2312'
        html = res.text.encode('gb2312')
        '''
        print(type(html))
        with open('1.txt', 'wb') as f:
            f.write(html)
        '''
        return html

    def parse_html(self, url):
        html = self.get_html(url)
        if html:
            p = etree.HTML(html)
            h_list = p.xpath(
                "/html/body/div[@class='foot clearfix']/div[@class='w1000 Conbg Conbg2 clearfix']/div[@class='p5Con "
                "clearfix']/ul[@class='p5_sub white clearfix']/li/text()")
            # 三个类别
            # print(h_list)
        text_list_dic = [[] for _ in range(len(h_list))]
        for i in range(len(h_list)):
            k = 1
            while True:
                head = p.xpath("/html/body/div[@class='foot clearfix']/div[@class='w1000 Conbg Conbg2 clearfix']/div["
                               "@class='p5Con clearfix']/div[@class='p5box p5box{}']/div[@class='p5con clearfix']["
                               "{}]/div/h3/a/text()".format(i + 1, k))
                if not head:
                    break
                # text = p.xpath("/div[@class='p5con clearfix'][{}]/div/p/a/text()".format(k))
                text = p.xpath("/html/body/div[@class='foot clearfix']/div[@class='w1000 Conbg Conbg2 clearfix']/div["
                               "@class='p5Con clearfix']/div[@class='p5box p5box{}']/div[@class='p5con clearfix']["
                               "{}]/div/p/a/text()".format(i + 1, k))
                # url = p.xpath("/div[@class='p5con clearfix'][{}]/div/p/a[@class='href']".format(k))
                url = p.xpath("/html/body/div[@class='foot clearfix']/div[@class='w1000 Conbg Conbg2 clearfix']/div["
                              "@class='p5Con clearfix']/div[@class='p5box p5box{}']/div[@class='p5con clearfix']["
                              "{}]/div/h3/a/@href".format(i + 1, k))

                dic = {'head': head[0].strip('\n'), 'text': text[0].strip('\n'), 'url': url[0]}
                # print("字典：", dic)
                text_list_dic[i].append(dic)
                k = k + 1
        # 每个标题里的head,text和url
        return h_list, text_list_dic

    def run(self):
        return self.parse_html(self.url)