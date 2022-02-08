# coding=utf-8
from typing import Generator

Info = list[tuple[str, str, str, float]]
Balance = dict[str, float]
nodesmap: dict[str, 'Node'] = {}
edgesmap: dict[str, 'Edge'] = {}
nodesappear_to: list[set['Node']] = []
nodesappear_from: list[set['Node']] = []


class Node:
    def __init__(self, address: str, balance: Balance, relation: set['Node'] = set(), label: str = None):
        self.__tohead: Edge = None
        self.__fromhead: Edge = None
        self.__address: str = address
        self.__relation: set['Node'] = relation
        self.__balance: Balance = balance
        self.__label: str = label
        self.__to_hlen: int = 0
        self.__from_hlen: int = 0

    def to_edges_generate(self) -> Generator['Edge', None, None]:
        head = self.__tohead
        while head is not None:
            yield head
            head = head.last_to_edge

    def from_edges_generate(self) -> Generator['Edge', None, None]:
        head = self.__fromhead
        while head is not None:
            yield head
            head = head.last_from_edge

    def add_to_edge(self, nodeto, info) -> 'Edge':
        for edge in self.to_edges_generate():
            if edge.nodeto == nodeto:
                edge.add_info(info)
                break
        else:
            self.__to_hlen += 1
            nodeto.__from_hlen += 1
            edge = Edge(self, nodeto, info, self.__tohead, nodeto.__fromhead)
            self.__tohead = edge
            nodeto.__fromhead = edge
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
    def tohead(self) -> 'Edge':
        return self.__tohead

    @property
    def fromhead(self) -> 'Edge':
        return self.__fromhead

    @property
    def to_hlen(self) -> int:
        return self.__to_hlen

    @property
    def from_hlen(self):
        return self.__from_hlen

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
        self.__relation = self.__relation.union(value)


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
