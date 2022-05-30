# coding=utf-8

from config import config
from net import Net
from spider.oklink.get import OKlink, OKGet


class BNB(OKlink):
    __linkname = 'BNB'

    @staticmethod
    def get_other(address) -> list[Net.AsyncRequest]:  # 代币列表
        params = {"limit": "100", 'tokenType': 'BEP20'}
        return Net.greq_get(config.bepholder.format(address), params)

    @staticmethod
    def get_main(address) -> list[Net.AsyncRequest]:  # 代币列表
        return Net.greq_get(config.bnbholder.format(address))

    @staticmethod
    def get_total_transfer(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {"tokenType": 'BEP20'}
        return Net.greq_get(config.bnbtransfer.format(address), params)

    @staticmethod
    def get_total_transaction(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {"type": 2}
        return Net.greq_get(config.bnbtransaction.format(address), params)

    @staticmethod
    def get_nodes_transfer(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
        params = {"offset": offset, "limit": limit, "tokenType": 'BEP20'}
        return Net.greq_get(config.bnbtransfer.format(address), params)

    @staticmethod
    def get_nodes_transaction(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
        params = {"offset": offset, "limit": limit, "type": 2}
        return Net.greq_get(config.bnbtransaction.format(address), params)


class Get(OKGet):
    def __init__(self):
        super().__init__(BNB)
