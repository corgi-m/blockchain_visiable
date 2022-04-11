# coding=utf-8

from pyecharts.charts.basic_charts.graph import Graph
from pyecharts.charts.basic_charts.tree import Tree
from pyecharts.options.global_options import InitOpts, AnimationOpts
from pyecharts.options.series_options import LineStyleOpts

from config import config
from visiable.visget import Nodeinfo, Edgeinfo
from visiable.vismodel import Node, Edge


# 作图节点、边 格式类
class Format:
    # 节点格式
    @staticmethod
    def nodeformat(address, size, color, tips, label) -> dict[str, any]:
        return {
            "name": address,
            "symbolSize": (5 - size) * 10,
            "label": {
                "fontSize": 10,
                "formatter": label if label else address
            },
            "category": color,
            "enterable": True,
            "tooltip": {
                "trigger": "item",
                "triggerOn": "click",
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

    # categories 格式
    @staticmethod
    def categoryformat(color, name):
        return {
            "itemStyle": {
                "color": color
            },
            "name": name
        }


# 作图类
class Echarts:
    JSCODE = \
        """
            var test = function(){
                chart_chart.on('click',function(params){
                    console.log(params.data.tooltip.formatter.replace(/<br>/g,'\\n'));
                });
            }
            test();
        """

    def __init__(self, nodes, edges, from_or_to):
        self.categories = []
        self.nodes = self.setnodes(nodes)
        self.edges = self.setedges(edges)
        self.categories = self.setcategories(Nodeinfo.get_categories())
        self.from_or_to = from_or_to

    # 设置节点列表
    @staticmethod
    def setnodes(nodes: list[list[Node]]) -> list[dict[str, any]]:
        enodes = []
        for i, layer in enumerate(nodes):
            for node in set(layer):
                nodeinfo = Nodeinfo(node)
                enodes.append(
                    Format.nodeformat(node.address, i, nodeinfo.get_node_category(), nodeinfo.get_node_tips(),
                                      nodeinfo.get_label()))
        return enodes

    # 设置边列表
    @staticmethod
    def setedges(edges: list[Edge]) -> list[dict[str, any]]:
        eedges = []
        for edge in edges:
            edgeinfo = Edgeinfo(edge)
            eedges.append(Format.edgeformat(edge.nodefrom, edge.nodeto, edgeinfo.get_edge_color(),
                                            edgeinfo.get_edge_tips()))
        return eedges

    # 设置categories
    @staticmethod
    def setcategories(categories: dict[str, int]) -> list[dict[str, any]]:
        ecategories = []
        for _, name, color in sorted(categories.values()):
            ecategories.append(Format.categoryformat(color, name))
        return ecategories

    # 作图
    def drawecharts(self) -> None:
        animation_opts = AnimationOpts(animation=False)
        linestyle_opts = LineStyleOpts(curve=0.1)
        init_opts = InitOpts(chart_id='chart', animation_opts=animation_opts, renderer='svg', width="100%",
                             height="1470%")
        G = Graph(init_opts=init_opts)
        G.add_js_funcs(self.JSCODE)
        print(len(self.nodes))
        G.add("", nodes=self.nodes, links=self.edges, categories=self.categories, repulsion=80, layout='force',
              edge_symbol=[''], linestyle_opts=linestyle_opts)
        G.render("./result/" + config.db.dbname + "/graph_" + self.from_or_to + ".html")
        return
