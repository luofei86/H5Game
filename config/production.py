 # -*- coding: utf-8 -*-
# 指定生成环境的配置
# 由APP_CONFIG_FILE环境变量指定，指定为绝对路径，如：
#       APP_CONFIG_FILE=/Users/zhouyanhui/PycharmProjects/mini_web/config/production.py
# 此配置最后被加载，会覆盖其他默认配置
DEBUG = False

CACHE_TYPE="redis"
CACHE_REDIS_HOST='192.168.2.4'
CACHE_REDIS_PORT=8643
CACHE_KEY_PREFIX='mini:web:'
CACHE_DEFAULT_TIMEOUT=24*7*3600

LOG_FILE='log/mini-web.log'
EN_PROPERTIES_FILE='/home/mk/mini_web/config/ln_en.properties'
CN_PROPERTIES_FILE='/home/mk/mini_web/config/ln_cn.properties'
TW_PROPERTIES_FILE='/home/mk/mini_web/config/ln_tw.properties'

DB_CONF = {
    "host" :'10.18.103.121',
    "user" : 'luofei',
    "passwd" : '16021incloud',
    "dbname" : 'h5_game'
}