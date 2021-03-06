# -*- coding: utf-8 -*-

from flask import Flask
from flask import g
from dao.MysqlDatasource import DataSource

import sys


reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='')
app.config.from_object('config.default')
app.config.from_pyfile('config.py', silent=True)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

LOGGER = app.logger
# if not debug , log to file
import logging
if not app.debug:
    from cloghandler import ConcurrentRotatingFileHandler
    filename = app.config.get('LOG_FILE', "h5game.log")
    handler = ConcurrentRotatingFileHandler(filename, 'a', 10 * 1024 * 1024 , 5)
    LOGGER.setLevel(logging.INFO)
else:
    from cloghandler import ConcurrentRotatingFileHandler
    filename = app.config.get('LOG_FILE', "h5game.log")
    handler = ConcurrentRotatingFileHandler(filename, 'a', 10 * 1024 * 1024 , 5)
    LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(handler)

from services.RedisConf import RedisConf
import redis

REDIS_CACHE_CONF = RedisConf(app.config.get("REDIS_CONF", None))
POOL = redis.ConnectionPool(host = REDIS_CACHE_CONF.host, port = REDIS_CACHE_CONF.port, \
                            password = REDIS_CACHE_CONF.password, db = REDIS_CACHE_CONF.db, \
                            socket_timeout = REDIS_CACHE_CONF.socket_timeout, \
                            socket_connect_timeout = REDIS_CACHE_CONF.socket_connect_timeout, \
                            socket_keepalive = REDIS_CACHE_CONF.socket_keepalive)

from controller import *
from views import *


app.register_blueprint(game, url_prefix="/game")

# add blue print views
# from .views.error import *

# import assets and template extensions
from utils import assets
from utils import template_filter_ex

# from .utils import template_filter_ex