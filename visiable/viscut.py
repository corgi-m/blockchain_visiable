# coding=utf-8
from visiable.vismodel import Edge, Node
from config import config
from utils import use, date_transform_reverse

count = {'from': set(), 'to': set()}


def node_cut(node: Node, from_or_to: str):
    hlen = node.to_hlen if from_or_to == 'to' else node.from_hlen
    if hlen > config['MAX_OUT_DEGREE']:
        return True
    if node.label is not None:
        return True
    return False


def data_cut(edge: Edge):
    for i in edge.info:
        if date_transform_reverse(i[1]) > config['TIME_STAMP']:
            break
    else:
        return True
    return False


def pre_cut(edge: Edge):
    use(edge)
    if data_cut(edge):
        return True
    return False


def post_cut(edge: Edge, node: Node, from_or_to):
    use(edge)
    hlen = node.to_hlen if from_or_to == 'to' else node.from_hlen
    if hlen > config['MAX_OUT_DEGREE']:
        return True
    if node in count[from_or_to]:
        return True
    return False
