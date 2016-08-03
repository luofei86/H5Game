from flask import g
from dao.MysqlDatasource import DataSource

from h5game_backend import app
from h5game_backend import LOGGER

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = DataSource.connect()
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_first_request
def init_db():
    db_conf = app.config.get("DB_CONF", None)
    LOGGER.info("DbConf:" + str(db_conf))
    if db_conf:
        LOGGER.info(db_conf)
        DataSource.setDbInfo(db_conf)