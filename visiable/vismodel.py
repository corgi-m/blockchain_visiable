# coding=utf-8

from utils import Date

import typing
import model

Info = tuple[str, str, str, float]


class Node:
    def __init__(self, address: str):
        self.__tohead: Edge or None = None
        self.__fromhead: Edge or None = None
        self.__address: str = address
        self.__to_relation: set['Node'] = set()
        self.__from_relation: set['Node'] = set()
        self.__balance: dict[str, float] = self.get_balance(address)
        self.__label: str = self.get_label(address)
        self.__to_hlen: int = 0
        self.__from_hlen: int = 0

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

    # 边生成器
    def edges_generate(self, from_or_to) -> typing.Generator['Edge', None, None]:
        head = self.__tohead if from_or_to == 'to' else self.__fromhead
        while head is not None:
            yield head
            head = head.last_to_edge if from_or_to == 'to' else head.last_from_edge

    # 添加边
    def add_edge(self, nodeto, info) -> 'Edge':
        for edge in self.edges_generate('to'):
            if edge.nodeto == nodeto:
                edge.add_info(info)
                break
        else:
            self.__to_hlen += 1
            nodeto.from_hlen += 1
            edge = Edge(self, nodeto, self.__tohead, nodeto.__fromhead)
            edge.add_info(info)
            self.__tohead = edge
            nodeto.fromhead = edge
        return edge

    @property
    def address(self) -> str:
        return self.__address

    @property
    def balance(self) -> dict[str, float]:
        return self.__balance

    @property
    def label(self) -> str:
        return self.__label

    @property
    def fromhead(self) -> 'Edge':
        return self.__fromhead

    @fromhead.setter
    def fromhead(self, value):
        self.__fromhead = value

    @property
    def from_hlen(self):
        return self.__from_hlen

    @property
    def to_hlen(self):
        return self.__to_hlen

    @from_hlen.setter
    def from_hlen(self, value):
        self.__from_hlen = value

    @property
    def to_relation(self) -> set['Node']:
        return self.__to_relation

    @property
    def to_relationcount(self) -> int:
        return len(self.__to_relation)

    @to_relation.setter
    def to_relation(self, value: set['Node']):
        self.__to_relation |= value

    @property
    def from_relation(self) -> set['Node']:
        return self.__from_relation

    @property
    def from_relationcount(self) -> int:
        return len(self.__from_relation)

    @from_relation.setter
    def from_relation(self, value: set['Node']):
        self.__from_relation |= value


class Edge:
    def __init__(self, nodefrom: Node, nodeto: Node,
                 last_to_edge: 'Edge' = None, last_from_edge: 'Edge' = None):
        self.__nodefrom: Node = nodefrom
        self.__nodeto: Node = nodeto
        self.__info: list[tuple[int, Info]] = []  # transferhash, blocktime, symbol, value
        self.__last_to_edge: 'Edge' = last_to_edge
        self.__last_from_edge: 'Edge' = last_from_edge

    # 添加边信息
    def add_info(self, info):
        self.__info.append((Date.date_transform_reverse(info[1]), info))

    @property
    def info(self) -> list[tuple[int, Info]]:
        return self.__info

    @property
    def nodeto(self) -> Node:
        return self.__nodeto

    @property
    def nodefrom(self) -> Node:
        return self.__nodefrom

    @property
    def last_to_edge(self) -> 'Edge':
        return self.__last_to_edge

    @property
    def last_from_edge(self) -> 'Edge':
        return self.__last_from_edge
