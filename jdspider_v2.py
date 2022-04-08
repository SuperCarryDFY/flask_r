import requests
import json


class jdspider_v2(object):
    def __init__(self):
        self.url = 'http://39.99.55.31:4000/api/pricesearch'
        self.headers = {'content-type': "application/json"}


    def get_html(self, word):
        body = {'word':word}
        res = requests.post(url=self.url, headers=self.headers, data = json.dumps(body),timeout=5)
        html = res.text
        x = html.encode('utf-8')
        html = x.decode('unicode_escape')
        return html
        


