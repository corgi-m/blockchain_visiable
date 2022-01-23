# coding=utf-8
from cuts import nodecut_reg, is_count
from utils import get_total_transaction, get_total_transfer, get_nodes_transfer, get_nodes_transaction, save_data
from config import config, init
from model import Label


def get_next_nodes(node):
    # get length
    len_edges_transfer = get_total_transfer(node)
    len_edges_transaction = get_total_transaction(node)
    next_nodes = set()

    # cut node
    if nodecut_reg(node, len_edges_transfer + len_edges_transaction):
        return next_nodes

    # transfers
    for page in range(0, len_edges_transfer, 100):
        next_nodes = next_nodes.union(get_nodes_transfer(node, page, 100))
    # transactions
    for page in range(0, len_edges_transaction, 100):
        next_nodes = next_nodes.union(get_nodes_transaction(node, page, 100))
    return next_nodes


def jungle(nodes):
    for turn in range(config['TURN']):
        next_nodes = set()
        for node in nodes:
            next_nodes = next_nodes.union(get_next_nodes(node))
        print(turn, len(next_nodes))
        nodes = next_nodes


def main():
    config['account'] = Label.get()
    for i in config['nodes']:
        is_count(i)
    jungle(config['nodes'])
    save_data()


if __name__ == "__main__":
    init()
    main()
