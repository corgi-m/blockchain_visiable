from config import config, init, count
from model import Transfer, Balance
from vismodel import Node, Edge, balances, nodesmap, edgesmap, nodesappear
from viscut import pre_cut, post_cut
import graphviz as gv
from visdraw import *
from visutils import get_balance


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


def getedges(nodes_get):
    edges_get: list[Edge] = []
    nodesappear.append(nodes_get)

    for _ in range(config['TURN']):
        next_nodes = set()

        for node in nodes_get:
            next_nodes |= get_next_nodes(node, edges_get)

        nodes_get = next_nodes - nodes_get
        nodesappear.append(nodes_get)
    return edges_get


def vismain():
    vis_init()
    G = gv.Digraph(format='svg')
    G.graph_attr.update(ranksep='10', rankdir='LR')

    nodes = [nodesmap[node] for node in config["visnodes"]]
    for node in nodes:
        node.relation = {node}
        count.add(node)
    edges = getedges(set(nodes))

    draw_nodes(G, nodesappear)
    draw_edges(G, edges)

    f = open("result\svg.svg", "w")
    print(G.pipe().decode('utf-8'), file=f)


if __name__ == "__main__":
    init()

# comment
