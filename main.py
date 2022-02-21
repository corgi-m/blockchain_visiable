# coding=utf-8
from visiable.visiable import vismain

from spider.spider import spidermain

from config import config, init


if __name__ == "__main__":
    init()
    if not config['visit']:
        spidermain()
    else:
        vismain()
