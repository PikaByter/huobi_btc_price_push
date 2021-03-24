import json
import os
import datetime
import time

from util.my_urllib import fuck_ssl
from util.mylog import log
from fangtang_push import fangtang_push
base_api = "https://api.huobi.pro/market/history"

curr_time = datetime.datetime.now()
time_str = curr_time.strftime("%Y-%m-%d")
store_name = "./data/%s.json" % time_str

# 修改成一次获取一天的数据，同时获取当天1min,5min,15min,30min,60min的数据，之后添加到定时任务中
def get_kandle(period):
    curr_time = datetime.datetime.now()
    log.logger.info("获取 %s 的数据" % curr_time)
    url = base_api + "/kline?symbol=btcusdt&period=%dmin&size=2" % period
    data = json.loads(fuck_ssl.myget(url))
    if data["status"] != "ok":
        raise Exception
    if not os.path.exists(store_name):
        log.logger.info("创建新文件")
        open(store_name, "w")
        log.logger.info("添加新数据")
        store_data(data['data'][1])
    else:
        log.logger.info("获取旧数据")
        with open(store_name, "r", encoding="utf-8") as my_file:
            old_data = json.load(my_file)
        log.logger.info("添加新数据")
        if isinstance(old_data, type({"a": 1})):
            old_data = [old_data]
        if data['data'][1]["id"] - old_data[-1]["id"] != 300:
            raise Exception
        old_data.append(data['data'][1])
        log.logger.info("保存新数据")
        store_data(old_data)


def store_data(data):
    with open(store_name, "w", encoding="utf-8") as my_file:
        json.dump(data, my_file, indent=4, ensure_ascii=False)

# 保持定时爬取


def sleep_until_next_period(period):
    period *= 60
    current_time = time.time()
    next_period = (int(current_time / period) + 1) * period + 60
    time_gap = next_period - current_time
    time.sleep(time_gap)


if __name__ == '__main__':
    period=5
    while True:
        try:
            get_kandle(period)
        except Exception as e:
            log.logger.error("发生错误，休息1min后重新抓取")
            time.sleep(600)
            try:
                get_kandle(period)
            except Exception as e:
                log.logger.error("依旧无法解决问题，使用方糖进行通知")
                fangtang_push("火币数据爬取出现错误，快起床看看啊", "来呀来看呀，程序崩溃了")
        log.logger.info("休息到下一个周期")
        sleep_until_next_period(period)
