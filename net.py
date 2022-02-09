# coding=utf-8
from config import config
from utils import date_transform
import requests
import time


def req_get(url, params=None) -> requests.models.Response or None:
    print(url, params)
    if params is None:
        params = {}
    try:
        res = requests.get(url=url, headers=config['headers'], params=params, proxies=config['proxies'], timeout=10)
    except Exception as e:
        print("retry")
        print(e)
        try:
            res = requests.get(url=url, headers=config['headers'], params=params, proxies=config['proxies'], timeout=10)
        except Exception as e:
            print("error")
            print(e)
            print(date_transform(time.time()), url, params, file=config['log'])
            print(e, file=config['log'])
            return None
    return res


def req_post(url, params=None, data=None) -> requests.models.Response or None:
    print(url, params, data)
    if params is None:
        params = {}
    if data is None:
        data = {}
    try:
        res = requests.post(url=url, headers=config['headers'], params=params, data=data,
                            proxies=config['proxies'], timeout=10)
    except Exception as e:
        print("retry")
        print(e)
        try:
            res = requests.post(url=url, headers=config['headers'], params=params, data=data,
                                proxies=config['proxies'], timeout=10)
        except Exception as e:
            print("error")
            print(e)
            print(date_transform(time.time()), url, params, data, file=config['log'])
            print(e, file=config['log'])
            return None
    return res
