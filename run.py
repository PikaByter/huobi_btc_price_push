import time
import requests
from fangtang_push import fangtang_push
from util.time_format import timestamp_to_date
from util.my_urllib import fuck_ssl
import json

# 基础API,需要科学上网
base_api = "https://api.huobi.pro/market/history"

# 15min涨跌提醒触发值
line_15 = 0.01
# 30min涨跌提醒触发值
line_30 = 0.01

#获取当前成交价格，以最近100单成交的均价为准
def get_current_price():
    url = base_api + "/trade?symbol=btcusdt&size=100"
    data = json.loads(fuck_ssl.myget(url))
    data = data["data"]
    average_price = 0
    for i in data:
        average_price += i["data"][0]["price"]
    average_price /= 100
    average_price = int(average_price)
    return average_price

# 获取K线图数据
def get_kandle(period):
    url = base_api + "/kline?symbol=btcusdt&period=%dmin&size=1" % period
    data = json.loads(fuck_ssl.myget(url))
    # 本周期开盘价
    open_price = int(data["data"][0]["open"])
    # 当前价格
    close_price = int(data["data"][0]["close"])
    return open_price, close_price

# 处理获取的K线图数据，调用方糖进行推送
def kandle_push(period, alarm_line, alarm_count, alarm_count_line):
    open_price, close_price = get_kandle(period)
    # 计算涨跌百分比
    current_line = (close_price - open_price) / open_price * 100
    # 超过涨跌上限，推送
    if abs(current_line) > alarm_line:
        current_price = get_current_price()
        current_time = time.time()
        detail = "%dmin 内变动了 %.2f%%\n\n当前价格为%d\n当前为此周期的第%d/%d次推送\n\n当前时间为:%s" \
                 % (period, current_line, current_price, alarm_count, alarm_count_line,
                    timestamp_to_date(current_time))
        if current_line > 0:
            fangtang_push("涨涨涨涨涨涨涨涨涨！", detail)
        else:
            fangtang_push("跌跌跌跌跌跌跌跌跌！", detail)
        return True
    else:
        return False

# 分别处理15min和30min的k线图数据
def call_kandle_push(alarm_15_count, alarm_30_count):
    if kandle_push(15, line_15, alarm_15_count, alarm_count_line=3):
        return True, True
    else:
        if kandle_push(30, line_30, alarm_30_count, alarm_count_line=5):
            return False, True
        else:
            return False, False

# 推送数量到达上限，停止推送
def sleep_until_next_period(period):
    period *= 60
    current_time = time.time()
    next_period = (int(current_time / period) + 1) * period
    title = "到达 %dmin 内推送上限，将休息至%s" % (period / 60, timestamp_to_date(next_period))
    print(title)
    fangtang_push(title, "")
    time_gap = next_period - current_time
    time.sleep(time_gap)


if __name__ == '__main__':
    alarm_15_count = 1
    alarm_30_count = 1
    while True:
        try:
        # 15min内推送上限为3次，30min内上限为5次
        # 到达上限则休息到下一个周期
            alarm_15, alarm_30 = call_kandle_push(alarm_15_count, alarm_30_count)
            if alarm_15_count == 3:
                alarm_15_count = 1
                sleep_until_next_period(15)
                continue
            if alarm_30_count == 5:
                alarm_30_count = 1
                sleep_until_next_period(30)
                continue

            if alarm_15:
                alarm_15_count += 1
            if alarm_30:
                alarm_30_count += 1
        except Exception as e:
            pass
        # 每10s获取一次数据
        time.sleep(10)
