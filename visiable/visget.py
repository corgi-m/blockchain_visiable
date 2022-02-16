# coding=utf-8
from visiable.vismodel import Balance, Edge, nodesappear, Node
from config import config
from visiable.viscut import pre_cut, post_cut, count, node_cut
from visiable.visutils import relationformat, balanceformat, tip_filter, outof_list


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
        if len(temp) != 2:
            continue
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


def get_node_tips(node, from_or_to, color):
    relation = node.to_relation if from_or_to == 'to' else node.from_relation
    tips = relationformat(relation) + balanceformat(node.balance)
    if color == 'blue':
        tips = node.label + '<br>' + tips
    tips = tip_filter(tips)
    return tips


def get_edge_tips(edge: Edge):
    res = "{0} -> {1}<br>".format(edge.nodefrom.address, edge.nodeto.address)
    form = "{{{1}, {2}: {3}, transferhash: {0}}}<br>"
    for info in edge.info:
        info = outof_list(info)
        res += form.format(info[0], info[1], tip_filter(info[2]), info[3])
    return res


def get_node_color(node: Node, from_or_to):
    hlen = node.to_hlen if from_or_to == 'to' else node.from_hlen
    if node.address in config['black']:
        fillcolor = 'yellow'
    elif node.address in config['gray']:
        fillcolor = 'green'
    elif node.address in config['visnodes']:
        fillcolor = 'red'
    elif node.label is not None:
        fillcolor = 'blue'
    elif hlen > config['MAX_OUT_DEGREE']:
        fillcolor = 'deeppink'
    else:
        fillcolor = 'black'
    return fillcolor


def get_edge_color(edge: Edge):
    value = 0
    count = 0
    fillcolor = 'black'
    for i in edge.info:
        if i[2] == 'USDT':
            count += 1
            value += i[3]
    if value > config['THRESHOLD_OF_VALUE']:
        fillcolor = 'red'
    elif len(edge.info) > config['THRESHOLD_OF_COUNT']:
        fillcolor = 'yellow'
    return fillcolor
