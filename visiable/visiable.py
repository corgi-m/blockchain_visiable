# coding=utf-8
from config import config, init
from model import Transfer, Balance, Label
from visiable.visdraw import graph_init, draw_nodes, draw_edges, graph_save
from visiable.visecharts import setnodes, setedges, drawecharts
from visiable.visget import get_edges, get_balance, get_label
from visiable.vismodel import Node, nodesmap, edgesmap, nodesappear


# from visiable.visdraw import draw_nodes, draw_edges, graph_init, graph_save


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

    # G_from, G_to = graph_init()

    edges = {'from': get_edges({nodesmap[node] for node in config["visnodes"] if node in nodesmap}, 'from'),
             'to': get_edges({nodesmap[node] for node in config["visnodes"] if node in nodesmap}, 'to')}

    nodes = setnodes(nodesappear['to'], 'to')
    edges = setedges(edges['to'], 'to')
    drawecharts(nodes, edges)
    '''draw_nodes(G_from, nodesappear['from'], 'from')
    draw_nodes(G_to, nodesappear['to'], 'to')

    draw_edges(G_from, edges['from'])
    draw_edges(G_to, edges['to'])

    graph_save(G_from, 'result_from.svg')
    graph_save(G_to, 'result_to.svg')'''


if __name__ == "__main__":
    init()
