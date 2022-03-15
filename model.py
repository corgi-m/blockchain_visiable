# coding=utf-8

from config import config


# 类属性访问
class classproperty:
    def __init__(self, method):
        self.method = method

    def __get__(self, instance, owner):
        return self.method(owner)


# 表父类
class Table:
    _tablename: str = None
    _column: list[str] = None
    _sqlsave = None
    __sqlget = "SELECT * FROM %s"
    __isexist = "SELECT EXISTS(SELECT * FROM %s WHERE %s=%s)"

    def __init__(self, value):
        self._value = value

    # sql查询语句格式化
    @staticmethod
    def sqlformat(sql, arglist) -> str:
        sql = sql.replace('%s', '{}', len(arglist))
        sql = sql.format(*arglist)
        return sql

    # 保存记录
    def save(self) -> None:
        try:
            cur = config.db.cursor
            sql = self.sqlformat(self.__class__._sqlsave, [self.__class__._tablename] +
                                 self.__class__._column)
            cur.execute(sql, self._value)
            config.db.commit()
            cur.close()
        except Exception as e:
            print("sql save error:")
            print(self.__class__._sqlsave, [self.__class__._tablename] +
                  self.__class__._column, self._value, file=config.log)
            print(e)
        return

    # 查询sql语句
    @staticmethod
    def query(sql, params):
        try:
            cur = config.db.cursor
            cur.execute(sql, params)
            result = cur.fetchall()
            cur.close()
            return result
        except Exception as e:
            print("Error: unable to fetch data: query")
            print(e)
            print(params)
            print(sql)
            return ()

    # 获取整表记录（已弃用）
    @classmethod
    def get_db(cls) -> list[list[str]]:
        try:
            cur = config.db.cursor
            cur.execute(cls.sqlformat(cls.__sqlget, [cls._tablename]))
            results = cur.fetchall()
            cur.close()
            return results
        except Exception as e:
            print("Error: unable to fetch data: get_db")
            print(e)

    # 查询某主键是否存在
    @classmethod
    def is_exist(cls, value) -> bool:
        try:
            cur = config.db.cursor
            cur.execute(cls.sqlformat(cls.__isexist, [cls._tablename, cls._column[0]]), value)
            results = cur.fetchone()
            cur.close()
            return True if results[0] == 1 else False
        except Exception as e:
            print("Error: unable to fetch data: is_exist")
            print(e)


# 标签类
class Label(Table):
    _tablename = "labels"
    _column = ["address", "tag"]
    _sqlsave = "REPLACE INTO %s (%s,%s)  VALUES(%s, %s)"
    __sqlget = "SELECT tag FROM labels where address=%s"

    def __init__(self, address, tag):
        super().__init__([address, tag])

    # 获取地址标签
    @classmethod
    def get(cls, address) -> tuple[tuple[str]]:
        sql = cls.__sqlget
        params = (address,)
        return super().query(sql, params)


# 交易类
class Transfer(Table):
    _tablename = "transfers"
    _column = ["transferhash", "addrfrom", "addrto", "symbol", "value", "blocktime"]
    _sqlsave = "REPLACE INTO %s (%s, %s, %s, %s, %s, %s)  VALUES(%s, %s, %s, %s, %s, %s)"
    __sqlget_address = "SELECT DISTINCT addrfrom FROM transfers WHERE addrto IN %s " \
                       "UNION SELECT DISTINCT addrto FROM transfers WHERE addrfrom IN %s"
    __sqlget_transfer = "SELECT * FROM transfers WHERE addrfrom IN %s OR addrto IN %s"

    def __init__(self, transferhash, addrfrom, addrto, symbol, value, blocktime):
        super().__init__([transferhash, addrfrom, addrto, symbol, value, blocktime])

    # 获取相关地址（爬虫）
    @classmethod
    def get_address(cls, addresses) -> tuple[tuple[str]]:
        sql = cls.__sqlget_address
        params = (addresses, addresses,)
        return super().query(sql, params)

    # 获取某地址交易记录
    @classmethod
    def get_transfer(cls, addresses) -> tuple[tuple[str]]:
        sql = cls.__sqlget_transfer
        params = (addresses, addresses,)
        return super().query(sql, params)

    # 获取表中列名
    @classproperty
    def column(self) -> list[str]:
        return self._column


# 持币类
class Balance(Table):
    _tablename = "balances"
    _column = ["address", "balance"]
    _sqlsave = "REPLACE INTO %s (%s, %s) VALUES(%s, %s)"
    __sqlget = "SELECT balance FROM balances where address=%s"

    def __init__(self, address, balance):
        super().__init__([address, balance])

    # 获取地址持币
    @classmethod
    def get(cls, address) -> tuple[tuple[str]]:
        sql = cls.__sqlget
        params = (address,)
        return super().query(sql, params)
