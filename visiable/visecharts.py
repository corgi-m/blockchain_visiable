from pyecharts.charts.basic_charts.graph import Graph
from pyecharts.options.charts_options import GraphNode
from pyecharts.options.global_options import TitleOpts, InitOpts
from config import config
from visiable.visget import get_node_tips, get_node_color, get_edge_color, get_edge_tips


def setnodes(nodes, from_or_to):
    enodes = []
    i = 0
    for layer in nodes:
        i += 1
        for node in layer:
            nodecolor = get_node_color(node, from_or_to)
            tips = get_node_tips(node, from_or_to, nodecolor)
            enodes.append(
                {"name": node.address, "symbolSize": (5 - i) * 30, "itemStyle": {'color': nodecolor},
                 "label": {"fontSize": 15},
                 "tooltip": {"textStyle": {"align": 'center', "fontSize": 20}, "formatter": tips}}
            )
    return enodes


def setedges(edges):
    eedges = []
    for edge in edges:
        color = get_edge_color(edge)
        tips = get_edge_tips(edge)
        eedges.append(
            {"source": edge.nodefrom.address, "target": edge.nodeto.address,
             "lineStyle": {'color': color, 'width': 3},
             "label": {"fontSize": 15},
             "tooltip": {"textStyle": {"align": 'center', "fontSize": 20}, "formatter": tips}})
    return eedges


def drawecharts(nodes, edges):
    c = (
        Graph(init_opts=InitOpts(renderer='svg', width='8000px', height='4000px'))
            .add("", nodes, edges, repulsion=8000, layout='force', edge_symbol=[''])
            .set_global_opts(title_opts=TitleOpts(title="Graph-test"))
            .render("graph_base.html")
    )
