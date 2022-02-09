# coding=utf-8
from visiable.vismodel import Edge, Node
from config import config
from utils import use

count = {'from': set(), 'to': set()}


def pre_cut(edge: Edge):
    use(edge)
    return False


def post_cut(edge: Edge, node: Node, from_or_to):
    use(edge)
    if node.to_hlen + node.from_hlen > 2 * config['MAX_OUT_DEGREE']:
        return True
    if node in count[from_or_to]:
        return True
    return False
