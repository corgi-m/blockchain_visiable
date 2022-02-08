# coding=utf-8
from visiable.vismodel import Edge, Node
from config import config, count
from utils import use


def pre_cut(edge: Edge):
    use(edge)
    return False


def post_cut(edge: Edge, node: Node):
    #if node.to_hlen + node.from_hlen > 2 * config['MAX_OUT_DEGREE']:
    #    return True
    if node in count:
        return True
    return False
