# coding=utf-8
from config import config


class DB:
    _dbcolumn = None
    _dbsave = None
    _dbname = None
    _sqlget = "SELECT * FROM %s"

    def __init__(self, dbvalue):
        self._dbvalue = dbvalue

    @staticmethod
    def sqlformat(sql, arglist):
        sql = sql.replace('%s', '{}', len(arglist))
        sql = sql.format(*arglist)
        return sql

    def save(self):
        try:
            cur = config['conn'].cursor()
            sql = self.sqlformat(self.__class__._dbsave, [self.__class__._dbname] +
                                 self.__class__._dbcolumn)
            cur.execute(sql, self._dbvalue)
            config['conn'].commit()
            cur.close()
        except Exception as e:
            print("sql save error:")
            print(e)

    @classmethod
    def get_db(cls):
        try:
            cur = config['conn'].cursor()

            cur.execute(cls.sqlformat(cls._sqlget, [cls._dbname]))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print("Error: unable to fetch data")
            print(e)


class Label(DB):
    _dbname = "labels"
    _dbcolumn = ["address", "tag"]
    _dbsave = "REPLACE INTO %s (%s,%s)  VALUES(%s, %s)"

    def __init__(self, address, tag):
        super().__init__([address, tag])

    @classmethod
    def get(cls):
        account = {}
        results = cls.get_db()
        for i in results:
            account[i[0]] = i[1]
        return account


class Count(DB):
    _dbname = "counts"
    _dbcolumn = ["address", "count"]
    _dbsave = "REPLACE INTO %s (%s, %s) VALUES(%s, %s)"

    def __init__(self, address, count):
        super().__init__([address, count])


class Transfer(DB):
    _dbname = "transfers"
    _dbcolumn = ["transferhash", "addrfrom", "addrto", "symbol", "value", "blocktime"]
    _dbsave = "REPLACE INTO %s (%s, %s, %s, %s, %s, %s)  VALUES(%s, %s, %s, %s, %s, %s)"

    def __init__(self, transferhash, addrfrom, addrto, symbol, value, blocktime):
        super().__init__([transferhash, addrfrom, addrto, symbol, value, blocktime])

    @classmethod
    def get(cls):
        return cls.get_db()

    @classmethod
    def column(cls):
        return cls._dbcolumn


class Balance(DB):
    _dbname = "balances"
    _dbcolumn = ["address", "balance"]
    _dbsave = "REPLACE INTO %s (%s, %s) VALUES(%s, %s)"

    def __init__(self, address, balance):
        super().__init__([address, balance])


class Node:
    def __init__(self, address: str, balance: dict[str, float] = None, label: str = None):
        self.address = address
        self.balance = balance
        self.label = label
        self.head = None

    def edges_generate(self):
        head = self.head
        while head is not None:
            yield head
            head = head.lastedge

    def add_edge(self, transferhash, nodeto, transfer):
        for edge in self.edges_generate():
            if edge.nodeto == nodeto:
                edge.add_transfer(transfer)
                break
        else:
            edge = Edge(transferhash, self, nodeto, transfer, self.head)
            self.head = edge
        return edge


class Edge:
    def __init__(self, transferhash: str, nodefrom: Node, nodeto: Node, transfer: dict[str, float],
                 lastedge: 'Edge' = None):
        self.transferhash = transferhash
        self.nodefrom = nodefrom
        self.nodeto = nodeto
        self.transfer = transfer
        self.lastedge = lastedge

    def add_transfer(self, transfer):
        (key, value) = list(transfer.items())[0]
        if key in self.transfer.keys():
            self.transfer[key] += value
        else:
            self.transfer[key] = value
