# coding=utf-8
from config import config
from model import Label

count: set[any] = set()  # 计数变量


def spidermain():
    Get = __import__('spider.' + config['db'].dbname + '.get').Get
    for i in config['nodes']:
        if i not in count:
            count.add(i)
    nodes = config['nodes']

    for turn in range(config['TURN']):
        nodes = Get.get_next_nodes(nodes)
    Get.get_info()
