# coding=utf-8

import time


def use(_):
    ...


def outof_list(li) -> str:
    return li[0] if isinstance(li, list) else li


def date_transform(timestamp) -> str:
    time_local = time.localtime(int(timestamp / 1000))
    datatime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return datatime

def date_transform2(timestamp) -> str:
    time_local = time.localtime(int(timestamp))
    datatime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return datatime
