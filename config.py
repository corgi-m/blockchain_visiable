# coding=utf-8
import configparser
import argparse
import sys

from db import DB

count: set[any] = set()  # 计数变量
config: dict[str, any] = {}


def parse_config(path_config):
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = lambda x: x

    config_parser.read(path_config, encoding='utf-8')

    config['db'] = DB(host=config_parser['mysql']['host'], port=int(config_parser['mysql']['port']),
                      user=config_parser['mysql']['user'], passwd=config_parser['mysql']['passwd'], )
    config.update(config_parser['common'])
    for key, value in config.items():
        if isinstance(value, str) and value.isdigit():
            config[key] = int(value)
    config.update({k: config['host'] + v for k, v in list(config_parser['api'].items())})
    config['headers'] = {'x-apiKey': config['apiKey']}
    return config


def parse_proxy(proxy: str) -> dict[str, str]:
    if proxy is None:
        return {}
    return {"http": proxy, "https": proxy}


def parse_nodes(file) -> list[str]:
    nodes_res = [i[:-1] for i in file.readlines()]
    return nodes_res


def get_config(args: argparse.Namespace):
    parse_config(args.config)
    config["nodes"] = parse_nodes(args.nodes)
    config["save"] = args.save
    config["visnodes"] = parse_nodes(args.visnodes)
    config['proxies'] = parse_proxy(args.proxy)
    config['visit'] = args.visit
    config['db'].dbname = args.link
    config['db'].check_db(args.dbstruct)

    if "apiKey" not in config:
        config['apiKey'] = args.apiKey
    if "log" not in config:
        config['log'] = args.log
    if "TURN" not in config:
        config['TURN'] = args.deep
    if "MAXN_LEN_EDGES" not in config:
        config['MAXN_LEN_EDGES'] = args.edgelimit
    if "MIN_TRANSFER_VALUE" not in config:
        config['MIN_TRANSFER_VALUE'] = args.valuelimit


def init():
    parser = argparse.ArgumentParser(prog='blockchain_visiable', description='developed by corgi')
    parser.add_argument('-p', '--proxy', type=str)
    parser.add_argument('-v', '--visit', action='store_true')
    parser.add_argument('-k', '--apiKey', type=str, default="301cac89-b56c-45ab-82b4-33656d074f73")
    parser.add_argument('-n', '--nodes', type=argparse.FileType('r'), default='./configs/nodeslist.txt')
    parser.add_argument('-N', '--visnodes', type=argparse.FileType('r'), default='./configs/visnodes.txt')
    parser.add_argument('-s', '--save', default='./result')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 4.0')
    parser.add_argument('-c', '--config', nargs='?', type=str, default='./configs/config.ini')
    parser.add_argument('-l', '--log', nargs='?', type=argparse.FileType('a'), default='./configs/error.log')
    parser.add_argument('-m', '--dbstruct', type=argparse.FileType('r'), default='./configs/db.sql')
    parser.add_argument('-d', '--deep', type=int, default=3)
    parser.add_argument('-e', '--edgelimit', type=int)
    parser.add_argument('-u', '--valuelimit', type=int)
    parser.add_argument('-L', '--link', nargs='?', type=str, default='trx', choices=['trx'])

    args = parser.parse_args(sys.argv[1:])

    get_config(args)
