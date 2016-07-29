from flask import g
from dao.MysqlDatasource import *

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DataSource.connect()
    return db