# coding=utf-8
from visiable.vismodel import Balance, Edge, nodesappear_to,nodesappear_from, Node
from config import count, config
from visiable.viscut import pre_cut, post_cut


def get_label(address, labels) -> str:
    if address not in labels:
        return ""
    else:
        return labels[address]


def get_balance(address, balances) -> Balance:
    res = {}
    if address not in balances:
        return res
    balance = balances[address]
    for balan in balance.split(';'):
        temp = balan.split(',')
        res[temp[0]] = float(temp[1])
    return res


def get_to_next_nodes(node, edges_get) -> set[Node]:
    next_nodes = set()

    for edge in node.to_edges_generate():

        if pre_cut(edge):
            continue

        edges_get.append(edge)
        edge.nodeto.relation = edge.nodefrom.relation

        if post_cut(edge, edge.nodeto):
            continue

        next_nodes.add(edge.nodeto)
        count.add(edge.nodeto)
    return next_nodes


def get_from_next_nodes(node, edges_get) -> set[Node]:
    next_nodes = set()

    for edge in node.from_edges_generate():

        if pre_cut(edge):
            continue

        edges_get.append(edge)
        edge.nodefrom.relation = edge.nodeto.relation

        if post_cut(edge, edge.nodefrom):
            continue

        next_nodes.add(edge.nodefrom)
        count.add(edge.nodefrom)
    return next_nodes


def get_to_edges(nodes) -> list[Edge]:
    for node in nodes:
        node.relation = {node}
        count.add(node)
    edges_get: list[Edge] = []
    nodesappear_to.append(nodes)

    # while len(nodes) != 0:
    for _ in range(config['TURN']):
        next_nodes = set()

        for node in nodes:
            next_nodes |= get_to_next_nodes(node, edges_get)

        nodes = next_nodes - nodes
        nodesappear_to.append(nodes)
    return edges_get


def get_from_edges(nodes) -> list[Edge]:
    for node in nodes:
        node.relation = {node}
        count.add(node)
    edges_get: list[Edge] = []
    nodesappear_from.append(nodes)

    # while len(nodes) != 0:
    for _ in range(config['TURN']):
        next_nodes = set()

        for node in nodes:
            next_nodes |= get_from_next_nodes(node, edges_get)

        nodes = next_nodes - nodes
        nodesappear_from.append(nodes)
    return edges_get
