# coding=utf-8
import configparser
import argparse
import pymysql
import sys

count = {}  # 计数变量
config: dict[str, any] = {}


def parse_config(path_config):
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = lambda x: x

    config_parser.read(path_config, encoding='utf-8')
    config['conn'] = pymysql.connect(host=config_parser['mysql']['host'], port=int(config_parser['mysql']['port']),
                                     user=config_parser['mysql']['user'], passwd=config_parser['mysql']['passwd'],
                                     db=config_parser['mysql']['db'])
    config.update(config_parser['common'])
    if 'TURN' in config:
        config['TURN'] = int(config['TURN'])
    if 'MAXN_LEN_EDGES' in config:
        config['MAXN_LEN_EDGES'] = int(config['MAXN_LEN_EDGES'])
    if 'MIN_TRANSFER_VALUE' in config:
        config['MIN_TRANSFER_VALUE'] = int(config['MIN_TRANSFER_VALUE'])

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
    config['proxies'] = parse_proxy(args.proxy)
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
    parser.add_argument('-k', '--apiKey', type=str, default="301cac89-b56c-45ab-82b4-33656d074f73")
    parser.add_argument('-n', '--nodes', type=argparse.FileType('r'), default='./configs/nodeslist.txt')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 3.0')
    parser.add_argument('-c', '--config', nargs='?', type=str, default='./configs/config.ini')
    parser.add_argument('-l', '--log', nargs='?', type=argparse.FileType('w'), default='./configs/error.log')
    parser.add_argument('-d', '--deep', type=int, default=3)
    parser.add_argument('-e', '--edgelimit', type=int, default=200)
    parser.add_argument('-u', '--valuelimit', type=int, default=10)

    args = parser.parse_args(sys.argv[1:])

    get_config(args)
