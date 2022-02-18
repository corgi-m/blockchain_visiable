# coding=utf-8
import base64
from random import randint
from config import config
import time
import grequests


def greq_get(url, params=None) -> list[grequests.AsyncRequest]:
    # print(url, params)
    if params is None:
        params = {}
    return grequests.get(url=url, headers={'x-apiKey': get_x_apikey()}, params=params, proxies=config['proxies'],
                         timeout=10)


# 获取动态变化且加密的x-apiKey
def get_x_apikey():
    # API_KEY固定字符串
    API_KEY = "a2c903cc-b31e-4547-9299-b6d07b7631ab"
    Key1 = API_KEY[0:8]
    Key2 = API_KEY[8:]
    #  交换API_KEY部分内容
    new_Key = Key2 + Key1
    # 获取当前时间，毫秒级
    cur_time = round(time.time() * 1000)
    # 处理获得的时间
    new_time = str(1 * cur_time + 1111111111111)
    # 生成三个0-9的随机整数
    random1 = str(randint(0, 9))
    random2 = str(randint(0, 9))
    random3 = str(randint(0, 9))
    # 再次处理时间字符串
    cur_time = new_time + random1 + random2 + random3
    # 将包含API_KEY和时间串的内容合并
    this_Key = new_Key + '|' + cur_time
    # 转码
    n_k = this_Key.encode('utf-8')
    # base64加秘
    x_apiKey = base64.b64encode(n_k)
    # 将加密后的x_apiKey返回
    return str(x_apiKey, encoding='utf8')
