# coding=utf-8
from config import count, config
from model import Label, Transfer
from utils import outof_list, date_transform, use


#   剪掉合约
def is_notransfer(edge):
    if "contractType" in edge and config['contractType'] not in edge["contractType"]:
        return True
    return False


#  剪掉零交易
def is_novalue(edge):
    if edge["value"] < config['MIN_TRANSFER_VALUE']:
        return True
    return False


#  剪掉重复
def is_count(node):  # 是否出现过，减少重复
    if node in count:
        return True
    count.add(node)
    return False


#  剪掉tag
def is_inaccount(node):
    if node in config['account']:
        return True
    return False


#  剪掉tag
def is_tag(edge, node, tag_name):
    if tag_name in edge and len(edge[tag_name]) > 0:
        config['account'][node] = edge[tag_name]
        label = Label(node, edge[tag_name][0]['tag'])
        label.save()
        return True
    return False


#  剪掉出度超过阈值
def is_outof_len(len_edges):
    if len_edges > config['MAXN_LEN_EDGES']:
        return True
    return False


# 边预剪枝
def pre_cut(edge, node, from_or_to):
    use(from_or_to)
    use(node)
    if is_notransfer(edge):
        return True
    if is_novalue(edge):
        return True
    return False


# 边后剪枝
def post_cut(edge, node, from_or_to):
    if is_count(node):
        return True
    if is_inaccount(node):
        return True
    if is_tag(edge, node, from_or_to + "Tag"):
        return True
    return False


# 边初始化
def init_edge(edge):
    edge["from"] = outof_list(edge["from"])
    edge["to"] = outof_list(edge["to"])
    return edge


# 边剪枝
def edgecut_reg(edge, from_or_to):
    edge = init_edge(edge)
    node = edge[from_or_to]

    if pre_cut(edge, node, from_or_to):
        return True

    transfer = Transfer(edge["txhash"] if "txhash" in edge else edge["hash"], edge["from"], edge["to"], edge["symbol"],
                        edge["value"], date_transform(edge["blocktime"]))
    transfer.save()

    if post_cut(edge, node, from_or_to):
        return True

    return False


# 节点剪枝
def nodecut_reg(node, len_edges):
    use(node)
    if is_outof_len(len_edges):
        return True

    return False
