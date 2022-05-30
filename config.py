# coding=utf-8

import argparse
import configparser
import sys

from typing.io import TextIO

from db import DB
from utils import Date


# Config 单例，通过重写getattr、setattr等魔术方法实现动态添加属性
class Config:
    def __init__(self):
        ...

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        return None

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        return

    def __call__(self, *args, **kwargs):
        return self.__dict__

    def update(self, value: dict[str, any]):
        self.__dict__.update(value)
        return

    def __str__(self):
        return str(self.__dict__)

    # 解析config.ini文件
    @staticmethod
    def parse_config(path_config):
        cfg = Config()
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = lambda x: x

        config_parser.read(path_config, encoding='utf-8')

        cfg.db = DB(host=config_parser['mysql']['host'], port=int(config_parser['mysql']['port']),
                    user=config_parser['mysql']['user'], passwd=config_parser['mysql']['passwd'])
        cfg.update(
            {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in config_parser['common'].items()})
        cfg.update({k: cfg.host + v for k, v in config_parser['api'].items()})
        return cfg

    # 解析proxy代理格式
    @staticmethod
    def parse_proxy(proxy: str) -> dict[str, str]:
        if proxy is None:
            return {}
        return {"http": proxy, "https": proxy}

    # 解析节点列表文件
    @staticmethod
    def parse_nodes(file) -> list[str]:
        nodes_res = []
        for i in file.readlines():
            address = i.strip()
            if address != '':
                nodes_res.append(address)
        return nodes_res

    # 解析请求头
    @staticmethod
    def parser_header(file) -> dict[str, str]:
        header = {}
        for i in file.readlines():
            record = i.strip()
            if record == '' or ':' not in record:
                continue
            temp = record.split(': ')
            header[temp[0]] = temp[1]
        return header

    # 读取文件对象
    def parser_readfile(self, path) -> TextIO:
        return open('./configs/' + self.db.dbname + '/' + path, 'r')

    # 解析命令行参数
    @staticmethod
    def create_config(args: argparse.Namespace) -> 'Config':
        cfg = Config()
        cfg.update(Config.parse_config(args.config)())
        cfg.MIN_TIME_STAMP = Date.date_transform_reverse(cfg.MIN_TIME_STAMP)
        cfg.MAX_TIME_STAMP = Date.date_transform_reverse(cfg.MAX_TIME_STAMP)
        cfg.db.dbname = args.link
        cfg.from_or_to = args.direction
        cfg.symbol = args.symbol
        cfg.nodes = set(Config.parse_nodes(cfg.parser_readfile(args.nodes)))
        cfg.save = args.save
        cfg.visnodes = Config.parse_nodes(cfg.parser_readfile(args.visnodes))
        cfg.proxies = Config.parse_proxy(args.proxy)
        cfg.visit = args.visit
        cfg.db.check_db(args.dbstruct)
        cfg.headers = Config.parser_header(cfg.parser_readfile(args.headers))
        cfg.log = args.log
        cfg.TURN = args.deep
        cfg.white = Config.parse_nodes(cfg.parser_readfile(args.white))
        cfg.black = Config.parse_nodes(cfg.parser_readfile(args.black))
        cfg.gray = Config.parse_nodes(cfg.parser_readfile(args.gray))
        return cfg


# Config单例
config: Config = Config()


# 解析config.ini参数及命令行参数
def parser_init():
    parser = argparse.ArgumentParser(prog='blockchain_visiable', description='developed by corgi')
    parser.add_argument('-p', '--proxy', type=str)
    parser.add_argument('-v', '--visit', action='store_true')
    parser.add_argument('-H', '--headers', type=str, default="headers.txt")
    parser.add_argument('-n', '--nodes', type=str, default='nodeslist.txt')
    parser.add_argument('-w', '--white', type=str, default='white.txt')
    parser.add_argument('-b', '--black', type=str, default='black.txt')
    parser.add_argument('-g', '--gray', type=str, default='gray.txt')
    parser.add_argument('-N', '--visnodes', type=str, default='visnodes.txt')
    parser.add_argument('-s', '--save', default='./result')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 2.7')
    parser.add_argument('-c', '--config', nargs='?', type=str, default='./configs/config.ini')
    parser.add_argument('-l', '--log', nargs='?', type=argparse.FileType('a'), default='./configs/error.log')
    parser.add_argument('-m', '--dbstruct', type=argparse.FileType('r'), default='./configs/db.sql')
    parser.add_argument('-d', '--deep', type=int, default=3)
    parser.add_argument('-L', '--link', nargs='?', type=str, default='trx', choices=['trx', 'eth', 'bnb'])
    parser.add_argument('-D', '--direction', nargs='+', type=str, default=['from', 'to'], choices=['from', 'to'])
    parser.add_argument('-S', '--symbol', nargs='+', type=str, default=[])
    parser.add_argument('-I', '--internal', action='store_true')

    args = parser.parse_args(sys.argv[1:])
    global config
    config.update(Config.create_config(args)())
