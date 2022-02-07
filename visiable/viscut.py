from vismodel import Edge, Node
from config import config, count
from utils import use

use(Node)


def pre_cut(edge: Edge):
    use(edge)
    return False


def post_cut(edge: Edge):
    if edge.nodeto.hlen > config['MAX_OUT_DEGREE']:
        return True
    if edge.nodeto in count:
        return True
    return False
