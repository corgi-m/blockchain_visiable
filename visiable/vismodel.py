# coding=utf-8

import model
from config import config
from utils import Date

Info = tuple[str, str, str, float]


class Node:
    def __init__(self, address: str):
        self.__address: str = address
        self.__balance: dict[str, float] = self.get_balance(address)
        if config.internal:
            self.__internal: list[tuple[int, str, str, float, str, float]] = self.get_internal(address)
        self.__label: str = self.get_label(address)
        self.__hlen: int = 0

    # 设置label
    @staticmethod
    def get_label(address) -> str:
        label = model.Label.get(address)
        if not label:
            return ""
        return label[0][0]

    # 设置balance
    @staticmethod
    def get_balance(address) -> dict[str, float]:
        res = {}
        balance = model.Balance.get(address)
        if not balance:
            return res
        balance = balance[0][0]
        for balan in balance.split(';'):
            temp = balan.split(',')
            if len(temp) != 2:
                continue
            res[temp[0]] = float(temp[1])
        return res

    # 设置internal
    @staticmethod
    def get_internal(address) -> list[tuple[int, str, str, float, str, float]]:
        res = []
        internal = model.Internal.get(address)
        if not internal:
            return res
        for i in internal:
            res.append((Date.date_transform_reverse(str(i[6])), i[0], i[6], i[3], i[2], i[5], i[4]))
        print(address)

        return res

    @property
    def address(self) -> str:
        return self.__address

    @property
    def balance(self) -> dict[str, float]:
        return self.__balance

    @property
    def internal(self) -> list[tuple[int, str, str, float, str, float]]:
        return self.__internal

    @property
    def label(self) -> str:
        return self.__label

    @property
    def hlen(self):
        return self.__hlen

    @hlen.setter
    def hlen(self, value):
        self.__hlen = value


class Edge:
    def __init__(self, nodefrom: str, nodeto: str):
        self.__nodefrom: str = nodefrom
        self.__nodeto: str = nodeto
        self.__info: list[tuple[int, Info]] = []  # transferhash, blocktime, symbol, value

    # 添加边信息
    def add_info(self, info):
        self.__info.append((Date.date_transform_reverse(info[1]), info))

    @property
    def info(self) -> list[tuple[int, Info]]:
        return self.__info

    @property
    def nodeto(self) -> str:
        return self.__nodeto

    @property
    def nodefrom(self) -> str:
        return self.__nodefrom
