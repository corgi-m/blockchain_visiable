# coding=utf-8

from spider.oklink.get import OKlink, OKGet

from config import config
from net import Net


class TRX(OKlink):
    __linkname = 'TRX'

    @staticmethod
    def get_other(address) -> list[Net.AsyncRequest]:  # 代币列表
        params = {"limit": "100"}
        return Net.greq_get(config.trcholder.format(address, 'TRC20'), params)

    @staticmethod
    def get_main(address) -> list[Net.AsyncRequest]:  # 代币列表
        return Net.greq_get(config.trxholder.format(address))

    @staticmethod
    def get_total_transfer(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {"tokenType": "TRC20", "contractAddress": address}
        return Net.greq_get(config.trxtransfer, params)

    @staticmethod
    def get_total_transaction(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {"address": address}
        return Net.greq_get(config.trxtransaction, params)

    @staticmethod
    def get_nodes_transfer(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
        params = {"offset": offset, "limit": limit, "tokenType": "TRC20",
                  "contractAddress": address}  # "sort": "blocktime,asc"
        return Net.greq_get(config.trxtransfer, params)

    @staticmethod
    def get_nodes_transaction(address, offset, limit) -> list[Net.AsyncRequest]:  # 下一级节点的集合。
        params = {"address": address, "offset": offset, "limit": limit}
        return Net.greq_get(config.trxtransaction, params)

    @staticmethod
    def get_total_internal(address) -> list[Net.AsyncRequest]:  # 下一级节点个数
        params = {'address': address}
        return Net.greq_get(config.trxinternaltransfer, params)

    @staticmethod
    def get_internal_transfer(address, offset, limit) -> list[Net.AsyncRequest]:
        params = {"offset": offset, "limit": limit, 'address': address}
        return Net.greq_get(config.trxinternaltransfer, params)

    @staticmethod
    def get_internal_main(offset, limit, tranHash) -> list[Net.AsyncRequest]:
        params = {"offset": offset, "limit": limit, "tranHash": tranHash}
        return Net.greq_get(config.trxinternal, params)

    @staticmethod
    def get_internal_other(offset, limit, tranHash) -> list[Net.AsyncRequest]:
        params = {"offset": offset, "limit": limit, "tranHash": tranHash, 'tokenType': 'TRC20'}
        return Net.greq_get(config.trcinternal, params)


class Get(OKGet):
    def __init__(self):
        super().__init__(TRX)
