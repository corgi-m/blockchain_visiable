# coding=utf-8
from config import config, init
from spider import spidermain
from visiable import vismain

if __name__ == "__main__":
    init()
    if not config['visit']:
        spidermain()
    else:
        vismain()
