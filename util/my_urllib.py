import urllib.request
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

# 重新搞一个Adapter
class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


s = requests.Session()
s.mount('https://', MyAdapter())
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

# 自己搞get，返回的时候直接转dict
def myget(url, headers=headers):
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    return eval(response.read())

# 自己搞post
def mypost(url: str, push_data: dict, headers: dict = headers) -> dict:
    data = bytes(urllib.parse.urlencode(push_data), encoding='utf8')
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req, data=data)
    return eval(response.read())


if __name__ == '__main__':
    url = "https://api.huobi.pro/market/history/kline?symbol=btcusdt&period=30min&size=1"
    r = myget(url)
    print(r)
