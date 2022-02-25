# coding=utf-8

from visiable.vismodel import Edge, Node, Info

from config import config
from utils import Utils, Date

# 节点集合
count = {'from': set(), 'to': set()}


class Nodecut:
    def __init__(self, node: Node, from_or_to: str):
        self.address: str = node.address
        self.label: str = node.label
        self.length: int = node.to_hlen if from_or_to == 'to' else node.from_hlen

    # 白名单剪枝
    @staticmethod
    def is_white(address: str) -> bool:
        if address in config.white:
            return True
        return False

    # label标签剪枝
    @staticmethod
    def is_label(label: str) -> bool:
        if label:
            return True
        return False

    # 出度剪枝
    @staticmethod
    def is_outof_len(length: int) -> bool:
        if length > config.MAX_OUT_DEGREE:
            return True
        return False

    # 黑名单剪枝
    @staticmethod
    def is_black(address: str) -> bool:
        if address in config.black:
            return True
        return False

    # 节点剪枝
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


class Precut:
    def __init__(self, edge: Edge, from_or_to: str):
        self.edge: Edge = edge
        self.from_or_to: str = from_or_to

    # 日期剪枝
    @staticmethod
    def is_outof_date(info: Info) -> bool:
        for i in info:
            if Date.date_transform_reverse(i[1][1]) > config.TIME_STAMP:
                return True
        return False

    # 预剪枝
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

    # 重复剪枝
    @staticmethod
    def is_count(node: Node, nodes: set[Node]) -> bool:
        if node in nodes:
            return True
        return False

    # 后剪枝
    def cut(self) -> bool:
        if self.is_count(self.node, self.count):
            return True
        return False
