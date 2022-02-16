# coding=utf-8
import re


def outof_list(li) -> str:
    return li[0] if isinstance(li, list) else li


def balanceformat(balance):
    res = ""
    form = "{{symbol: {0}, value: {1}}}<br>"
    for balan in balance.items():
        res += form.format(balan[0], balan[1])
    return res


def relationformat(relation):
    res = str(len(relation)) + '<br>'
    res += "from:<br>"
    for relat in relation:
        res += relat.address + '<br>'
    return res


def tip_filter(tips):
    tips = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", tips)
    tips = re.sub('[^\x00-\x7F]', '', tips)
    return tips
