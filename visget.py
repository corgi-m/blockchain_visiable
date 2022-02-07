from vismodel import Balance, balances, Edge, nodesappear
from config import count, config
from viscut import pre_cut, post_cut


def get_balance(address) -> Balance:
    res = {}
    if address not in balances:
        return res
    balance = balances[address]
    for balan in balance.split(';'):
        temp = balan.split(',')
        res[temp[0]] = float(temp[1])
    return res


def get_next_nodes(node, edges_get):
    next_nodes = set()

    for edge in node.edges_generate():

        if pre_cut(edge):
            continue

        edges_get.append(edge)
        edge.nodeto.relation = edge.nodefrom.relation

        if post_cut(edge):
            continue

        next_nodes.add(edge.nodeto)
        count.add(edge.nodeto)
    return next_nodes


def getedges(nodes):
    for node in nodes:
        node.relation = {node}
        count.add(node)
    edges_get: list[Edge] = []
    nodesappear.append(nodes)

    for _ in range(config['TURN']):
        next_nodes = set()

        for node in nodes:
            next_nodes |= get_next_nodes(node, edges_get)

        nodes = next_nodes - nodes
        nodesappear.append(nodes)
    return edges_get
