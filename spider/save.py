# coding=utf-8
from model import Balance, Label, Transfer


def save_balance(address, balance):
    balance = Balance(address, balance)
    balance.save()


def save_label(address, tag):
    label = Label(address, tag)
    label.save()


def save_transfer(transferhash, addrfrom, addrto, symbol, value, blocktime):
    transfer = Transfer(transferhash, addrfrom, addrto, symbol, value, blocktime)
    transfer.save()
