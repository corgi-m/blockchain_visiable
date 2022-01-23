from vismodel import Edge, Node
from config import config, count
from utils import use


def pre_cut(edge: Edge):
    use(edge)
    return False


def post_cut(edge: Edge):
    if edge.getnodeto.gethlen > config['MAX_OUT_DEGREE']:
        return True
    if edge.getnodeto in count:
        return True
    return False
