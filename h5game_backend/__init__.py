# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.cache import Cache
from flask import g
from dao.MysqlDatasource import DataSource

import sys


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='')
app.config.from_object('config.default')
app.config.from_pyfile('config.py', silent=True)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

cache = Cache(app) # ,config={'CACHE_TYPE': 'redis'}

LOGGER = app.logger
# if not debug , log to file
import logging
if not app.debug:
    from cloghandler import ConcurrentRotatingFileHandler
    filename = app.config.get('LOG_FILE', "h5game.log")
    handler = ConcurrentRotatingFileHandler(filename, 'a', 10 * 1024 * 1024 , 5)
    LOGGER.setLevel(logging.INFO)
else:
    handler = logging.StreamHandler()
    LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(handler)

from controller import *
from views import *

app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(page, url_prefix="/page")


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_first_request
def init_db():
    db_conf = app.config.get("DB_CONF", None)
    LOGGER.info(db_conf)
    if db_conf:
        DataSource.setDbInfo(db_conf)


# add blue print views
# from .views.error import *

# import assets and template extensions
from utils import assets
# from .utils import template_filter_ex