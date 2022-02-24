# coding=utf-8

import pymysql


# 封装数据库类
class DB:
    def __init__(self, host, port, user, passwd):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self._conn = self.connect_db()
        self._dbname = None

    def commit(self):
        try:
            self.conn.commit()
        except Exception:
            raise Exception
        return

    @property
    def conn(self) -> pymysql.connections.Connection:
        return self._conn

    @property
    def cursor(self) -> pymysql.cursors.Cursor:
        return self._conn.cursor()

    @property
    def dbname(self) -> str:
        return self._dbname

    @dbname.setter
    def dbname(self, value) -> None:
        self._dbname = value
        return

    def connect_db(self) -> pymysql.connections.Connection:
        try:
            conn = pymysql.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__passwd,
                                   charset='utf8mb4')
        except Exception:
            raise Exception
        return conn

    # 创建数据库
    def create_db(self, dbstruct) -> None:
        createsql = "CREATE DATABASE {}".format(self.dbname)
        try:
            cursor = self.cursor
            cursor.execute(createsql)
            self.use_db()
            sql = ''
            line = dbstruct.readline()
            while line:
                sql += line
                if line.endswith(';\n'):
                    cursor.execute(sql)
                    sql = ''
                line = dbstruct.readline()
            cursor.close()
        except Exception:
            raise Exception
        return

    # 使用该数据库
    def use_db(self) -> None:
        usesql = "USE {}".format(self.dbname)
        try:
            cursor = self.cursor
            cursor.execute(usesql)
            cursor.close()
        except Exception:
            raise Exception
        return

    # 检查数据库是否存在
    def check_db(self, dbstruct) -> None:
        checksql = "SHOW DATABASES LIKE %s"
        try:
            cursor = self.cursor
            cursor.execute(checksql, self.dbname)
            self.create_db(dbstruct) if cursor.fetchone() is None else self.use_db()
            cursor.close()
        except Exception:
            raise Exception
        return
