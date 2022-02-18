from pyecharts.charts.basic_charts.graph import Graph
from pyecharts.options.global_options import TitleOpts, InitOpts, AnimationOpts
from pyecharts.options.series_options import LineStyleOpts

from visiable.visget import get_node_tips, get_node_color, get_edge_color, get_edge_tips


def setnodes(nodes, from_or_to):
    enodes = []
    i = 0
    for layer in nodes:
        for node in layer:
            nodecolor = get_node_color(node, from_or_to)
            tips = get_node_tips(node, from_or_to, nodecolor)
            enodes.append({
                "name": node.address,
                "symbolSize": (5 - i) * 10,
                "itemStyle": {
                    'color': nodecolor
                },
                "label": {
                    "fontSize": 10
                },
                "enterable": True,
                "tooltip": {
                    "textStyle": {
                        "align": 'center',
                        "fontSize": 15
                    },
                    "formatter": tips
                }
            })
        i += 1
    return enodes


def setedges(edges):
    eedges = []
    for edge in edges:
        color = get_edge_color(edge)
        tips = get_edge_tips(edge)
        eedges.append({
            "source": edge.nodefrom.address,
            "target": edge.nodeto.address,
            "symbol": [None, "arrow"],
            "lineStyle": {
                'color': color,
                'width': 2,
            },
            "enterable": True,
            "label": {
                "fontSize": 15
            },
            "tooltip": {
                "textStyle": {
                    "align": 'center',
                    "fontSize": 15
                },
                "formatter": tips
            }
        })
    return eedges


def drawecharts(nodes, edges, from_or_to):
    G = Graph(
        init_opts=InitOpts(
            animation_opts=AnimationOpts(
                animation=False,
            ),
            renderer='svg',
            width='8000px',
            height='4000px'
        ),
    )
    G.add(
        "",
        nodes,
        edges,
        repulsion=80,
        layout='force',
        edge_symbol=[''],
        linestyle_opts=LineStyleOpts(
            curve=0.1
        ),
    )
    G.set_global_opts(
        title_opts=TitleOpts(
            title="Graph-" + from_or_to
        ),
    )
    G.render("./result/graph_" + from_or_to + ".html")
