# coding=utf-8
from spider.common.get import ABCGet
from spider.eth.cut import Edgecut, Nodecut
from spider.save import Save
from spider.spider import count

from net import Net
from config import config
from utils import Utils, Json
from model import Balance


def get_erc(address) -> list[Net.AsyncRequest]:  # 代币列表
    params = {"limit": "100", 'tokenType': 'ERC20'}
    return Net.greq_get(config['ercholder'].format(address), params)


# noinspection DuplicatedCode
def get_blance_erc(res) -> list[str]:  # 代币列表
    if res is None:
        return []
    data = Json.loads(res.text)
    if data is None:
        return []
    if "hits" in data["data"] and data["data"]["hits"] is not None:
        return [i["symbol"] + ',' + str(i["value"]) for i in data["data"]["hits"]]
    return []


def get_eth(address) -> list[Net.AsyncRequest]:  # 代币列表
    return Net.greq_get(config['trxholder'].format(address))


def get_balance_eth(res):
    if res is None:
        return []
    data = Json.loads(res.text)
    if data is None:
        return []
    return ["ETH," + str(data["data"]["balance"])]


# noinspection DuplicatedCode
def get_total(res) -> int:
    if res is None:
        return 0
    data = Json.loads(res.text)
    if data is None or data["code"] != 0:
        return 0
    return data['data']['total']


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
            edgecut = Edgecut(i, "to")
            if not edgecut.cut():
                nodesto.add(i["to"])
        else:
            edgecut = Edgecut(i, "from")
            if not edgecut.cut():
                nodesfrom.add(i["from"])

    return nodesto | nodesfrom


def get_total_transfer(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
    params = {"tokenType": 'ERC20'}
    return Net.greq_get(config['ethtransfer'].format(address), params)


def get_total_transaction(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
    params = {}
    return Net.greq_get(config['ethtransaction'].format(address), params)


def get_nodes_transfer(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
    params = {"offset": offset, "limit": limit, "tokenType": 'ERC20'}
    return Net.greq_get(config['ethtransfer'].format(address), params)


def get_nodes_transaction(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
    params = {"offset": offset, "limit": limit, "type": 2}
    return Net.greq_get(config['ethtransaction'].format(address), params)


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
    def get_next_nodes(cls, nodes) -> list[str]:

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

        for i in len_edges_transfer_res:
            len_edges_transfer.append(get_total(i))
        for i in len_edges_transaction_res:
            len_edges_transaction.append(get_total(i))
        print(len_edges_transfer)
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

        erc_req = []
        eth_req = []
        nodes = []

        for address in count:
            if not Balance.is_exist(address):
                erc_req.append(get_erc(address))
                nodes.append(address)

        erc_res = Net.greq_map(erc_req)

        for address in count:
            if not Balance.is_exist(address):
                eth_req.append(get_eth(address))

        eth_res = Net.greq_map(eth_req)

        for i in range(len(nodes)):
            balances = []
            erc = get_blance_erc(erc_res[i])
            eth = get_balance_eth(eth_res[i])
            balances.extend(erc)
            balances.extend(eth)
            Save.save_balance(nodes[i], ';'.join(balances))

        return
