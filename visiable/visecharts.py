from pyecharts.charts.basic_charts.graph import Graph
from pyecharts.globals import RenderType
from pyecharts.options.charts_options import GraphNode
from pyecharts.options.global_options import TitleOpts, InitOpts
from pyecharts.options.series_options import ItemStyleOpts

from config import config
from visiable.vismodel import Node


def getcolor(node: Node, from_or_to):
    hlen = node.to_hlen if from_or_to == 'to' else node.from_hlen
    relationcount = node.to_relationcount if from_or_to == 'to' else node.from_relationcount
    if node.address in config['black']:
        fillcolor = 'pink'
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
        fillcolor = 'black'
        fontcolor = 'white'
    return fillcolor, fontcolor


def setnodes(nodes, from_or_to):
    enodes = []
    i = 0

    for layer in nodes:
        print(nodes)
        i += 1
        for node in layer:
            fillcolor, fontcolor = getcolor(node, from_or_to)
            print(fillcolor)
            enodes.append(
                # GraphNode(name=node.address, symbol_size=(5 - i) * 30, itemstyleopts=ItemStyleOpts(color=fillcolor))
                {"name": node.address, "symbolSize": (5 - i) * 30, "itemStyle": {'color': fillcolor}}
            )
    return enodes


def setedges(edges, from_or_to):
    eedges = []
    for edge in edges:
        eedges.append({"source": edge.nodefrom.address, "target": edge.nodeto.address, "lineStyle": {'color': fil}})
    return eedges


def drawecharts(nodes, edges):
    c = (
        Graph(init_opts=InitOpts(renderer='svg', width='8000px', height='4000px'))
            .add("", nodes, edges, repulsion=8000, layout='force', is_draggable=True)
            .set_global_opts(title_opts=TitleOpts(title="Graph-test"))
            .render("graph_base.html")
    )
