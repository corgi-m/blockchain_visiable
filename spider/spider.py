# coding=utf-8

from config import config

count: dict[str, set[any]] = {'from': set(), 'to': set()}  # 计数变量


# 爬虫main函数
def spidermain() -> None:
    Get = __import__('spider.' + config.db.dbname + '.get', fromlist=['Get']).Get()
    global count
    nodes = {"from": config.nodes, "to": config.nodes}
    for from_or_to in config.from_or_to:
        count[from_or_to] |= config.nodes
    for turn in range(config.TURN):
        for from_or_to in config.from_or_to:
            nodes[from_or_to] = Get.get_next_nodes(nodes[from_or_to], from_or_to)
    Get.get_info()
    return
