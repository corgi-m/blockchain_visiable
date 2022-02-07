from config import config, init
from model import Transfer, Balance
from visiable.visget import getedges, get_balance
from visiable.vismodel import Node, balances, nodesmap, edgesmap, nodesappear
from visiable.visdraw import draw_nodes, draw_edges, graph_init, graph_save


def vis_init():
    edges_init: list[any] = Transfer.get()
    for i in Balance.get():
        balances[i[0]] = i[1]
    for edge in edges_init:
        edge = dict(zip(Transfer.column(), edge))
        if edge['addrfrom'] not in nodesmap:
            nodesmap[edge['addrfrom']] = Node(address=edge['addrfrom'], balance=get_balance(edge['addrfrom']))
        if edge['addrto'] not in nodesmap:
            nodesmap[edge['addrto']] = Node(address=edge['addrto'], balance=get_balance(edge['addrfrom']))
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
