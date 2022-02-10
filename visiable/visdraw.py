# coding=utf-8
from visiable.visutils import relationformat, balanceformat, infoformat
import graphviz as gv
from config import config
from utils import date_transform_reverse
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


def draw_nodes(G, nodesappear, from_or_to) -> None:
    for i in range(len(nodesappear)):
        with G.subgraph(name='cluster_' + str(i)) as L:
            L.graph_attr.update(rank='same', color='green', label='layer_' + str(i), fontsize='100', compound='true')
            for node in nodesappear[i]:
                relationcount = node.to_relationcount if from_or_to == 'to' else node.from_relationcount
                relation = node.to_relation if from_or_to == 'to' else node.from_relation
                fontcolor = 'black' if relationcount <= 5 else 'white'
                tips = relationformat(relation) + balanceformat(node.balance)
                if node.address in config['black']:
                    fillcolor = 'yellow'
                elif i == 0:
                    fillcolor = 'red'
                elif node.label is not None:
                    fillcolor = 'blue'
                    fontcolor = 'white'
                    tips = node.label + '\n' + tips
                else:
                    num = 100 - 10 * relationcount
                    if num < 0:
                        num = 0
                    fillcolor = 'grey' + str(num)
                if relationcount > 0:
                    L.node(node.address, style='filled', fillcolor=fillcolor, fontcolor=fontcolor,
                           tooltip=tips, shape='box', layer=str(i))


def draw_edges(G, edges) -> None:
    for edge in edges:
        '''for i in edge.info:
            if date_transform_reverse(i[1]) > 1642003200:
                break
        else:
            continue'''
        G.edge(edge.nodefrom.address, edge.nodeto.address,
               edgetooltip=infoformat(edge.nodefrom.address, edge.nodeto.address, edge.info), penwidth='4')
