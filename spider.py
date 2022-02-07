from trx.get import get_next_nodes
from save import save_data
from config import config, count
from model import Label


def jungle(nodes):
    for turn in range(config['TURN']):
        next_nodes = set()
        for node in nodes:
            next_nodes |= get_next_nodes(node)
        print(turn, len(next_nodes))
        nodes = next_nodes


def spidermain():
    config['account'] = Label.get()
    for i in config['nodes']:
        if i not in count:
            count.add(i)
    jungle(config['nodes'])
    save_data()
