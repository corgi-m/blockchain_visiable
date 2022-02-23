# coding=utf-8

from db import DB

import configparser
import argparse
import sys


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

    def update(self, value: dict[str, any]):
        self.__dict__.update(value)
        return

    def __str__(self):
        return str(self.__dict__)


config: Config = Config()


def parse_config(path_config):
    global config
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = lambda x: x

    config_parser.read(path_config, encoding='utf-8')

    config.db = DB(host=config_parser['mysql']['host'], port=int(config_parser['mysql']['port']),
                   user=config_parser['mysql']['user'], passwd=config_parser['mysql']['passwd'])
    config.update({k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in config_parser['common'].items()})
    config.update({k: config.host + v for k, v in config_parser['api'].items()})


def parse_proxy(proxy: str) -> dict[str, str]:
    if proxy is None:
        return {}
    return {"http": proxy, "https": proxy}


def parse_nodes(file) -> list[str]:
    nodes_res = []
    for i in file.readlines():
        address = i.strip()
        if address != '':
            nodes_res.append(address)
    return nodes_res


def parser_header(file):
    header = {}
    for i in file.readlines():
        record = i.strip()
        if record == '' or ':' not in record:
            continue
        temp = record.split(': ')
        header[temp[0]] = temp[1]
    return header


def parser_readfile(path):
    return open('./configs/' + config.db.dbname + '/' + path, 'r')


def init_config(args: argparse.Namespace):
    global config
    parse_config(args.config)
    config.db.dbname = args.link
    config.nodes = parse_nodes(parser_readfile(args.nodes))
    config.save = args.save
    config.visnodes = parse_nodes(parser_readfile(args.visnodes))
    config.proxies = parse_proxy(args.proxy)
    config.visit = args.visit
    config.db.check_db(args.dbstruct)
    config.headers = parser_header(parser_readfile(args.headers))
    config.log = args.log
    config.TURN = args.deep
    config.white = parse_nodes(parser_readfile(args.white))
    config.black = parse_nodes(parser_readfile(args.black))
    config.gray = parse_nodes(parser_readfile(args.gray))
    return config


def init():
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
    parser.add_argument('-e', '--edgelimit', type=int)
    parser.add_argument('-u', '--valuelimit', type=int)
    parser.add_argument('-L', '--link', nargs='?', type=str, default='trx', choices=['trx', 'eth'])

    args = parser.parse_args(sys.argv[1:])
    init_config(args)
