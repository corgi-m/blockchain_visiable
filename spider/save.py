# coding=utf-8

from model import Balance, Label, Transfer


class Save:
    def __init__(self):
        ...

    @staticmethod
    def save_balance(address, balance) -> None:
        balance = Balance(address, balance)
        balance.save()
        return

    @staticmethod
    def save_label(address, tag) -> None:
        label = Label(address, tag)
        label.save()
        return

    @staticmethod
    def save_transfer(transferhash, addrfrom, addrto, symbol, value, blocktime) -> None:
        transfer = Transfer(transferhash, addrfrom, addrto, symbol, value, blocktime)
        transfer.save()
        return
