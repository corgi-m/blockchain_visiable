from config import config, init
import pygraphviz as pgv
from model import Node, Edge, Transfer

nodesmap: dict[str, Node] = {}
edgesmap: dict[str, Edge] = {}


def vis_init():
    edges_init: list[any] = Transfer.get()
    for edge in edges_init:
        edge = dict(zip(Transfer.column(), edge))
        if edge['addrfrom'] not in nodesmap:
            nodesmap[edge['addrfrom']] = Node(edge['addrfrom'])
        if edge['addrto'] not in nodesmap:
            nodesmap[edge['addrto']] = Node(edge['addrto'])
        edgesmap[edge['transferhash']] = nodesmap[edge['addrfrom']].add_edge(nodesmap[edge['addrto']], [
            (edge['transferhash'], edge["blocktime"], edge["symbol"], edge["value"])])
    return nodesmap, edgesmap


def getedges(nodes_get):
    edges_get: list[Edge] = []
    repeat_nodes: set[Node] = set(nodes_get)
    for _ in range(config['TURN']-1):
        nextnodes = []
        for node in nodes_get:
            for edge in node.edges_generate():
                edges_get.append(edge)
                if edge.nodeto not in repeat_nodes:
                    nextnodes.append(edge.nodeto)
        nodes_get = nextnodes
    return edges_get


if __name__ == "__main__":
    init()
    vis_init()
    G = pgv.AGraph(directed=True)

    nodes = [nodesmap['TYAy9bXUZ9Hf3VcBkdghfbuRScCcxRHkh1']]

    edges = getedges(nodes)
    G.add_edges_from([(i.nodefrom.address, i.nodeto.address) for i in edges])

    # create a png file
    G.layout(prog='dot')  # use dot
    G.draw('./configs/file.svg')
