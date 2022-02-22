# coding=utf-8
from visiable.vismodel import Edge, Node, Info

from config import config
from utils import Utils, Date

count = {'from': set(), 'to': set()}


def node_cut(node: Node, from_or_to: str):
    if white_cut(node.address):
        return False
    if black_cut(node.address):
        return True
    if len_cut(node.to_hlen if from_or_to == 'to' else node.from_hlen):
        return True
    if label_cut(node.label):
        return True
    return False


def white_cut(address: str):
    if address in config['white']:
        return True
    return False


def date_cut(info: Info):
    for i in info:
        if Date.date_transform_reverse(i[1][1]) > config['TIME_STAMP']:
            return False
    return True


def label_cut(label: str or None):
    if label is not None:
        return True
    return False


def len_cut(length: int):
    if length > config['MAX_OUT_DEGREE']:
        return True
    return False


def black_cut(address: str):
    if address in config['black']:
        return True
    return False


def pre_cut(edge: Edge, node: Node):
    Utils.use(edge)
    Utils.use(node)
    '''if date_cut(edge.info):
        return True'''

    return False


def post_cut(edge: Edge, node: Node, from_or_to):
    Utils.use(edge)
    if node in count[from_or_to]:
        return True
    return False
