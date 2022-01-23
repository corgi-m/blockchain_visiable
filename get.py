from config import config
from net import req_get
from cuts import edgecut_reg
from utils import outof_list
import json


def get_nodes(address, res):
    if res is None:
        return set()
    data = json.loads(res.text)
    hits = data["data"]["hits"]
    nodesto = set([i["to"] for i in hits if outof_list(i["from"]) == address and not edgecut_reg(i, "to")])
    nodesfrom = set([i["from"] for i in hits if outof_list(i["to"]) == address and not edgecut_reg(i, "from")])
    return nodesto.union(nodesfrom)


def get_total(res):
    if res is None:
        return 0
    data = json.loads(res.text)
    return data['data']['total']


# 转账
def get_nodes_transfer(address, offset, limit):
    params = {"offset": offset, "limit": limit, "tokenType": "TRC20", "contractAddress": address}
    res = req_get(config['trxtransfer'], params)
    return get_nodes(address, res)


# 交易
def get_nodes_transaction(address, offset, limit):
    params = {"address": address, "offset": offset, "limit": limit}
    res = req_get(config['trxtransaction'], params)
    return get_nodes(address, res)


def get_total_transfer(address):
    params = {"tokenType": "TRC20", "contractAddress": address}
    res = req_get(config['trxtransfer'], params)
    return get_total(res)


def get_total_transaction(address):
    params = {"address": address}
    res = req_get(config['trxtransaction'], params)
    return get_total(res)


def get_balance(address):
    balances = []
    balances.extend(get_trc(address, "TRC20"))
    balances.extend(get_trc(address, "TRC10"))
    balances.extend(get_trx(address))
    return balances


def get_trc(address, trc_type):
    res = req_get(config['trxholdertrc20'].format(address, trc_type))
    if res is None:
        return []
    data = json.loads(res.text)
    # print(data["data"]["hits"])
    if "hits" in data["data"] and data["data"]["hits"] is not None:
        return data["data"]["hits"]
    return []


def get_trx(address):
    res = req_get(config['trxinfo'].format(address))
    if res is None:
        return []
    data = json.loads(res.text)
    return [{"symbol": "TRX", "value": data["data"]["balance"]}]
