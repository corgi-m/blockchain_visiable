# coding=utf-8

from visiable.visecharts import Echarts
from visiable.visget import Get, nodesappear


def vismain():
    print("start get nodes set")
    ori = Get.get_nodes_set()

    print("start get edges")
    edges = {
        'from': Get.get_edges(ori, 'from'),
        'to': Get.get_edges(ori, 'to')
    }

    print("start draw")
    graph_to = Echarts(nodesappear['to'], edges['to'], 'to')
    graph_from = Echarts(nodesappear['from'], edges['from'], 'from')
    graph_to.drawecharts()
    graph_from.drawecharts()
    print("end")
