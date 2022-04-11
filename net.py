# coding=utf-8

from config import config
from utils import Utils

import grequests


class Net:
    def __init__(self):
        self.__AsyncRequest = grequests.AsyncRequest

    # 添加进请求池
    @staticmethod
    def greq_get(url, params=None) -> list[grequests.AsyncRequest]:
        if params is None:
            params = {}
        return grequests.get(url=url, headers={'x-apiKey': Utils.get_x_apikey()}, params=params, proxies=config.proxies,
                             )

    # 进行请求哦
    @staticmethod
    def greq_map(urls) -> list[grequests.AsyncRequest]:
        return grequests.map(urls)

    @property
    def AsyncRequest(self) -> type:
        return self.__AsyncRequest
