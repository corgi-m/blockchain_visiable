# coding=utf-8
from config import config


class classproperty:
    def __init__(self, method):
        self.method = method

    def __get__(self, instance, owner):
        return self.method(owner)


class Table:
    _tablename: str = None
    _column: list[str] = None
    _sqlsave = None
    __sqlget = "SELECT * FROM %s"
    __isexist = "SELECT EXISTS(SELECT * FROM %s WHERE %s=%s)"

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

    @staticmethod
    def query(sql, params):
        try:
            cur = config['db'].cursor
            cur.execute(sql, params)
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print("Error: unable to fetch data")
            print(e)

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

    @classmethod
    def is_exist(cls, value) -> bool:
        try:
            cur = config['db'].cursor
            cur.execute(cls.sqlformat(cls.__isexist, [cls._tablename, cls._column[0]]), value)
            results = cur.fetchone()
            cur.close()
            return True if results[0] == 1 else False
        except Exception as e:
            print("Error: unable to fetch data")
            print(e)


class Label(Table):
    _tablename = "labels"
    _column = ["address", "tag"]
    _sqlsave = "REPLACE INTO %s (%s,%s)  VALUES(%s, %s)"
    __sqlget = "SELECT tag FROM labels where address=%s"

    def __init__(self, address, tag):
        super().__init__([address, tag])

    @classmethod
    def get(cls, address) -> tuple[tuple]:
        sql = cls.__sqlget
        params = (address,)
        return super().query(sql, params)


class Transfer(Table):
    _tablename = "transfers"
    _column = ["transferhash", "addrfrom", "addrto", "symbol", "value", "blocktime"]
    _sqlsave = "REPLACE INTO %s (%s, %s, %s, %s, %s, %s)  VALUES(%s, %s, %s, %s, %s, %s)"
    __sqlget_address = "SELECT DISTINCT addrfrom FROM transfers WHERE addrto IN %s " \
                       "UNION SELECT DISTINCT addrto FROM transfers WHERE addrfrom IN %s"
    __sqlget_transfer = "SELECT * FROM transfers WHERE addrfrom IN %s OR addrto IN %s"

    def __init__(self, transferhash, addrfrom, addrto, symbol, value, blocktime):
        super().__init__([transferhash, addrfrom, addrto, symbol, value, blocktime])

    @classmethod
    def get_address(cls, addresses):
        sql = cls.__sqlget_address
        params = (addresses, addresses,)
        return super().query(sql, params)

    @classmethod
    def get_transfer(cls, addresses):
        sql = cls.__sqlget_transfer
        params = (addresses, addresses,)
        return super().query(sql, params)

    @classproperty
    def column(self) -> list[str]:
        return self._column


class Balance(Table):
    _tablename = "balances"
    _column = ["address", "balance"]
    _sqlsave = "REPLACE INTO %s (%s, %s) VALUES(%s, %s)"
    __sqlget = "SELECT balance FROM balances where address=%s"

    def __init__(self, address, balance):
        super().__init__([address, balance])

    @classmethod
    def get(cls, address) -> tuple[tuple]:
        sql = cls.__sqlget
        params = (address,)
        return super().query(sql, params)
