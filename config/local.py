 # -*- coding: utf-8 -*-
# 指定生成环境的配置
# 由APP_CONFIG_FILE环境变量指定，指定为绝对路径，如：
#       APP_CONFIG_FILE=/Users/luofei/source/H5game/config/production.py
# 此配置最后被加载，会覆盖其他默认配置
DEBUG = False

CACHE_TYPE="redis"
CACHE_REDIS_HOST='127.0.0.1'
CACHE_REDIS_PORT=8643
CACHE_KEY_PREFIX='h5game:'
CACHE_DEFAULT_TIMEOUT=24*7*3600

LOG_FILE='log/h5game.log'

DB_CONF = {
    "host" :'127.0.0.1',
    "user" : 'luofei',
    "passwd" : '16021incloud',
    "dbname" : 'h5_game'
}