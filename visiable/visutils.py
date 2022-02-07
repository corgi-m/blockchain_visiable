from utils import outof_list


def infoformat(infos):
    res = ""
    form = "{{transferhash: {0}, blocktime: {1}, symbol: {2}, value: {3}}}\n"
    for info in infos:
        info = outof_list(info)
        res += form.format(info[0], info[1], info[2], info[3])
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
