import psycopg2
from config import Config

DSN = Config.DSN
class Postgres:
    def __init__(self, dsn=None, read_write=None):
        self.dsn = dsn
        self.read_write = read_write
        self.conn = psycopg2.connect(self.dsn)

    def cursor(self):
        return self.conn.cursor()

    def execute(self, sql, params=None):
        cur = self.cursor()
        cur.execute(sql, params)
        try:
            return cur.fetchone()[0]
        except:
            pass

    def select(self, sql, params=None):
        res = []
        cur = self.cursor()
        cur.execute(sql, params)
        columns = [c.name for c in cur.description]
        for row in cur.fetchall():
            res.append(row)
        return columns, res

    def dict_select(self, sql, params=None):
        cols, rows = self.select(sql, params)
        res = []
        for row in rows:
            rres = {}
            for col, val in zip(cols, row):
                rres[col] = val
            res.append(rres)
        return res

    def commit(self):
        self.conn.commit()

