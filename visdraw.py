from visutils import *


def draw_nodes(G, nodesappear):
    for i in range(len(nodesappear)):
        with G.subgraph(name='cluster_' + str(i)) as L:
            L.graph_attr.update(rank='same', color='green', label='layer_' + str(i), fontsize='100')
            for node in nodesappear[i]:
                color = 'black' if node.relationcount <= 5 else 'white'
                fillcolor = 'grey{}0'.format(str(10 - node.relationcount)) if i != 0 else 'yellow'
                tips = relationformat(node.relation) + balanceformat(node.balance)
                L.node(node.address, style='filled', fillcolor=fillcolor, fontcolor=color,
                       tooltip=tips, shape='box')


def draw_edges(G, edges):
    for edge in edges:
        G.edge(edge.nodefrom.address, edge.nodeto.address, edgetooltip=infoformat(edge.info), penwidth='4')
