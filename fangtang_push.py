from util.my_urllib import fuck_ssl

# 自己去申请一个
API_Key="SCT19128TvH96G3HJivHMLPFxSvXgJ8RW"

# 封装方糖推送服务
def fangtang_push(title, detail):
    push_data = {
        "title": title,
        "desp": detail
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    push_url = "https://sctapi.ftqq.com/%s.send"%API_Key
    fuck_ssl.set_headers(headers)
    fuck_ssl.mypost(push_url, data=push_data)

if __name__ == '__main__':
    fangtang_push("测试推送","哈哈哈")
    pass