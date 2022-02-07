from config import config, init, count
from model import Transfer, Balance
from visget import getedges, get_balance
from vismodel import Node, balances, nodesmap, edgesmap, nodesappear
import graphviz as gv
from visdraw import draw_nodes, draw_edges


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
    G = gv.Digraph(format='svg')
    G.graph_attr.update(ranksep='10', rankdir='LR')

    edges = getedges({nodesmap[node] for node in config["visnodes"]})

    draw_nodes(G, nodesappear)
    draw_edges(G, edges)

    print(G.pipe().decode('utf-8'), file=config["save"])


if __name__ == "__main__":
    init()

# comment
