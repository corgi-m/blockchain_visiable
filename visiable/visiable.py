# coding=utf-8
import time

from visiable.visecharts import setnodes, setedges, drawecharts
from visiable.visget import get_edges
from visiable.vismodel import Node, nodesappear

from config import config, init
from model import Transfer, Label, Balance


def get_nodes_set():
    ori = set(config["visnodes"])
    addresses = ori.copy()
    for _ in range(config['TURN']):
        res = Transfer.get_address(addresses)
        for i in res:
            address = i[0]
            if not Label.get(address) and Balance.get(address):
                addresses.add(address)
        print(len(addresses))
    nodes = {}
    edges = Transfer.get_transfer(list(addresses))
    print(len(edges))
    for i in edges:
        edge = dict(zip(Transfer.column, i))
        if edge['addrfrom'] not in nodes:
            nodes[edge['addrfrom']] = Node(address=edge['addrfrom'], )
        if edge['addrto'] not in nodes:
            nodes[edge['addrto']] = Node(address=edge['addrto'], )
        info = (edge['transferhash'], str(edge["blocktime"]), edge["symbol"], edge["value"])
        nodes[edge['addrfrom']].add_edge(nodes[edge['addrto']], info)

    return {v for k, v in nodes.items() if k in ori}


def vismain():
    print("start get nodes set")

    start = time.time()
    ori = get_nodes_set()
    end = time.time()

    print(end - start)
    print("start get edges")
    edges = {
        'from': get_edges(ori, 'from'),
        'to': get_edges(ori, 'to')
    }
    print("start draw")
    nodes_to = setnodes(nodesappear['to'], 'to')
    nodes_from = setnodes(nodesappear['from'], 'from')
    edges_to = setedges(edges['to'])
    edges_from = setedges(edges['from'])
    drawecharts(nodes_to, edges_to, 'to')
    drawecharts(nodes_from, edges_from, 'from')
    print("end")


if __name__ == "__main__":
    init()
