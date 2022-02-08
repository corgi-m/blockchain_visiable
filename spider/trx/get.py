# coding=utf-8
from spider.net import req_get
from config import config, count
from utils import outof_list
from spider.trx.cuts import Edgecut, Nodecut
from spider.save import save_balance
import json


def get_nodes(address, res) -> set[str]:  # 下一级节点的集合。
    if res is None:
        return set()
    data = json.loads(res.text)
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


def get_total(res) -> int:  # 下一级节点个数
    if res is None:
        return 0
    data = json.loads(res.text)
    return data['data']['total']


def get_total_transfer(address) -> int:  # 下一级节点个数
    params = {"tokenType": "TRC20", "contractAddress": address}
    res = req_get(config['trxtransfer'], params)
    return get_total(res)


def get_total_transaction(address) -> int:  # 下一级节点个数
    params = {"address": address}
    res = req_get(config['trxtransaction'], params)
    return get_total(res)


# 转账
def get_nodes_transfer(address, offset, limit) -> set[str]:  # 下一级节点的集合。
    params = {"offset": offset, "limit": limit, "tokenType": "TRC20", "contractAddress": address}
    res = req_get(config['trxtransfer'], params)
    return get_nodes(address, res)


# 交易
def get_nodes_transaction(address, offset, limit) -> set[str]:  # 下一级节点的集合。
    params = {"address": address, "offset": offset, "limit": limit}
    res = req_get(config['trxtransaction'], params)
    return get_nodes(address, res)


def get_next_nodes(node) -> set[str]:  # 下一级节点的集合。
    # get length
    len_edges_transfer = get_total_transfer(node)
    len_edges_transaction = get_total_transaction(node)
    next_nodes = set()
    length = len_edges_transfer + len_edges_transaction

    # cut node
    nodecut = Nodecut(node, length)
    if nodecut.cut():
        return next_nodes

    # transfers
    for page in range(0, len_edges_transfer, 100):
        next_nodes |= get_nodes_transfer(node, page, 100)
    # transactions
    for page in range(0, len_edges_transaction, 100):
        next_nodes |= get_nodes_transaction(node, page, 100)
    return next_nodes


def get_balance(address) -> list[dict]:  # 代币列表
    balances = []
    balances.extend(get_trc(address, "TRC20"))
    balances.extend(get_trc(address, "TRC10"))
    balances.extend(get_trx(address))
    return balances


def get_trc(address, trc_type) -> list[dict]:  # 代币列表
    res = req_get(config['trxholdertrc20'].format(address, trc_type))
    if res is None:
        return []
    data = json.loads(res.text)
    # print(data["data"]["hits"])
    if "hits" in data["data"] and data["data"]["hits"] is not None:
        return data["data"]["hits"]
    return []


def get_trx(address) -> list[dict]:  # 代币列表
    res = req_get(config['trxinfo'].format(address))
    if res is None:
        return []
    data = json.loads(res.text)
    return [{"symbol": "TRX", "value": data["data"]["balance"]}]


def final() -> None:  # 保存balance
    for address in count:
        balances = get_balance(address)
        bals = []
        if balances is not None:
            for i in balances:
                bals.append(i["symbol"] + ',' + str(i["value"]))
            save_balance(address, ';'.join(bals))
    return
