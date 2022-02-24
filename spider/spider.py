# coding=utf-8

from config import config

count: set[any] = set()  # 计数变量


# 爬虫main函数
def spidermain() -> None:
    Get = __import__('spider.' + config.db.dbname + '.get', fromlist=['Get']).Get()
    global count
    nodes = set(config.nodes)
    count |= nodes.copy()
    for turn in range(config.TURN):
        print(nodes)
        nodes = Get.get_next_nodes(nodes)
    Get.get_info()
    return
