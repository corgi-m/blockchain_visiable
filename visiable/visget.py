# coding=utf-8

from model import Transfer, Balance, Label
from visiable.vismodel import Edge, Node
from visiable.viscut import Postcut, Precut, count, Nodecut

from config import config
from utils import Date, Utils

nodesappear: dict[str, list[set[Node]]] = {'from': [], 'to': []}


class Format:

    @staticmethod
    def nodeformat(address, size, color, tips):
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

    @staticmethod
    def edgeformat(addrfrom, addrto, color, tips):
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


class Get:
    @staticmethod
    def get_nodes_set():
        ori = set(config.visnodes)
        addresses = ori.copy()
        for _ in range(config.TURN):
            print(addresses)
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

    @staticmethod
    def get_next_nodes(node, edges_get, from_or_to) -> set[Node]:
        next_nodes = set()

        for edge in node.edges_generate(from_or_to):

            precut = Precut(edge, from_or_to)
            if precut.cut():
                continue

            edges_get.append(edge)
            if from_or_to == 'to':
                edge.nodeto.to_relation = node.to_relation
            else:
                edge.nodefrom.from_relation = node.from_relation

            postcut = Postcut(edge, from_or_to)
            if postcut.cut():
                continue

            remote = edge.nodeto if from_or_to == 'to' else edge.nodefrom
            next_nodes.add(remote)
            count[from_or_to].add(remote)

        return next_nodes

    @staticmethod
    def get_edges(nodes_ori, from_or_to) -> list[Edge]:
        nodes = nodes_ori.copy()
        for node in nodes:
            node.to_relation = {node}
            node.from_relation = {node}
            count[from_or_to].add(node)

        edges_get: list[Edge] = []
        nodesappear[from_or_to].append(nodes)
        node_exits = set()
        node_exits |= nodes
        # while len(nodes) != 0:
        for _ in range(config.TURN):
            next_nodes = set()

            for node in nodes:
                nodecut = Nodecut(node, from_or_to)
                if nodecut.cut():
                    continue
                next_nodes |= Get.get_next_nodes(node, edges_get, from_or_to)

            nodes = next_nodes - node_exits
            node_exits |= nodes
            nodesappear[from_or_to].append(nodes)
        return edges_get


class Nodeinfo:
    def __init__(self, node, from_or_to):
        self.node = node
        self.hlen = node.to_hlen if from_or_to == 'to' else node.from_hlen
        self.relation = node.to_relation if from_or_to == 'to' else node.from_relation
        self.color = None

    @staticmethod
    def balanceformat(balance):
        res = ""
        form = "{{{0}: {1}}}<br>"
        for balan in balance.items():
            res += form.format(balan[0], balan[1])
        return res

    @staticmethod
    def relationformat(relation):
        res = str(len(relation)) + '<br>'
        res += "from:<br>"
        for relat in relation:
            res += relat.address + '<br>'
        return res

    def get_node_color(self):
        if self.node.address in config.black:
            self.color = 'yellow'
        elif self.node.address in config.gray:
            self.color = 'green'
        elif self.node.address in config.visnodes:
            self.color = 'red'
        elif self.node.label is not None:
            self.color = 'blue'
        elif self.hlen > config.MAX_OUT_DEGREE:
            self.color = 'deeppink'
        else:
            self.color = 'black'
        return self.color

    def get_node_tips(self):
        tips = self.node.address + '<br>'
        tips += self.relationformat(self.relation) + self.balanceformat(self.node.balance)
        if self.color == 'blue':
            tips = self.node.label + '<br>' + tips
        tips = Utils.tip_filter(tips)
        return tips


class Edgeinfo:
    def __init__(self, edge):
        self.edge = edge

    def get_edge_tips(self):
        tips = "{0} -> {1}<br>".format(self.edge.nodefrom.address, self.edge.nodeto.address)
        form = "{{{1}, {2}: {3}, transferhash: {0}}}<br>"
        for info in sorted(self.edge.info):
            info = Utils.outof_list(info[1])
            tips += form.format(info[0], info[1], Utils.tip_filter(info[2]), info[3])
        return tips

    def get_edge_color(self):
        fillcolor = 'black'
        tokendict = {}
        tokens = ['USDT', 'DLW', 'POSCHE', 'TRX']
        for i in self.edge.info:
            info = i[1]
            if info[2] in tokendict:
                tokendict[info[2]] += info[3]
            else:
                tokendict[info[2]] = info[3]
            if Date.date_transform_reverse(info[1]) > config.TIME_STAMP:
                return 'blue'
        for k, v in tokendict.items():
            if k in tokens and v > config.THRESHOLD_OF_VALUE:
                fillcolor = 'red'
                break
        else:
            if len(self.edge.info) > config.THRESHOLD_OF_COUNT:
                fillcolor = 'yellow'
        return fillcolor
