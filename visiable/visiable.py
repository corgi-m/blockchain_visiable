# coding=utf-8
from config import config
from visiable.visecharts import Echarts
from visiable.visget import Get


# 可视化main函数
def vismain():
    for from_or_to in config.from_or_to:
        nodes, edges = Get.get_nodes_edges(from_or_to)
        graph = Echarts(nodes, edges, from_or_to)
        print("draw graph")
        graph.drawecharts()
    print("end")
