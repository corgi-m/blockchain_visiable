# coding=utf-8

from config import config
from net import Net
from spider.oklink.get import OKlink, OKGet


class ETH(OKlink):
    __linkname = 'ETH'

    @staticmethod
    def get_other(address) -> list[Net.AsyncRequest]:  # 代币列表
        params = {"limit": "100", 'tokenType': 'ERC20'}
        return Net.greq_get(config.ercholder.format(address), params)

    @staticmethod
    def get_main(address) -> list[Net.AsyncRequest]:  # 代币列表
        return Net.greq_get(config.ethholder.format(address))

    @staticmethod
    def get_total_transfer(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {"tokenType": 'ERC20'}
        return Net.greq_get(config.ethtransfer.format(address), params)

    @staticmethod
    def get_total_transaction(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {}
        return Net.greq_get(config.ethtransaction.format(address), params)

    @staticmethod
    def get_total_internal(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {}
        return Net.greq_get(config.ethinternaltransfer.format(address), params)

    @staticmethod
    def get_nodes_transfer(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
        params = {"offset": offset, "limit": limit, "tokenType": 'ERC20'}
        return Net.greq_get(config.ethtransfer.format(address), params)

    @staticmethod
    def get_nodes_transaction(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
        params = {"offset": offset, "limit": limit, "type": 2}
        return Net.greq_get(config.ethtransaction.format(address), params)

    @staticmethod
    def get_internal_transfer(address, offset, limit) -> list[Net.AsyncRequest]:
        params = {"offset": offset, "limit": limit}
        return Net.greq_get(config.ethinternaltransfer.format(address), params)

    @staticmethod
    def get_internal_main(offset, limit, tranHash) -> list[Net.AsyncRequest]:
        params = {"offset": offset, "limit": limit, "tranHash": tranHash}
        return Net.greq_get(config.ethinternal, params)

    @staticmethod
    def get_internal_other(offset, limit, tranHash) -> list[Net.AsyncRequest]:
        params = {"offset": offset, "limit": limit, "tranHash": tranHash}
        return Net.greq_get(config.ercinternal, params)


class Get(OKGet):
    def __init__(self):
        super().__init__(ETH)
