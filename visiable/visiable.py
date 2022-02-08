# coding=utf-8
from config import config, init
from model import Transfer, Balance, Label
from visiable.visget import getedges, get_balance, get_label
from visiable.vismodel import Node, nodesmap, edgesmap, nodesappear
from visiable.visdraw import draw_nodes, draw_edges, graph_init, graph_save


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
        edgesmap[edge['transferhash']] = nodesmap[edge['addrfrom']].add_edge(nodesmap[edge['addrto']], [
            (edge['transferhash'], str(edge["blocktime"]), edge["symbol"], edge["value"])])
    return nodesmap, edgesmap


def vismain():
    vis_init()

    G = graph_init()

    edges = getedges({nodesmap[node] for node in config["visnodes"]})

    draw_nodes(G, nodesappear)
    draw_edges(G, edges)

    graph_save(G)


if __name__ == "__main__":
    init()
