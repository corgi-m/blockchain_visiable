# coding=utf-8
from config import config
import requests
import time


def req_get(url, params=None):
    print(url, params)
    if params is None:
        params = {}
    try:
        res = requests.get(url=url, headers=config['headers'], params=params, proxies=config['proxies'], timeout=2)
    except Exception as e:
        print("error")
        print(e)
        try:
            res = requests.get(url=url, headers=config['headers'], params=params, proxies=config['proxies'], timeout=2)
        except Exception as e:
            print("error")
            print(e)
            print(time.time(), url, params, file=config['log'])
            return None
    return res
