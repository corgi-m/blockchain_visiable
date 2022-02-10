# coding=utf-8
from spider.eth.cut import Edgecut, Nodecut

from spider.common.get import ABCGet

from spider.save import save_balance
from spider.spider import count

from net import req_get

from config import config
from utils import outof_list

import json


def get_erc(address, tokentype) -> list[dict]:  # 代币列表
    params = {"limit": "100", 'tokenType': tokentype}
    res = req_get(config['ercholder'].format(address), params)
    if res is None:
        return []
    data = json.loads(res.text)
    if "hits" in data["data"] and data["data"]["hits"] is not None:
        return data["data"]["hits"]
    return []


def get_eth(address) -> list[dict]:  # 代币列表
    res = req_get(config['trxholder'].format(address))
    if res is None:
        return []
    data = json.loads(res.text)
    return [{"symbol": "TRX", "value": data["data"]["balance"]}]


def get_balance(address) -> list[dict]:  # 代币列表
    balances = []
    balances.extend(get_erc(address, "ERC20"))
    balances.extend(get_erc(address, "ERC721"))
    balances.extend(get_erc(address, "ERC1155"))
    balances.extend(get_eth(address))
    return balances


def get_total(res) -> int:  # 下一级节点个数
    if res is None:
        return 0
    data = json.loads(res.text)
    return data['data']['total']


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


def get_total_transfer(address, tokentype) -> int:  # 下一级节点个数
    params = {"tokenType": tokentype}
    res = req_get(config['ethtransfer'].format(address), params)
    return get_total(res)


def get_total_transaction(address) -> int:  # 下一级节点个数
    res = req_get(config['ethtransaction'].format(address))
    return get_total(res)


def get_nodes_transfer(address, tokentype, offset, limit) -> set[str]:  # 下一级节点的集合。
    params = {"offset": offset, "limit": limit, "tokenType": tokentype}
    res = req_get(config['ethtransfer'].format(address), params)
    return get_nodes(address, res)


def get_nodes_transaction(address, offset, limit) -> set[str]:  # 下一级节点的集合。
    params = {"offset": offset, "limit": limit, "type": 2}
    res = req_get(config['ethtransaction'].format(address), params)
    return get_nodes(address, res)


class Get(ABCGet):
    def __init__(self):
        ...

    @classmethod
    def get_next_nodes(cls, node) -> set[str]:  # 下一级节点的集合。
        # get length
        len_edges_transfer_erc20 = get_total_transfer(node, 'ERC20')
        len_edges_transfer_erc721 = get_total_transfer(node, 'ERC721')
        len_edges_transfer_erc1155 = get_total_transfer(node, 'ERC1155')
        len_edges_transaction = get_total_transaction(node)
        print(len_edges_transfer_erc20, len_edges_transfer_erc721, len_edges_transfer_erc1155, len_edges_transaction)
        next_nodes = set()
        length = \
            len_edges_transfer_erc20 + len_edges_transfer_erc721 + len_edges_transfer_erc1155 + len_edges_transaction

        # cut node
        nodecut = Nodecut(node, length)
        if nodecut.cut():
            return next_nodes

        # transfers
        for page in range(0, len_edges_transfer_erc20, 100):
            next_nodes |= get_nodes_transfer(node, 'ERC20', page, 100)
        for page in range(0, len_edges_transfer_erc721, 100):
            next_nodes |= get_nodes_transfer(node, 'ERC721', page, 100)
        for page in range(0, len_edges_transfer_erc1155, 100):
            next_nodes |= get_nodes_transfer(node, 'ERC1155', page, 100)
        # transactions
        for page in range(0, len_edges_transaction, 100):
            next_nodes |= get_nodes_transaction(node, page, 100)
        return next_nodes

    @classmethod
    def get_info(cls) -> None:  # 保存balance等
        for address in count:
            balances = get_balance(address)
            bals = []
            if balances is not None:
                for i in balances:
                    bals.append(i["symbol"] + ',' + str(i["value"]))
                save_balance(address, ';'.join(bals))
        return
