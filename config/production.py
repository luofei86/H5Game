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

#####给微信用户跳转用的，无须变更
SHARE_TO_WEIXIN_PLAY_URL = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"

####微信用户授权后跳转过来的页面
SHARE_TO_WEIXIN_REDIRECT_URL = "http://api.yiketalks.com/V2/command/wechatTokenSend?url=%s"

#####微信用户跳转到yike后，yike再跳转到游戏服务器
YIKE_REDIRECT_GAME_UR_AND_CURRENT_GAME_WEBISTE = "http://192.168.1.110:12123/page/welcome/share/callback/%s&sign=%s"

