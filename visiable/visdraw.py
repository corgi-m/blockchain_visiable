# coding=utf-8
from visiable.vismodel import Node
from visiable.visutils import relationformat, balanceformat, infoformat, tip_filter
import graphviz as gv
from config import config
import os


def graph_save(G, path) -> None:
    if not os.path.exists(config['save']):
        os.makedirs(config['save'])
    with open(config['save'] + '/' + path, 'w') as result:
        print(G.pipe().decode('gbk'), file=result)
    return


def graph_init() -> gv.graphs.Digraph:
    G_from = gv.Digraph(format='svg')
    G_from.graph_attr.update(ranksep='20', rankdir='LR', nodesep='0.5')
    G_to = gv.Digraph(format='svg')
    G_to.graph_attr.update(ranksep='20', rankdir='LR', nodesep='0.5')
    return G_from, G_to


def getcolor(node: Node, from_or_to):
    hlen = node.to_hlen if from_or_to == 'to' else node.from_hlen
    relationcount = node.to_relationcount if from_or_to == 'to' else node.from_relationcount
    if node.address in config['black']:
        fillcolor = 'yellow'
        fontcolor = 'black'
    elif node.address in config['gray']:
        fillcolor = 'green'
        fontcolor = 'white'
    elif node.address in config['visnodes']:
        fillcolor = 'red'
        fontcolor = 'black'
    elif node.label is not None:
        fillcolor = 'blue'
        fontcolor = 'white'
    elif hlen > config['MAX_OUT_DEGREE']:
        fillcolor = 'deeppink'
        fontcolor = 'white'
    else:
        fontcolor = 'black' if relationcount <= 5 else 'white'
        num = 100 - 10 * relationcount
        num = 0 if num < 0 else num
        fillcolor = 'grey' + str(num)
    return fillcolor, fontcolor


def draw_nodes(G, nodesappear, from_or_to) -> None:
    for i in range(len(nodesappear)):
        with G.subgraph(name='cluster_' + str(i)) as L:
            L.graph_attr.update(rank='same', color='green', label='layer_' + str(i), fontsize='100', compound='true')
            for node in nodesappear[i]:
                relation = node.to_relation if from_or_to == 'to' else node.from_relation
                tips = relationformat(relation) + balanceformat(node.balance)
                fillcolor, fontcolor = getcolor(node, from_or_to)
                if fillcolor == 'blue':
                    tips = node.label + '\n' + tips
                tips = tip_filter(tips)
                L.node(node.address, style='filled', fillcolor=fillcolor, fontcolor=fontcolor,
                       tooltip=tips, shape='box', layer=str(i))


def draw_edges(G, edges) -> None:
    for edge in edges:
        G.edge(edge.nodefrom.address, edge.nodeto.address,
               edgetooltip=infoformat(edge.nodefrom.address, edge.nodeto.address, edge.info), penwidth='4')
