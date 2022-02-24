# coding=utf-8

from visiable.visiable import vismain

from spider.spider import spidermain

from config import config, parser_init

# 程序入口点
if __name__ == "__main__":
    parser_init()
    if not config.visit:
        spidermain()
    else:
        vismain()
