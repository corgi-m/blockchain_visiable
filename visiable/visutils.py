# coding=utf-8
import re


def outof_list(li) -> str:
    return li[0] if isinstance(li, list) else li


def infoformat(addrfrom, addrto, infos):
    res = ""
    form = "{{transferhash: {0},from: {1}, to: {2}, blocktime: {3}, symbol: {4}, value: {5}}}\n"
    for info in infos:
        info = outof_list(info)
        symbol = tip_filter(info[2])
        res += form.format(info[0], addrfrom, addrto, info[1], symbol, info[3])
    return res


def balanceformat(balance):
    res = ""
    form = "{{symbol: {0}, value: {1}}}\n"
    for balan in balance.items():
        res += form.format(balan[0], balan[1])
    return res


def relationformat(relation):
    res = str(len(relation)) + '\n'
    res += "from:\n"
    for relat in relation:
        res += relat.address + '\n'
    return res


def tip_filter(tips):
    tips = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", tips)
    tips = re.sub('[^\x00-\x7F]', '', tips)
    return tips
