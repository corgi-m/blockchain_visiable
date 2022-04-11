# coding=utf-8

from abc import ABC, abstractmethod

from config import config
from model import Label
from net import Net
from spider.common.get import ABCGet
from spider.oklink.cut import OKEdgecut, OKNodecut
from spider.save import Save
from spider.spider import count
from utils import Utils, Json, Date


# Oklink父类
class OKlink(ABC):
    __linkname = 'OKlink'

    # 获取其他代币
    @staticmethod
    @abstractmethod
    def get_other(address) -> list[Net.AsyncRequest]:
        ...

    # 获取主链代币
    @staticmethod
    @abstractmethod
    def get_main(address) -> list[Net.AsyncRequest]:
        ...

    # 获取交易数量
    @staticmethod
    @abstractmethod
    def get_total_transfer(address) -> list[Net.AsyncRequest]:
        ...

    # 同上
    @staticmethod
    @abstractmethod
    def get_total_transaction(address) -> list[Net.AsyncRequest]:
        ...

    # 获取交易记录
    @staticmethod
    @abstractmethod
    def get_nodes_transfer(address, offset, limit) -> list[Net.AsyncRequest]:
        ...

    # 同上
    @staticmethod
    @abstractmethod
    def get_nodes_transaction(address, offset, limit) -> list[Net.AsyncRequest]:
        ...

    # 获取内部交易
    @staticmethod
    @abstractmethod
    def get_internal_transfer(address, offset, limit) -> list[Net.AsyncRequest]:
        ...

    # 内部交易主代币
    @staticmethod
    @abstractmethod
    def get_internal_main(offset, limit, tranHash) -> list[Net.AsyncRequest]:
        ...

    # 内部交易其他代币
    @staticmethod
    @abstractmethod
    def get_internal_other(offset, limit, tranHash) -> list[Net.AsyncRequest]:
        ...

    # 解析其他代币数量
    @staticmethod
    def parse_balance_other(res) -> list[str]:
        if res is None:
            return []
        data = Json.loads(res.text)
        if data is None or "code" not in data or data["code"] != 0:
            print("get_balance_other")
            return []
        if "hits" in data["data"] and data["data"]["hits"] is not None:
            return [i["symbol"] + ',' + str(i["value"]) for i in data["data"]["hits"]]
        return []

    # 解析主链代笔数量
    @classmethod
    def parse_balance_main(cls, res) -> list[str]:
        if res is None:
            return []
        data = Json.loads(res.text)
        if data is None or "data" not in data or "balance" not in data["data"]:
            print("get_balance_main")
            return []
        return [cls.__linkname + "," + str(data["data"]["balance"])]

    # 解析交易数量
    @staticmethod
    def parse_total(res) -> int:
        if res is None:
            return 0
        data = Json.loads(res.text)
        if data is None or "code" in data and data["code"] != 0 or "status" in data and data["status"] == 404:
            print("get_total")
            return 0
        return data['data']['total']

    # 解析交易内容
    @staticmethod
    def parse_nodes(address, res, from_or_to) -> set[str]:  # 下一级节点的集合。
        if res is None:
            return set()
        data = Json.loads(res.text)
        if data is None or "code"not in data or data["code"] != 0 or "hits" not in data["data"]:
            return set()
        hits = data["data"]["hits"]
        nodes = set()
        for i in hits:
            if Utils.outof_list(i[from_or_to]) != address:
                edgecut = OKEdgecut(i, from_or_to)
                if not edgecut.cut():
                    nodes.add(i[from_or_to])
        return nodes

    @staticmethod
    def parse_internal_transfer(address, res):
        if res is None:
            return set()
        data = Json.loads(res.text)
        if data is None or data["code"] != 0:
            return set()
        hits = data["data"]["hits"]
        return [(i["txhash"], address, Date.date_transform(i["blocktime"]/100)) for i in hits]

    @staticmethod
    def parse_internal_value(address, internal_main_res, internal_other_res):
        fromtoken = None
        fromvalue = None
        totoken = None
        tovalue = None
        if internal_main_res is None or internal_other_res is None:
            return fromtoken, fromvalue, totoken, tovalue
        main_data = Json.loads(internal_main_res.text)
        other_data = Json.loads(internal_other_res.text)
        if main_data is None or other_data is None or main_data["code"] != 0 or other_data["code"] != 0:
            return fromtoken, fromvalue, totoken, tovalue
        pairs = []
        for i in main_data["data"]["hits"] + other_data["data"]["hits"]:
            pairs.append((i["from"], i["to"]))
            if i["from"] == address:
                fromtoken = i["symbol"] if "symbol" in i else config.db.dbname
                fromvalue = i["value"]
            if i["to"] == address:
                totoken = i["symbol"] if "symbol" in i else config.db.dbname
                tovalue = i["value"]
        return fromtoken, fromvalue, totoken, tovalue

    @classmethod
    def get_internal_req(cls, nodes, len_edges_internal, node_addr) -> list[Net.AsyncRequest]:
        flag = 0
        internal_req = []
        for i, node in enumerate(nodes):
            for page in range(0, min(len_edges_internal[i], 1), 100):
                internal_req.append(cls.get_internal_transfer(node, page, 100))
                node_addr.append(node)
                flag += 1
                if len(internal_req) >= 8000:
                    yield internal_req
                    flag = 0
                    internal_req = []
        yield internal_req

    @classmethod
    def get_internal_value_req(cls, info):
        flag = 0
        internal_main_req = []
        internal_other_req = []
        for transferhash, _, _ in info:
            internal_main_req.append(cls.get_internal_main(0, 100, transferhash))
            internal_other_req.append(cls.get_internal_other(0, 100, transferhash))
            flag += 1
            if len(internal_main_req) * 2 >= 8000:
                yield internal_main_req, internal_other_req
                flag = 0
                internal_main_req = []
                internal_other_req = []
        yield internal_main_req, internal_other_req

    # 获取下一级节点的请求列表
    @classmethod
    def get_next_nodes_req(cls, nodes, len_edge, node_addr) -> list[Net.AsyncRequest]:

        len_edges_transaction = len_edge[0]
        len_edges_transfer = len_edge[1]

        flag = 0
        next_nodes_req = []
        for i, node in enumerate(nodes):
            nodecut = OKNodecut(node, max(len_edges_transaction[i], len_edges_transfer[i]))
            if not nodecut.cut():

                for page in range(0, min(len_edges_transfer[i], 9900), 100):
                    next_nodes_req.append(cls.get_nodes_transfer(node, page, 100))
                    node_addr.append(node)
                    flag += 1
                    if len(next_nodes_req) >= 8000:
                        yield next_nodes_req
                        flag = 0
                        next_nodes_req = []

                for page in range(0, min(len_edges_transaction[i], 9900), 100):
                    next_nodes_req.append(cls.get_nodes_transaction(node, page, 100))
                    node_addr.append(node)
                    flag += 1
                    if len(next_nodes_req) >= 8000:
                        yield next_nodes_req
                        flag = 0
                        next_nodes_req = []

        yield next_nodes_req


