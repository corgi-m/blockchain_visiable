# coding=utf-8
from config import config, init
from model import Transfer, Balance, Label
from visiable.visecharts import setnodes, setedges, drawecharts
from visiable.visget import get_edges, get_balance, get_label
from visiable.vismodel import Node, nodesmap, edgesmap, nodesappear


def vis_init():
    edges_init: list[any] = Transfer.get()
    balances = Balance.get()
    labels = Label.get()
    for edge in edges_init:
        edge = dict(zip(Transfer.column(), edge))
        if edge['addrfrom'] not in nodesmap:
            nodesmap[edge['addrfrom']] = Node(address=edge['addrfrom'], balance=get_balance(edge['addrfrom'], balances),
                                              label=get_label(edge['addrfrom'], labels))
        if edge['addrto'] not in nodesmap:
            nodesmap[edge['addrto']] = Node(address=edge['addrto'], balance=get_balance(edge['addrto'], balances),
                                            label=get_label(edge['addrto'], labels))
        edgesmap[edge['transferhash']] = nodesmap[edge['addrfrom']].add_edge(nodesmap[edge['addrto']],
                                                                             (edge['transferhash'],
                                                                              str(edge["blocktime"]), edge["symbol"],
                                                                              edge["value"]))
    return


def vismain():
    vis_init()

    edges = {'from': get_edges({nodesmap[node] for node in config["visnodes"] if node in nodesmap}, 'from'),
             'to': get_edges({nodesmap[node] for node in config["visnodes"] if node in nodesmap}, 'to')}

    nodes_to = setnodes(nodesappear['to'], 'to')
    nodes_from = setnodes(nodesappear['from'], 'from')
    edges_to = setedges(edges['to'])
    edges_from = setedges(edges['from'])
    drawecharts(nodes_to, edges_to, 'to')
    drawecharts(nodes_from, edges_from, 'from')


if __name__ == "__main__":
    init()
