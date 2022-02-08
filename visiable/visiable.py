# coding=utf-8
from config import config, init
from model import Transfer, Balance, Label
from visiable.visget import get_to_edges, get_balance, get_label, get_from_edges
from visiable.vismodel import Node, nodesmap, edgesmap, nodesappear_from, nodesappear_to
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
        edgesmap[edge['transferhash']] = nodesmap[edge['addrfrom']].add_to_edge(nodesmap[edge['addrto']], [
            (edge['transferhash'], str(edge["blocktime"]), edge["symbol"], edge["value"])])
    return


def vismain():
    vis_init()

    G_from, G_to = graph_init()

    edges_from = get_from_edges({nodesmap[node] for node in config["visnodes"]})

    edges_to = get_to_edges({nodesmap[node] for node in config["visnodes"]})

    draw_nodes(G_from, nodesappear_from)
    draw_nodes(G_to, nodesappear_to)

    draw_edges(G_from, edges_from)
    draw_edges(G_to, edges_to)

    graph_save(G_from, 'result_from.svg')
    graph_save(G_to, 'result_to.svg')


if __name__ == "__main__":
    init()
