# coding=utf-8
from typing import Generator

Info = list[tuple[str, str, str, float]]
Balance = dict[str, float]
nodesmap: dict[str, 'Node'] = {}
edgesmap: dict[str, 'Edge'] = {}
nodesappear: list[set['Node']] = []


class Node:
    def __init__(self, address: str, balance: Balance, relation: set['Node'] = set(), label: str = None):
        self.__head: Edge = None
        self.__address: str = address
        self.__relation: set['Node'] = relation
        self.__balance: Balance = balance
        self.__label: str = label
        self.__hlen: int = 0

    def edges_generate(self) -> Generator['Edge', None, None]:
        head = self.__head
        while head is not None:
            yield head
            head = head.lastedge

    def add_edge(self, nodeto, info) -> 'Edge':
        for edge in self.edges_generate():
            if edge.nodeto == nodeto:
                edge.add_info(info)
                break
        else:
            self.__hlen += 1
            edge = Edge(self, nodeto, info, self.__head)
            self.__head = edge
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
    def head(self) -> 'Edge':
        return self.__head

    @property
    def hlen(self) -> int:
        return self.__hlen

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
                 lastedge: 'Edge' = None):
        self.__nodefrom: Node = nodefrom
        self.__nodeto: Node = nodeto
        self.__info: Info = info  # transferhash, blocktime, symbol, value
        self.__lastedge: 'Edge' = lastedge

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
    def lastedge(self) -> 'Edge':
        return self.__lastedge
