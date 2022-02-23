# coding=utf-8

from config import config
from utils import Utils

import grequests


class Net:
    def __init__(self):
        self.__AsyncRequest = grequests.AsyncRequest

    @staticmethod
    def greq_get(url, params=None) -> list[grequests.AsyncRequest]:
        if params is None:
            params = {}
        return grequests.get(url=url, headers={'x-apiKey': Utils.get_x_apikey()}, params=params, proxies=config['proxies'],
                             timeout=10)

    @staticmethod
    def greq_map(urls):
        return grequests.map(urls)

    @property
    def AsyncRequest(self):
        return self.__AsyncRequest
