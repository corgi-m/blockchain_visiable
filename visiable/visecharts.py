# coding=utf-8

from pyecharts.options.global_options import InitOpts, AnimationOpts
from pyecharts.options.series_options import LineStyleOpts
from pyecharts.charts.basic_charts.graph import Graph

from visiable.visget import Nodeinfo, Edgeinfo
from visiable.vismodel import Node, Edge


# 作图节点、边 格式类
class Format:
    # 节点格式
    @staticmethod
    def nodeformat(address, size, color, tips) -> dict[str, any]:
        return {
            "name": address,
            "symbolSize": (5 - size) * 10,
            "itemStyle": {
                'color': color
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
        }

    # 边格式
    @staticmethod
    def edgeformat(addrfrom, addrto, color, tips) -> dict[str, any]:
        return {
            "source": addrfrom,
            "target": addrto,
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
        }


# 作图类
class Echarts:
    def __init__(self, nodes, edges, from_or_to):
        self.nodes = self.setnodes(nodes, from_or_to)
        self.edges = self.setedges(edges)
        self.from_or_to = from_or_to

    # 设置节点列表
    @staticmethod
    def setnodes(nodes: list[list[Node]], from_or_to: str) -> list[dict[str, any]]:
        enodes = []
        for i, layer in enumerate(nodes):
            for node in layer:
                nodeinfo = Nodeinfo(node, from_or_to)
                enodes.append(Format.nodeformat(node.address, i, nodeinfo.get_node_color(), nodeinfo.get_node_tips()))
        return enodes

    # 设置边列表
    @staticmethod
    def setedges(edges: list[Edge]) -> list[dict[str, any]]:
        eedges = []
        for edge in edges:
            edgeinfo = Edgeinfo(edge)
            eedges.append(Format.edgeformat(edge.nodefrom.address, edge.nodeto.address, edgeinfo.get_edge_color(),
                                            edgeinfo.get_edge_tips()))
        return eedges

    # 作图
    def drawecharts(self) -> None:
        animation_opts = AnimationOpts(animation=False)
        linestyle_opts = LineStyleOpts(curve=0.1)
        init_opts = InitOpts(animation_opts=animation_opts, renderer='svg', width='8000px', height='4000px')
        G = Graph(init_opts=init_opts)
        G.add("", nodes=self.nodes, links=self.edges, repulsion=80, layout='force', edge_symbol=[''],
              linestyle_opts=linestyle_opts)
        G.render("./result/graph_" + self.from_or_to + ".html")
        return
