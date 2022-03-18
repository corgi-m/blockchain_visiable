# coding=utf-8

from model import Balance, Label, Transfer, Internal


# 保存数据库类
class Save:
    def __init__(self):
        ...

    # 保存balance
    @staticmethod
    def save_balance(address, balance) -> None:
        balance = Balance(address, balance)
        balance.save()
        return

    # 保存label
    @staticmethod
    def save_label(address, tag) -> None:
        label = Label(address, tag)
        label.save()
        return

    # 保存transfer
    @staticmethod
    def save_transfer(transferhash, addrfrom, addrto, symbol, value, blocktime) -> None:
        transfer = Transfer(transferhash, addrfrom, addrto, symbol, value, blocktime)
        transfer.save()
        return

    @classmethod
    def save_internal(cls, transferhash, address, fromtoken, fromvalue, totoken, tovalue, blocktime) -> None:
        internal = Internal(transferhash, address, fromtoken, fromvalue, totoken, tovalue, blocktime)
        internal.save()
        return
