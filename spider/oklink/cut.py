# coding=utf-8

from config import config
from model import Transfer, Label
from spider.common.cut import ABCPrecut, ABCPostcut, ABCEdgecut, ABCNodecut
from spider.save import Save
from spider.spider import count
from utils import Utils, Date


class OKEdgecut(ABCEdgecut):

    def __init__(self, edge, from_or_to):
        self.edge = self.init_edge(edge)
        self.node = edge[from_or_to]
        self.from_or_to = from_or_to
        self.precut = OKPrecut(self.edge, self.node, self.from_or_to)
        self.postcut = OKPostcut(self.edge, self.node, self.from_or_to)

    @staticmethod
    def init_edge(edge) -> dict[str, any]:
        edge["from"] = Utils.outof_list(edge["from"])
        edge["to"] = Utils.outof_list(edge["to"])
        return edge

    def cut(self) -> bool:
        if self.precut.cut():
            return True
        txhash = self.edge["txhash"] if "txhash" in self.edge else self.edge["hash"]
        symbol = self.edge["symbol"] if "symbol" in self.edge else config.db.dbname.upper()
        if "blocktime" in self.edge:
            blocktime = self.edge["blocktime"] / 1000 if self.edge["blocktime"] > 2000000000 else self.edge["blocktime"]
        else:
            blocktime = 2000000000
        datetime = Date.date_transform(blocktime)
        if not Transfer.is_exist(txhash):
            Save.save_transfer(txhash, self.edge["from"], self.edge["to"], symbol, self.edge["value"], datetime)
        if self.postcut.cut():
            return True
        return False


class OKPrecut(ABCPrecut):

    def __init__(self, edge, node, from_or_to):
        self.edge = edge
        self.node = node
        self.from_or_to = from_or_to

    def is_notransfer(self) -> bool:
        if "contractType" in self.edge and 'TransferContract' not in self.edge["contractType"]:
            return True
        if "isFromContract" in self.edge and self.edge['isFromContract'] is True:
            return True
        if "isToContract" in self.edge and self.edge['isToContract'] is True:
            return True
        return False

    def is_novalue(self) -> bool:
        if 'value' not in self.edge:
            return True
        if self.edge["value"] < config.MIN_TRANSFER_VALUE:
            return True
        return False

    def cut(self) -> bool:
        if self.is_notransfer():
            return True
        if self.is_novalue():
            return True
        return False


class OKPostcut(ABCPostcut):
    def __init__(self, edge, node, from_or_to):
        self.edge = edge
        self.node = node
        self.from_or_to = from_or_to

    def is_count(self) -> bool:  # 是否出现过，减少重复
        if self.node in count:
            return True
        count[self.from_or_to].add(self.node)
        return False

    def is_inaccount(self) -> bool:
        if Label.get(self.node):
            return True
        return False

    def is_tag(self) -> bool:
        if self.from_or_to + "Tag" in self.edge and len(self.edge[self.from_or_to + "Tag"]) > 0:
            tag = self.edge[self.from_or_to + "Tag"][0]['tag']
        elif self.from_or_to + "EntityTag" in self.edge:
            tag = self.edge[self.from_or_to + "EntityTag"]
        elif self.from_or_to + "TagMap" in self.edge and self.node in self.edge[self.from_or_to + "TagMap"]:
            tag = self.edge[self.from_or_to + "TagMap"][self.node]
        else:
            return False
        Save.save_label(self.node, tag)
        return True

    def cut(self) -> bool:
        if self.is_count():
            return True
        if self.is_inaccount():
            return True
        if self.is_tag():
            return True
        return False


class OKNodecut(ABCNodecut):
    def __init__(self, node, len_edges):
        self.node = node
        self.len_edges = len_edges

    #  剪掉出度超过阈值
    def is_outof_len(self) -> bool:
        if self.len_edges > config.MAXN_LEN_EDGES:
            return True
        return False

    # 节点剪枝
    def cut(self) -> bool:
        if self.node in config.white:
            return False
        if self.node in config.black:
            return True
        if self.is_outof_len():
            return True
        return False
