# coding=utf-8

from spider.trx.cut import Edgecut, Nodecut
from spider.common.get import ABCGet
from spider.save import Save
from spider.spider import count

from net import Net
from config import config
from utils import Utils, Json
from model import Balance


def get_trc(address) -> list[Net.AsyncRequest]:  # 代币列表
    params = {"limit": "100"}
    return Net.greq_get(config['trcholder'].format(address, 'TRC20'), params)


# noinspection DuplicatedCode
def get_balance_trc(res):
    if res is None:
        return []
    data = Json.loads(res.text)
    if data is None:
        print(res.text)
        return []
    if "hits" in data["data"] and data["data"]["hits"] is not None:
        return [i["symbol"] + ',' + str(i["value"]) for i in data["data"]["hits"]]
    return []


def get_trx(address) -> list[Net.AsyncRequest]:  # 代币列表
    return Net.greq_get(config['trxholder'].format(address))


def get_balance_trx(res):
    if res is None:
        return []
    data = Json.loads(res.text)
    if data is None:
        print(res.text)
        return []
    return ["TRX," + str(data["data"]["balance"])]


# noinspection DuplicatedCode
def get_total(res) -> int:
    if res is None:
        return 0
    data = Json.loads(res.text)
    if data is None or data["code"] != 0:
        print(res.text)
        return 0
    return data['data']['total']


def get_nodes(address, res) -> set[str]:  # 下一级节点的集合。
    if res is None:
        return set()
    data = Json.loads(res.text)
    if data is None or data["code"] != 0:
        print(res.text)
        return set()
    hits = data["data"]["hits"]
    nodesto = set()
    nodesfrom = set()
    for i in hits:
        if Utils.outof_list(i['from']) == address:
            edgecut = Edgecut(i, "to")
            if not edgecut.cut():
                nodesto.add(i["to"])
        else:
            edgecut = Edgecut(i, "from")
            if not edgecut.cut():
                nodesfrom.add(i["from"])
    return nodesto | nodesfrom


def get_total_transfer(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
    params = {"tokenType": "TRC20", "contractAddress": address}
    return Net.greq_get(config['trxtransfer'], params)


def get_total_transaction(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
    params = {"address": address}
    return Net.greq_get(config['trxtransaction'], params)


def get_nodes_transfer(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
    params = {"offset": offset, "limit": limit, "tokenType": "TRC20",
              "contractAddress": address}  # "sort": "blocktime,asc"
    return Net.greq_get(config['trxtransfer'], params)


def get_nodes_transaction(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
    params = {"address": address, "offset": offset, "limit": limit}
    return Net.greq_get(config['trxtransaction'], params)


# noinspection DuplicatedCode
def get_next_nodes_req(nodes, len_edges_transaction, len_edges_transfer, node_addr):
    flag = 0
    next_nodes_req = []
    for i in range(len(nodes)):
        nodecut = Nodecut(nodes[i], max(len_edges_transaction[i], len_edges_transfer[i]))
        if not nodecut.cut():
            for page in range(0, len_edges_transfer[i], 100):
                next_nodes_req.append(get_nodes_transfer(nodes[i], page, 100))
                node_addr.append(nodes[i])
                flag += 1
                if len(next_nodes_req) >= 8000:
                    yield next_nodes_req
                    flag = 0
                    next_nodes_req = []
            for page in range(0, len_edges_transaction[i], 100):
                next_nodes_req.append(get_nodes_transaction(nodes[i], page, 100))
                node_addr.append(nodes[i])
                flag += 1
                if len(next_nodes_req) >= 8000:
                    yield next_nodes_req
                    flag = 0
                    next_nodes_req = []
    yield next_nodes_req


class Get(ABCGet):
    def __init__(self):
        ...

    # noinspection DuplicatedCode
    @classmethod
    def get_next_nodes(cls, nodes):
        # 获取节点长度
        len_edges_transfer_req = []
        len_edges_transfer = []
        len_edges_transaction_req = []
        len_edges_transaction = []

        for node in nodes:
            len_edges_transfer_req.append(get_total_transfer(node))
        print('start get len')
        len_edges_transfer_res = Net.greq_map(len_edges_transfer_req)
        print("get len over")

        for node in nodes:
            len_edges_transaction_req.append(get_total_transaction(node))
        print('start get len')
        len_edges_transaction_res = Net.greq_map(len_edges_transaction_req)
        print("get len over")
        # 获取下一轮节点
        for i in len_edges_transfer_res:
            len_edges_transfer.append(get_total(i))
        for i in len_edges_transaction_res:
            len_edges_transaction.append(get_total(i))

        node_addr = []
        next_nodes_res = []

        for next_nodes_req in get_next_nodes_req(nodes, len_edges_transaction, len_edges_transfer, node_addr):
            print('start get res')
            next_nodes_res.extend(Net.greq_map(next_nodes_req))
            print("get res over")

        next_nodes = set()

        for i in range(len(next_nodes_res)):
            next_nodes |= get_nodes(node_addr[i], next_nodes_res[i])

        print(next_nodes)

        return list(next_nodes)

    @classmethod
    def get_info(cls) -> None:  # 保存balance等

        print("save balance")

        trc_req = []
        trx_req = []
        nodes = []

        for address in count:
            if not Balance.is_exist(address):
                trc_req.append(get_trc(address))
                nodes.append(address)

        trc_res = Net.greq_map(trc_req)

        for address in nodes:
            if not Balance.is_exist(address):
                trx_req.append(get_trx(address))

        trx_res = Net.greq_map(trx_req)

        for i in range(len(nodes)):
            balances = []
            trc = get_balance_trc(trc_res[i])
            trx = get_balance_trx(trx_res[i])
            balances.extend(trc)
            balances.extend(trx)
            Save.save_balance(nodes[i], ';'.join(balances))

        return
