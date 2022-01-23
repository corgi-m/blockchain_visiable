from config import config, init, count
import pygraphviz as pgv
from model import Transfer
from vismodel import Node, Edge
from viscut import pre_cut, post_cut

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


def get_next_nodes(node, edges_get):
    next_nodes = set()

    for edge in node.edges_generate():

        if pre_cut(edge):
            return next_nodes

        edges_get.append(edge)

        if post_cut(edge):
            return next_nodes

        next_nodes.add(edge.getnodeto)
        count.add(edge.getnodeto)
    return next_nodes


def getedges(nodes_get):
    edges_get: list[Edge] = []
    for _ in range(config['TURN']):
        next_nodes = set()
        for node in nodes_get:
            next_nodes = next_nodes.union(get_next_nodes(node, edges_get))
        '''        
            for edge in node.edges_generate():
                edges_get.append(edge)
                if edge.nodeto not in repeat_nodes:
                    nextnodes.append(edge.nodeto)
        '''
        nodes_get = next_nodes
    return edges_get


if __name__ == "__main__":
    init()
    vis_init()
    G = pgv.AGraph(directed=True)

    nodes = [nodesmap['TYAy9bXUZ9Hf3VcBkdghfbuRScCcxRHkh1']]

    edges = getedges(nodes)
    G.add_edges_from([(i.getnodefrom.getaddress, i.getnodeto.getaddress) for i in edges])

    # create a png file
    G.layout(prog='dot')  # use dot
    G.draw('./configs/file.svg')
