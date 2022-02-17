# coding=utf-8
import grequests

from model import Balance
from spider.trx.cut import Edgecut, Nodecut

from spider.common.get import ABCGet

from spider.save import save_balance
from spider.spider import count

from net import greq_get

from config import config
from utils import outof_list

import json


def get_trc(address, trc_type) -> list[dict]:  # 代币列表
    params = {"limit": "100"}
    return greq_get(config['trcholder'].format(address, trc_type), params)


def get_balance_trc(res):
    if res is None:
        return []
    print(res.url, res.text)
    try:
        data = json.loads(res.text)
    except:
        return []
    if "hits" in data["data"] and data["data"]["hits"] is not None:
        return [i["symbol"] + ',' + str(i["value"]) for i in data["data"]["hits"]]
    return []


def get_trx(address) -> list[dict]:  # 代币列表
    return greq_get(config['trxholder'].format(address))


def get_balance_trx(res):
    if res is None:
        return []
    try:
        data = json.loads(res.text)
    except:
        return []
    return ["TRX," + str(data["data"]["balance"])]


def get_total(res) -> int:  # 下一级节点个数
    if res is None:
        return 0
    print(res.url, res.text)
    try:
        data = json.loads(res.text)
    except:
        return 0
    if data["code"] != 0:
        return 0
    return data['data']['total']


def get_nodes(address, res) -> set[str]:  # 下一级节点的集合。
    if res is None:
        return set()
    print(res.url, res.text)
    try:
        data = json.loads(res.text)
    except:
        return set()
    if data["code"] != 0:
        return set()
    hits = data["data"]["hits"]
    nodesto = set()
    nodesfrom = set()
    for i in hits:
        if outof_list(i['from']) == address:
            edgecut = Edgecut(i, "to")
            if not edgecut.cut():
                nodesto.add(i["to"])
        else:
            edgecut = Edgecut(i, "from")
            if not edgecut.cut():
                nodesfrom.add(i["from"])
    return nodesto | nodesfrom


def get_total_transfer(address) -> int:  # 下一级节点个数
    params = {"tokenType": "TRC20", "contractAddress": address}
    return greq_get(config['trxtransfer'], params)


def get_total_transaction(address) -> int:  # 下一级节点个数
    params = {"address": address}
    return greq_get(config['trxtransaction'], params)


def get_nodes_transfer(address, offset, limit) -> set[str]:  # 下一级节点的集合。
    params = {"offset": offset, "limit": limit, "tokenType": "TRC20", "contractAddress": address,
              "sort": "blocktime,desc"}
    return greq_get(config['trxtransfer'], params)


def get_nodes_transaction(address, offset, limit) -> set[str]:  # 下一级节点的集合。
    params = {"address": address, "offset": offset, "limit": limit}
    return greq_get(config['trxtransaction'], params)


class Get(ABCGet):
    def __init__(self):
        ...

    @classmethod
    def get_next_nodes(cls, nodes):
        len_edges_transfer_req = []
        len_edges_transfer = []
        len_edges_transaction_req = []
        len_edges_transaction = []
        for node in nodes:
            len_edges_transfer_req.append(get_total_transfer(node))
        print('start get len')
        len_edges_transfer_res = grequests.map(len_edges_transfer_req)
        print("get len over")
        for node in nodes:
            len_edges_transaction_req.append(get_total_transaction(node))
        print('start get len')
        len_edges_transaction_res = grequests.map(len_edges_transaction_req)
        print("get len over")
        for i in len_edges_transfer_res:
            len_edges_transfer.append(get_total(i))
        for i in len_edges_transaction_res:
            len_edges_transaction.append(get_total(i))
        next_nodes_req = []
        node_addr = []
        for i in range(len(nodes)):
            nodecut = Nodecut(nodes[i], max(len_edges_transaction[i], len_edges_transfer[i]))
            if nodecut.cut():
                continue
            else:
                for page in range(0, len_edges_transfer[i], 100):
                    next_nodes_req.append(get_nodes_transfer(nodes[i], page, 100))
                    node_addr.append(nodes[i])
                for page in range(0, len_edges_transfer[i], 100):
                    next_nodes_req.append(get_nodes_transfer(nodes[i], page, 100))
                    node_addr.append(nodes[i])
        print('start get res')
        next_nodes_res = grequests.map(next_nodes_req)
        print("get res over")

        next_nodes = set()
        for i in range(len(next_nodes_res)):
            next_nodes |= get_nodes(node_addr[i], next_nodes_res[i])

        print(len(next_nodes))
        return list(next_nodes)

    @classmethod
    def get_info(cls) -> None:  # 保存balance等
        print("save balance")
        trc_req = []
        trx_req = []
        nodes = []
        for address in count:
            if not Balance.is_exist(address):
                trc_req.append(get_trc(address, "TRC20"))
                nodes.append(address)
        trc_res = grequests.map(trc_req)
        for address in nodes:
            if not Balance.is_exist(address):
                trx_req.append(get_trx(address))
        trx_res = grequests.map(trx_req)
        for i in range(len(nodes)):
            balances = []
            trc = get_balance_trc(trc_res[i])
            trx = get_balance_trx(trx_res[i])
            balances.extend(trc)
            balances.extend(trx)
            save_balance(nodes[i], ';'.join(balances))
        return
