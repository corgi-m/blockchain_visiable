import pymysql


class DB:
    def __init__(self, host, port, user, passwd):
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        try:
            self._conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset='utf8mb4')
        except Exception:
            raise Exception
        self._dbname = None

    def commit(self):
        try:
            self.conn.commit()
        except Exception:
            raise Exception

    @property
    def conn(self):
        return self._conn

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def user(self):
        return self._user

    @property
    def passwd(self):
        return self._passwd

    @property
    def cursor(self):
        return self._conn.cursor()

    @property
    def dbname(self):
        return self._dbname

    @dbname.setter
    def dbname(self, value):
        self._dbname = value

    def connect_db(self):
        try:
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd)
        except Exception:
            raise Exception
        return conn

    def create_db(self, dbstruct):
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

    def use_db(self):
        usesql = "USE {}".format(self.dbname)
        try:
            cursor = self.cursor
            cursor.execute(usesql)
            cursor.close()
        except Exception:
            raise Exception

    def check_db(self, dbstruct):
        checksql = "SHOW DATABASES LIKE %s"
        try:
            cursor = self.cursor
            cursor.execute(checksql, self.dbname)
            self.create_db(dbstruct) if cursor.fetchone() is None else self.use_db()
            cursor.close()
        except Exception:
            raise Exception
