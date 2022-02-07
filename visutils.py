from utils import outof_list


def infoformat(info):
    res = ""
    form = "{{transferhash: {0}, blocktime: {1}, symbol: {2}, value: {3}}}\n"
    for i in info:
        i = outof_list(i)
        res += form.format(i[0], i[1], i[2], i[3])
    return res


def balanceformat(balance):
    res = ""
    form = "{{token: {0}, value: {1}}}\n"
    for i in balance.items():
        res += form.format(i[0], i[1])
    return res


def relationformat(relation):
    res = str(len(relation)) + '\n'
    res += "from:\n"
    for i in relation:
        res += i.address + '\n'
    return res
