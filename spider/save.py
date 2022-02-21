# coding=utf-8
from model import Balance, Label, Transfer


class Save:
    def __init__(self):
        ...

    @staticmethod
    def save_balance(address, balance):
        balance = Balance(address, balance)
        balance.save()

    @staticmethod
    def save_label(address, tag):
        label = Label(address, tag)
        label.save()

    @staticmethod
    def save_transfer(transferhash, addrfrom, addrto, symbol, value, blocktime):
        transfer = Transfer(transferhash, addrfrom, addrto, symbol, value, blocktime)
        transfer.save()
