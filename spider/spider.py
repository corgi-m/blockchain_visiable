# coding=utf-8
from config import config
from model import Label

import importlib

count: set[any] = set()  # 计数变量


def spidermain():
    Get = importlib.import_module('spider.' + config['db'].dbname + '.get').Get
    config['account'] = Label.get()
    for i in config['nodes']:
        if i not in count:
            count.add(i)
    nodes = config['nodes']

    for turn in range(config['TURN']):
        nodes = Get.get_next_nodes(nodes)
    Get.get_info()
