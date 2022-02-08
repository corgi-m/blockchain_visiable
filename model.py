# coding=utf-8

from config import config


class Table:
    _tablename = None
    _column = None
    _sqlsave = None
    __sqlget = "SELECT * FROM %s"

    def __init__(self, value):
        self._value = value

    @staticmethod
    def sqlformat(sql, arglist) -> str:
        sql = sql.replace('%s', '{}', len(arglist))
        sql = sql.format(*arglist)
        return sql

    def save(self) -> None:
        try:
            cur = config['db'].cursor
            sql = self.sqlformat(self.__class__._sqlsave, [self.__class__._tablename] +
                                 self.__class__._column)
            cur.execute(sql, self._value)
            config['db'].commit()
            cur.close()
        except Exception as e:
            print("sql save error:")
            print(self.__class__._sqlsave, [self.__class__._tablename] +
                  self.__class__._column, self._value, file=config['log'])
            print(e)
        return

    @classmethod
    def get_db(cls) -> list[list[str]]:
        try:
            cur = config['db'].cursor
            cur.execute(cls.sqlformat(cls.__sqlget, [cls._tablename]))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print("Error: unable to fetch data")
            print(e)


class Label(Table):
    _tablename = "labels"
    _column = ["address", "tag"]
    _sqlsave = "REPLACE INTO %s (%s,%s)  VALUES(%s, %s)"

    def __init__(self, address, tag):
        super().__init__([address, tag])

    @classmethod
    def get(cls) -> dict[str, str]:
        account = {}
        results = cls.get_db()
        for i in results:
            account[i[0]] = i[1]
        return account


class Transfer(Table):
    _tablename = "transfers"
    _column = ["transferhash", "addrfrom", "addrto", "symbol", "value", "blocktime"]
    _sqlsave = "REPLACE INTO %s (%s, %s, %s, %s, %s, %s)  VALUES(%s, %s, %s, %s, %s, %s)"

    def __init__(self, transferhash, addrfrom, addrto, symbol, value, blocktime):
        super().__init__([transferhash, addrfrom, addrto, symbol, value, blocktime])

    @classmethod
    def get(cls) -> list[list[str]]:
        return cls.get_db()

    @classmethod
    def column(cls) -> list[str]:
        return cls._column


class Balance(Table):
    _tablename = "balances"
    _column = ["address", "balance"]
    _sqlsave = "REPLACE INTO %s (%s, %s) VALUES(%s, %s)"

    def __init__(self, address, balance):
        super().__init__([address, balance])

    @classmethod
    def get(cls) -> dict[str, str]:
        res = {}
        results = cls.get_db()
        for i in results:
            res[i[0]] = i[1]
        return res
