 # -*- coding: utf-8 -*-
# 指定生成环境的配置
# 由APP_CONFIG_FILE环境变量指定，指定为绝对路径，如：
#       APP_CONFIG_FILE=/Users/zhouyanhui/PycharmProjects/mini_web/config/production.py
# 此配置最后被加载，会覆盖其他默认配置
DEBUG = False

LOG_FILE='log/h5game.log'

SECRET_KEY='zRbcL8jGqESN3eUYBaDtRatyOndHeprZ'

DB_CONF = {
    "host" :'10.18.103.121',
    "user" : 'luofei',
    "passwd" : '16021incloud',
    "dbname" : 'h5_game'
}
REDIS_CONF = {
	"host": '127.0.0.1',
	"port": 6379,
	"password": "yike",
	"db": 0,
	"socket_timeout": 5,
	"socket_connect_timeout": 1,
	"socket_keepalive": 7200 
}

APP_ID = ''
APP_SECERT = ''
WEIXIN_JS_URL = ''