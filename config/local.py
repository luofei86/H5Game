 # -*- coding: utf-8 -*-
# 指定生成环境的配置
# 由APP_CONFIG_FILE环境变量指定，指定为绝对路径，如：
# APP_CONFIG_FILE=/Users/luofei/source/H5game/config/production.py
# 此配置最后被加载，会覆盖其他默认配置
DEBUG = True

LOG_FILE='log/h5game.log'

SECRET_KEY='zRbdL8jGqESN3eUYBaDtRatyOndHeprZ'

DB_CONF = {
    "host" :'127.0.0.1',
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

APP_ID = 'wx4d1ff3f3dbe1505f'
APP_SECERT = 'cf2c4d491c49b6a0fa8a4cfa47a6d8f8'
WEBSITE_ROOT = "http://192.168.1.110:12123/page"
SHARE_PAGE = 'http://192.168.1.110:12123/page/welcome/callback&sign='
NAV_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=http://api.yiketalks.com/V2/command/wechatTokenSend?url=%s&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect'