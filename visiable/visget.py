# coding=utf-8
from visiable.vismodel import Balance, Edge, nodesappear, Node
from config import config
from visiable.viscut import pre_cut, post_cut, count, node_cut


def get_label(address, labels) -> str or None:
    if address not in labels:
        return None
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


def get_next_nodes(node, edges_get, from_or_to) -> set[Node]:
    next_nodes = set()

    for edge in node.edges_generate(from_or_to):

        remote = edge.nodeto if from_or_to == 'to' else edge.nodefrom
        if pre_cut(edge, remote):
            continue

        edges_get.append(edge)
        if from_or_to == 'to':
            remote.to_relation = node.to_relation
        else:
            remote.from_relation = node.from_relation

        if post_cut(edge, remote, from_or_to):
            continue
        next_nodes.add(remote)
        count[from_or_to].add(remote)

    return next_nodes


def get_edges(nodes, from_or_to) -> list[Edge]:
    for node in nodes:
        node.to_relation = {node}
        node.from_relation = {node}
        count[from_or_to].add(node)
    edges_get: list[Edge] = []
    nodesappear[from_or_to].append(nodes)
    node_exits = set()
    node_exits |= nodes
    # while len(nodes) != 0:
    for _ in range(config['TURN']):
        next_nodes = set()

        for node in nodes:
            if node_cut(node, from_or_to):
                continue
            next_nodes |= get_next_nodes(node, edges_get, from_or_to)

        nodes = next_nodes - node_exits
        node_exits |= nodes
        nodesappear[from_or_to].append(nodes)
    return edges_get
