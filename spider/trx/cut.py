# coding=utf-8
from spider.cut import ABCPrecut, ABCPostcut, ABCEdgecut, ABCNodecut

from spider.save import save_label, save_transfer

from config import count, config
from utils import outof_list, date_transform


class Edgecut(ABCEdgecut):
    def __init__(self, edge, from_or_to):
        self.edge = self.init_edge(edge)
        self.node = edge[from_or_to]
        self.from_or_to = from_or_to
        self.precut = Precut(self.edge, self.node, self.from_or_to)
        self.postcut = Postcut(self.edge, self.node, self.from_or_to)

    # 边初始化
    @staticmethod
    def init_edge(edge):
        edge["from"] = outof_list(edge["from"])
        edge["to"] = outof_list(edge["to"])
        return edge

    # 边剪枝
    def cut(self):
        if self.precut.cut():
            return True
        save_transfer(self.edge["txhash"] if "txhash" in self.edge else self.edge["hash"], self.edge["from"],
                      self.edge["to"], self.edge["symbol"], self.edge["value"], date_transform(self.edge["blocktime"]))
        if self.postcut.cut():
            return True
        return False


class Precut(ABCPrecut):
    def __init__(self, edge, node, from_or_to):
        self.edge = edge
        self.node = node
        self.from_or_to = from_or_to

    #   剪掉合约
    def is_notransfer(self):
        if "contractType" in self.edge and 'TransferContract' not in self.edge["contractType"]:
            return True
        return False

    #  剪掉零交易
    def is_novalue(self):
        if self.edge["value"] < config['MIN_TRANSFER_VALUE']:
            return True
        return False

    # 边预剪枝
    def cut(self):
        if self.is_notransfer():
            return True
        if self.is_novalue():
            return True
        return False


class Postcut(ABCPostcut):
    def __init__(self, edge, node, from_or_to):
        self.edge = edge
        self.node = node
        self.from_or_to = from_or_to

    #  剪掉重复
    def is_count(self):  # 是否出现过，减少重复
        if self.node in count:
            return True
        count.add(self.node)
        return False

    #  剪掉tag
    def is_inaccount(self):
        if self.node in config['account']:
            return True
        return False

    #  剪掉tag
    def is_tag(self):
        if self.from_or_to + "Tag" in self.edge and len(self.edge[self.from_or_to + "Tag"]) > 0:
            config['account'][self.node] = self.edge[self.from_or_to + "Tag"]
            save_label(self.node, self.edge[self.from_or_to + "Tag"][0]['tag'])
            return True
        return False

    # 边后剪枝
    def cut(self):
        if self.is_count():
            return True
        if self.is_inaccount():
            return True
        if self.is_tag():
            return True
        return False


class Nodecut(ABCNodecut):
    def __init__(self, node, len_edges):
        self.node = node
        self.len_edges = len_edges

    #  剪掉出度超过阈值
    def is_outof_len(self):
        if self.len_edges > config['MAXN_LEN_EDGES']:
            return True
        return False

    # 节点剪枝
    def cut(self):
        if self.is_outof_len():
            return True
        return False
