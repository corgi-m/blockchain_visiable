# coding=utf-8
import re
import time
import json
import config
import base64
import random


class Utils:
    def __init__(self):
        ...

    @staticmethod
    def use(_):
        ...

    @staticmethod
    def outof_list(li) -> str:
        return li[0] if isinstance(li, list) else li

    @staticmethod
    def tip_filter(tips):
        tips = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", tips)
        tips = re.sub('[^\x00-\x7F]', '', tips)
        return tips

    @staticmethod
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
        random1 = str(random.randint(0, 9))
        random2 = str(random.randint(0, 9))
        random3 = str(random.randint(0, 9))
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


class Date:
    def __init__(self):
        ...

    @staticmethod
    def date_transform(timestamp) -> str:
        time_local = time.localtime(int(timestamp))
        datatime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return datatime

    @staticmethod
    def date_transform_reverse(datatime) -> int:
        time_local = time.strptime(datatime, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(time_local)
        return int(timestamp)


class Json:
    def __init__(self):
        ...

    @staticmethod
    def loads(res):
        try:
            data = json.loads(res)
        except Exception as e:
            print(e, file=config.config['log'])
            return None
        return data
