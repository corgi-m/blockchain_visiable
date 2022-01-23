# coding=utf-8
from config import count, config
from model import Count, Balance
from net import req_get
from cuts import edgecut_reg
import json
import time


def outof_list(li):
    return li[0] if isinstance(li, list) else li


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


def save_count(address, value):
    cou = Count(address, value)
    cou.save()


def save_balance(address):
    balances = get_balance(address)
    bals = []
    if balances is not None:
        for i in balances:
            bals.append(i["symbol"] + ',' + str(i["value"]))
        balance = Balance(address, ';'.join(bals))
        balance.save()


def save_data():
    for address in count:
        print(address)
        # save_count(address, value)
        save_balance(address)


def date_transform(timestamp):
    time_local = time.localtime(int(timestamp / 1000))
    datatime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return datatime
