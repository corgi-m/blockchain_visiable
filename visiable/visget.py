# coding=utf-8
from config import config
from model import Transfer
from utils import Date, Utils
from visiable.viscut import Postcut, count, Nodecut
from visiable.vismodel import Edge, Node


class Get:

    # 爬取指定层数 获取所有边的集合
    @classmethod
    def get_nodes_edges(cls, from_or_to) -> tuple[list[list[Node]], list[Edge]]:
        layers = []
        edges = []

        info = lambda x: (x[0], str(x[5]), x[3], x[4])
        direction = lambda x: (x[1], x[2], info(x))

        next_node = config.visnodes
        layers.append(cls.create_node(next_node))

        count[from_or_to] |= set(next_node)

        for _ in range(config.TURN):
            transfers = Transfer.get_transfer(next_node, from_or_to)
            transfer = [direction(transfer) for transfer in transfers]
            this_nodes, this_edges = cls.create_edge(transfer, from_or_to)
            next_node = {node for node in this_nodes if not Nodecut(node, from_or_to).cut()}

            layers.append(cls.create_node(next_node))
            edges.extend(this_edges)
        return layers, edges

    @staticmethod
    def create_node(all_node):
        return [Node(node) for node in all_node]

    @staticmethod
    def create_edge(all_edge, from_or_to):
        pairs: dict[str, dict[str, Edge]] = dict()
        edges = []
        nodes = []

        for edge in all_edge:
            last, this = (edge[0], edge[1]) if from_or_to == 'to' else (edge[1], edge[0])
            if last not in pairs:
                pairs[last] = dict()
            if this not in pairs[last]:
                pairs[last].update({this: Edge(edge[0], edge[1])})
            pairs[last][this].add_info(edge[2])

        for address, pair in pairs.items():
            postcut = Postcut(len(pair), address, Node.get_label(address))
            if postcut.cut():
                continue

            edges.extend(pair.values())
            nodes.extend(pair.keys())

        return nodes, edges


class Nodeinfo:
    __categories = {}

    def __init__(self, node):
        self.node = node
        self.hlen = node.hlen
        self.color = None

    # tips中balance格式化
    @staticmethod
    def balanceformat(balance) -> str:
        res = ""
        form = "{{{0}: {1}}}"
        for i, balan in enumerate(balance.items()):
            res += form.format(balan[0], balan[1])
            if (i + 1) % 5 == 0:
                res += "<br>"
        return res

    # tips中internal格式化
    @staticmethod
    def internalformat(internal) -> str:
        res = ""
        form = "{{transferhash: {0} time: {1}  {2} {3} -> {4} {5}}}<br>"
        for i, inter in enumerate(internal):
            res += form.format(inter[1], inter[2], inter[3], inter[4], inter[5], inter[6])
        return res

    # 获取categories字典
    @classmethod
    def get_categories(cls):
        return cls.__categories

    def get_label(self):
        return self.node.label

    # 获取节点颜色
    def get_node_category(self) -> int:
        if self.node.address in config.black:
            color = 'yellow'
            name = '黑名单'
        elif self.node.address in config.gray:
            color = 'green'
            name = '特殊标注'
        elif self.node.address in config.visnodes:
            color = 'red'
            name = '起始节点'
        elif self.node.label:
            color = 'blue'
            name = '交易所'
        elif self.hlen > config.MAX_OUT_DEGREE:
            color = 'deeppink'
            name = '大量交易节点'
        else:
            color = 'black'
            name = '普通节点'
        if color not in self.__categories:
            index = len(self.__categories)
            self.__categories[color] = (index, name, color)
        self.color = color
        return self.__categories[color][0]

    # 获取节点tips
    def get_node_tips(self) -> str:
        tips = self.node.address + '<br>'
        tips += self.balanceformat(self.node.balance)
        # self.internalformat(sorted(self.node.internal))
        if self.color == 'blue':
            tips = self.node.label + '<br>' + tips
        tips = Utils.tip_filter(tips)
        return tips


class Edgeinfo:
    def __init__(self, edge):
        self.edge = edge

    # 获取边颜色
    def get_edge_color(self) -> str:
        fillcolor = 'black'
        tokendict = {}
        tokens = ['USDT', 'DLW', 'POSCHE', 'TRX']
        for i in self.edge.info:
            info = i[1]
            if info[2] in tokendict:
                tokendict[info[2]] += info[3]
            else:
                tokendict[info[2]] = info[3]
            if config.MAX_TIME_STAMP > Date.date_transform_reverse(info[1]) > config.MIN_TIME_STAMP:
                return 'blue'
        for k, v in tokendict.items():
            if k in tokens and v > config.THRESHOLD_OF_VALUE:
                fillcolor = 'red'
                break
        else:
            if len(self.edge.info) > config.THRESHOLD_OF_COUNT:
                fillcolor = 'yellow'
        return fillcolor

    # 获取边tips
    def get_edge_tips(self) -> str:
        tips = "{0} -> {1}<br>".format(self.edge.nodefrom, self.edge.nodeto)
        form = "{{{1}, {2}: {3}, transferhash: {0}}}<br>"
        for info in sorted(self.edge.info):
            info = Utils.outof_list(info[1])
            tips += form.format(info[0], info[1], Utils.tip_filter(info[2]), info[3])
        return tips
