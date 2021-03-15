import json
from urllib import request, parse
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class my_urllib:
    def __init__(self):
        self.s = requests.session()
        self.s.mount('https://', MyAdapter())
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.post_json = False

    def set_headers(self, headers):
        self.headers = headers
    def set_post_json(self):
        self.post_json=True

    def myget(self, url):
        req = request.Request(url=url, headers=self.headers)
        response = request.urlopen(req)
        return response.read()

    def mypost(self, url, data):
        if self.post_json:
            data = bytes(json.dumps(data), encoding="utf8")
        else:
            data = bytes(parse.urlencode(data), encoding='utf8')
        req = request.Request(url=url, headers=self.headers)
        response = request.urlopen(req, data=data)
        return response.read()

    def parse_response_json(self,url,data):
        return json.loads(self.mypost(url,data))

fuck_ssl=my_urllib()

if __name__ == '__main__':
    url = "https://api.huobi.pro/market/history/kline?symbol=btcusdt&period=30min&size=1"
    my_urllib=my_urllib()
    response_text=my_urllib.myget(url)
    print(json.loads(response_text))

