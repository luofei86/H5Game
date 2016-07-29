# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.cache import Cache
from flask import g
from dao.MysqlDatasource import DataSource

app = Flask(__name__, instance_relative_config=True)
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

app.register_blueprint(api, url_prefix="/api")


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
# from .views.android import android_view
# from .views.ios import ios_view
# from .views.error import *

# app.register_blueprint(android_view, url_prefix='/android')
# app.register_blueprint(ios_view, url_prefix='/ios')

# import assets and template extensions
# from .utils import assets
# from .utils import template_filter_ex