# coding=utf-8

from visiable.vismodel import Edge, Node, Info

from config import config
from utils import Utils, Date

count = {'from': set(), 'to': set()}


class Nodecut:
    def __init__(self, node: Node, from_or_to: str):
        self.address: str = node.address
        self.label: str or None = node.label
        self.length: int = node.to_hlen if from_or_to == 'to' else node.from_hlen

    def cut(self) -> bool:
        if self.is_white(self.address):
            return False
        if self.is_black(self.address):
            return True
        if self.is_outof_len(self.length):
            return True
        if self.is_label(self.label):
            return True
        return False

    @staticmethod
    def is_white(address: str) -> bool:
        if address in config['white']:
            return True
        return False

    @staticmethod
    def is_label(label: str or None) -> bool:
        if label is not None:
            return True
        return False

    @staticmethod
    def is_outof_len(length: int) -> bool:
        if length > config['MAX_OUT_DEGREE']:
            return True
        return False

    @staticmethod
    def is_black(address: str) -> bool:
        if address in config['black']:
            return True
        return False


class Precut:
    def __init__(self, edge: Edge, from_or_to: str):
        self.edge: Edge = edge
        self.from_or_to: str = from_or_to

    @staticmethod
    def is_outof_date(info: Info) -> bool:
        for i in info:
            if Date.date_transform_reverse(i[1][1]) > config['TIME_STAMP']:
                return True
        return False

    def cut(self) -> bool:
        Utils.use(self)
        # if self.is_outof_date(self.edge.info):
        #    return True
        return False


class Postcut:
    def __init__(self, edge: Edge, from_or_to: str):
        self.edge: Edge = edge
        self.from_or_to: str = from_or_to
        self.node: Node = edge.nodeto if from_or_to == 'to' else edge.nodefrom
        self.count: set[Node] = count[from_or_to]

    @staticmethod
    def is_count(node: Node, nodes: set[Node]) -> bool:
        if node in nodes:
            return True
        return False

    def cut(self) -> bool:
        if self.is_count(self.node, self.count):
            return True
        return False
