# coding=utf-8

from config import config

# 节点集合
count = {'from': set(), 'to': set()}


class Nodecut:
    def __init__(self, address, from_or_to: str):
        self.address: str = address
        self.from_or_to: str = from_or_to

    @staticmethod
    def is_count(address: str, from_or_to) -> bool:
        if address in count[from_or_to]:
            return True
        count[from_or_to] |= {address}
        return False

    # 节点剪枝
    def cut(self) -> bool:
        if self.is_count(self.address, self.from_or_to):
            return True
        return False


class Postcut:
    def __init__(self, length: int, address: str, label: str):
        self.length = length
        self.address: str = address
        self.label: str = label

    # 出度剪枝
    @staticmethod
    def is_outof_len(length: int) -> bool:
        if length > config.MAX_OUT_DEGREE:
            return True
        return False

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

    # 黑名单剪枝
    @staticmethod
    def is_black(address: str) -> bool:
        if address in config.black:
            return True
        return False

    # 后剪枝
    def cut(self) -> bool:
        if self.is_white(self.address):
            return False
        if self.is_black(self.address):
            return True
        if self.is_label(self.label):
            return True
        if self.is_outof_len(self.length):
            return True
        return False
