# coding=utf-8

from abc import ABC, abstractmethod

from model import Balance
from spider.common.get import ABCGet
from spider.oklink.cut import OKEdgecut, OKNodecut
from spider.save import Save
from spider.spider import count

from utils import Utils, Json
from net import Net


class OKlink(ABC):
    __linkname = 'OKlink'

    @staticmethod
    @abstractmethod
    def get_other(address) -> list[Net.AsyncRequest]:  # 代币列表
        ...

    @staticmethod
    @abstractmethod
    def get_main(address) -> list[Net.AsyncRequest]:  # 代币列表
        ...

    @staticmethod
    @abstractmethod
    def get_total_transfer(address) -> list[Net.AsyncRequest]:
        ...

    @staticmethod
    @abstractmethod
    def get_total_transaction(address) -> list[Net.AsyncRequest]:
        ...

    @staticmethod
    @abstractmethod
    def get_nodes_transfer(address, offset, limit) -> list[Net.AsyncRequest]:
        ...

    @staticmethod
    @abstractmethod
    def get_nodes_transaction(address, offset, limit) -> list[Net.AsyncRequest]:
        ...

    @staticmethod
    def get_balance_other(res) -> list[str]:
        if res is None:
            return []
        data = Json.loads(res.text)
        if data is None:
            return []
        if "hits" in data["data"] and data["data"]["hits"] is not None:
            return [i["symbol"] + ',' + str(i["value"]) for i in data["data"]["hits"]]
        return []

    @classmethod
    def get_balance_main(cls, res) -> list[str]:
        if res is None:
            return []
        data = Json.loads(res.text)
        if data is None:
            print(res.text)
            return []
        return [cls.__linkname + "," + str(data["data"]["balance"])]

    @staticmethod
    def get_total(res) -> int:
        if res is None:
            return 0
        data = Json.loads(res.text)
        if data is None or data["code"] != 0:
            print(res.text)
            return 0
        return data['data']['total']

    @staticmethod
    def get_nodes(address, res) -> set[str]:  # 下一级节点的集合。
        if res is None:
            return set()
        data = Json.loads(res.text)
        if data is None or data["code"] != 0:
            return set()
        hits = data["data"]["hits"]
        nodesto = set()
        nodesfrom = set()
        for i in hits:
            if Utils.outof_list(i['from']) == address:
                edgecut = OKEdgecut(i, "to")
                if not edgecut.cut():
                    nodesto.add(i["to"])
            else:
                edgecut = OKEdgecut(i, "from")
                if not edgecut.cut():
                    nodesfrom.add(i["from"])
        return nodesto | nodesfrom

    @classmethod
    def get_next_nodes_req(cls, nodes, len_edges_transaction, len_edges_transfer, node_addr) -> list[Net.AsyncRequest]:
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

    def __init__(self, Link):
        self.Link = Link

    def get_next_nodes(self, nodes) -> set[str]:
        print('start get len')
        len_edges_transfer_req = []
        len_edges_transfer = []
        len_edges_transaction_req = []
        len_edges_transaction = []
        for node in nodes:
            len_edges_transfer_req.append(self.Link.get_total_transfer(node))
        len_edges_transfer_res = Net.greq_map(len_edges_transfer_req)
        for node in nodes:
            len_edges_transaction_req.append(self.Link.get_total_transaction(node))
        len_edges_transaction_res = Net.greq_map(len_edges_transaction_req)
        for i in len_edges_transfer_res:
            len_edges_transfer.append(self.Link.get_total(i))
        for i in len_edges_transaction_res:
            len_edges_transaction.append(self.Link.get_total(i))

        print('start get res')
        node_addr = []
        next_nodes_res = []
        for next_nodes_req in self.Link.get_next_nodes_req(nodes, len_edges_transaction, len_edges_transfer, node_addr):
            next_nodes_res.extend(Net.greq_map(next_nodes_req))
        next_nodes = set()
        for i in range(len(next_nodes_res)):
            next_nodes |= self.Link.get_nodes(node_addr[i], next_nodes_res[i])
        return next_nodes

    def get_info(self) -> None:
        print("get balance")
        other_req = []
        main_req = []
        nodes = []
        for address in count:
            if not Balance.is_exist(address):
                other_req.append(self.Link.get_other(address))
                nodes.append(address)
        other_res = Net.greq_map(other_req)
        for address in count:
            if not Balance.is_exist(address):
                main_req.append(self.Link.get_main(address))
        main_res = Net.greq_map(main_req)

        print("save balance")
        for i in range(len(nodes)):
            balances = []
            erc = self.Link.get_balance_other(other_res[i])
            eth = self.Link.get_balance_main(main_res[i])
            balances.extend(erc)
            balances.extend(eth)
            Save.save_balance(nodes[i], ';'.join(balances))
        return
