from config import count
from trx.get import get_balance
from model import Balance


def save_balance(address):
    balances = get_balance(address)
    bals = []
    if balances is not None:
        for i in balances:
            bals.append(i["symbol"] + ',' + str(i["value"]))
        balance = Balance(address, ';'.join(bals))
        balance.save()


def save_data():
    for address in count:
        print(address)
        save_balance(address)