class OKGet(ABCGet):

    def __init__(self, link):
        self.__link = link
        self.__nodeslist = None

    def get_len_edges(self, nodes):
        len_edges_transfer_req = []
        len_edges_transaction_req = []
        len_edges_transfer = []
        len_edges_transaction = []
        for node in nodes:
            len_edges_transfer_req.append(self.__link.get_total_transfer(node))
            len_edges_transaction_req.append(self.__link.get_total_transaction(node))
            if len(len_edges_transfer_req) >= 2000:
                len_edges_transfer_res = Net.greq_map(len_edges_transfer_req)
                len_edges_transaction_res = Net.greq_map(len_edges_transaction_req)
                len_edges_transfer_req = []
                len_edges_transaction_req = []
                for i in len_edges_transfer_res:
                    len_edges_transfer.append(self.__link.parse_total(i))
                for i in len_edges_transaction_res:
                    len_edges_transaction.append(self.__link.parse_total(i))
        len_edges_transfer_res = Net.greq_map(len_edges_transfer_req)
        len_edges_transaction_res = Net.greq_map(len_edges_transaction_req)
        for i in len_edges_transfer_res:
            len_edges_transfer.append(self.__link.parse_total(i))
        for i in len_edges_transaction_res:
            len_edges_transaction.append(self.__link.parse_total(i))
        return [len_edges_transfer, len_edges_transaction]

    def get_next_nodes(self, nodes, from_or_to) -> set[str]:
        print('start get len')
        len_edges = self.get_len_edges(nodes)
        print('start get res')
        node_addr = []
        next_nodes_res = []
        for next_nodes_req in self.__link.get_next_nodes_req(nodes, len_edges, node_addr):
            next_nodes_res.extend(Net.greq_map(next_nodes_req))
        next_nodes = set()
        for i in range(len(next_nodes_res)):
            next_nodes |= self.__link.parse_nodes(node_addr[i], next_nodes_res[i], from_or_to)
        return next_nodes

    def save_balance(self):
        print("get balance")
        other_req = []
        main_req = []
        other_res = []
        main_res = []
        for address in self.__nodeslist:
            other_req.append(self.__link.get_other(address))
            main_req.append(self.__link.get_main(address))
            if len(other_req) > 2000:
                other_res.extend(Net.greq_map(other_req))
                main_res.extend(Net.greq_map(main_req))
                other_req = []
                main_req = []

        other_res.extend(Net.greq_map(other_req))
        main_res.extend(Net.greq_map(main_req))

        print("save balance")
        for i in range(len(self.__nodeslist)):
            balances = []
            erc = self.__link.parse_balance_other(other_res[i])
            eth = self.__link.parse_balance_main(main_res[i])
            balances.extend(erc)
            balances.extend(eth)
            Save.save_balance(self.__nodeslist[i], ';'.join(balances))
        return

    def get_len_edges_internal(self):
        len_edges_internal_req = []
        len_edges_internal = []

        for node in self.__nodeslist:
            len_edges_internal_req.append(self.__link.get_total_internal(node))
        len_edges_internal_res = Net.greq_map(len_edges_internal_req)

        for i in len_edges_internal_res:
            len_edges_internal.append(self.__link.parse_total(i))
        return len_edges_internal

    def get_info_iternal(self, len_edges_internal):
        internal_res = []
        node_addr = []
        for internal_req in self.__link.get_internal_req(self.__nodeslist, len_edges_internal, node_addr):
            internal_res.extend(Net.greq_map(internal_req))
        info = []  # transferhash, address, blocktime
        for i, res in enumerate(internal_res):
            for j in self.__link.parse_internal_transfer(node_addr[i], res):
                info.append(j)
        return info

    def get_iternal(self, info_internal):
        internal_main_res = []
        internal_other_res = []
        for internal_main_req, internal_other_req in self.__link.get_internal_value_req(info_internal):
            internal_main_res.extend(Net.greq_map(internal_main_req))
            internal_other_res.extend(Net.greq_map(internal_other_req))

        for i in range(len(info_internal)):
            fromtoken, fromvalue, totoken, tovalue = \
                self.__link.parse_internal_value(info_internal[i][1], internal_main_res[i], internal_other_res[i])
            if fromtoken and fromvalue and totoken and tovalue:
                yield info_internal[i][0], info_internal[i][1], fromtoken, fromvalue, totoken, tovalue, \
                      info_internal[i][2]

    def save_internal(self):
        print("get internal")
        len_edges_internal = self.get_len_edges_internal()
        info_internal = self.get_info_iternal(len_edges_internal)
        print("save internal")
        for transferhash, address, fromtoken, fromvalue, totoken, tovalue, blocktime in self.get_iternal(info_internal):
            Save.save_internal(transferhash, address, fromtoken, fromvalue, totoken, tovalue, blocktime)

    def get_info(self) -> None:
        self.__nodeslist = [i for i in count['from'] | count['to'] if not Label.get(i)]
        print('total nodes count: ' + str(len(self.__nodeslist)))
        self.save_balance()
        #self.save_internal()
