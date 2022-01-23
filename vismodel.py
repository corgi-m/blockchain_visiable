from typing import Generator

Info = list[tuple[str, str, str, float]]
Balance = dict[str, float]


class Node:
    def __init__(self, address: str, balance: Balance = None, label: str = None):
        self.__head: Edge = None
        self.__address: str = address
        self.__balance: Balance = balance
        self.__label: str = label
        self.__hlen: int = 0

    def edges_generate(self) -> Generator['Edge', None, None]:
        head = self.__head
        while head is not None:
            yield head
            head = head.getlastedge

    def add_edge(self, nodeto, info) -> 'Edge':
        for edge in self.edges_generate():
            if edge.getnodeto == nodeto:
                edge.add_info(info)
                break
        else:
            self.__hlen += 1
            edge = Edge(self, nodeto, info, self.__head)
            self.__head = edge
        return edge

    @property
    def getaddress(self) -> str:
        return self.__address

    @property
    def getbalance(self) -> Balance:
        return self.__balance

    @property
    def getlabel(self) -> str:
        return self.__label

    @property
    def gethead(self) -> 'Edge':
        return self.__head

    @property
    def gethlen(self) -> int:
        return self.__hlen


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
    def getinfo(self) -> Info:
        return self.__info

    @property
    def getnodeto(self) -> Node:
        return self.__nodeto

    @property
    def getnodefrom(self) -> Node:
        return self.__nodefrom

    @property
    def getlastedge(self) -> 'Edge':
        return self.__lastedge
