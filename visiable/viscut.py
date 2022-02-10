# coding=utf-8
from visiable.vismodel import Edge, Node
from config import config
from utils import use, date_transform_reverse

count = {'from': set(), 'to': set()}


def node_cut(node: Node, from_or_to: str):
    hlen = node.to_hlen if from_or_to == 'to' else node.from_hlen
    if node.address in config['white']:
        return False
    if nodes_cut(node):
        return True
    if hlen > config['MAX_OUT_DEGREE']:
        return True
    if node.label is not None:
        return True
    return False


def date_cut(edge: Edge):
    for i in edge.info:
        if date_transform_reverse(i[1]) > config['TIME_STAMP']:
            break
    else:
        return True
    return False


def nodes_cut(node: Node):
    if node.address in config['black']:
        return True
    return False


def pre_cut(edge: Edge, node: Node):
    use(edge)
    '''if date_cut(edge):
        return True'''

    return False


def post_cut(edge: Edge, node: Node, from_or_to):
    use(edge)
    if node in count[from_or_to]:
        return True
    return False
