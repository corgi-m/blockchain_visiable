# coding=utf-8
from typing import Generator

Info = list[tuple[str, str, str, float]]
Balance = dict[str, float]
nodesmap: dict[str, 'Node'] = {}
edgesmap: dict[str, 'Edge'] = {}
nodesappear: dict[str, list[set['Node']]] = {'from': [], 'to': []}


class Node:
    def __init__(self, address: str, balance: Balance, label: str = None):
        self.__tohead: Edge or None = None
        self.__fromhead: Edge or None = None
        self.__address: str = address
        self.__relation: set['Node'] = set()
        self.__balance: Balance = balance
        self.__label: str = label
        self.__to_hlen: int = 0
        self.__from_hlen: int = 0

    def edges_generate(self, from_or_to) -> Generator['Edge', None, None]:
        head = self.__tohead if from_or_to == 'to' else self.__fromhead
        while head is not None:
            yield head
            head = head.last_to_edge if from_or_to == 'to' else head.last_from_edge

    def add_edge(self, nodeto, info) -> 'Edge':
        for edge in self.edges_generate('to'):
            if edge.nodeto == nodeto:
                edge.add_info(info)
                break
        else:
            self.__to_hlen += 1
            nodeto.from_hlen += 1
            edge = Edge(self, nodeto, info, self.__tohead, nodeto.__fromhead)
            self.__tohead = edge
            nodeto.fromhead = edge
        return edge

    @property
    def address(self) -> str:
        return self.__address

    @property
    def balance(self) -> Balance:
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
    def relation(self) -> set['Node']:
        return self.__relation

    @property
    def relationcount(self) -> int:
        return len(self.__relation)

    @relation.setter
    def relation(self, value: set['Node']):
        self.__relation |= value


class Edge:
    def __init__(self, nodefrom: Node, nodeto: Node, info: Info,
                 last_to_edge: 'Edge' = None, last_from_edge: 'Edge' = None):
        self.__nodefrom: Node = nodefrom
        self.__nodeto: Node = nodeto
        self.__info: Info = info  # transferhash, blocktime, symbol, value
        self.__last_to_edge: 'Edge' = last_to_edge
        self.__last_from_edge: 'Edge' = last_from_edge

    def add_info(self, info):
        self.__info.append(info)

    @property
    def info(self) -> Info:
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
