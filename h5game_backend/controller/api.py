# -*- coding: utf-8 -*-

from flask import render_template,jsonify,Blueprint,url_for,redirect,request,session,g
import re
import random
import json
import math
import uuid

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
from services import GameQuestionInfoService
from services import UserShareLimitInfoService
from services import UserShareInfoService
from services import GameActiveInfoService
from services import GameBizService
from models import *
from utils import *


#API
# iosAPI = IosAPI()
# iosUnionAPI = IosUnionAPI()
# strategyAPI = StrategyAPI()
# AppMap = AppMap()
# baiduSearch = BaiduSearch()

# TIMEOUT=600
# VIEW_TYPE_COOKIE_KEY = 'view_type'
# COOKIE_MAX_AGE = 86400
# #COOKIE_MAX_AGE = 60

# page = Blueprint('page', __name__)

api = Blueprint("api", __name__)

gameActiveInfoService = GameActiveInfoService.GameActiveInfoService()
gameQuestionInfoService = GameQuestionInfoService.GameQuestionInfoService()
userShareInfoService = UserShareInfoService.UserShareInfoService()
userShareLimitInfoService = UserShareLimitInfoService.UserShareLimitInfoService()
gameBizService = GameBizService.GameBizService()
# def make_cache_key(*args, **kwargs):
#     path = request.path
#     items = request.args.items()
#     items.append(path)
#     items.append(g.is_mobile) #cache different view for pc/mobile
#     args = str(hash(frozenset(items)))
#     s = args.encode('utf-8')
#     return args

# #TODO
# def set_client_session():
#     sessionid =  request.cookies.get('sessionid',None)
#     if sessionid:
#         session['client'] = sessionid
#     else:
#         session['client'] = uuid.uuid4()

# MOBILE_PATTERN = re.compile('(android|ios|iphone|ipad|ipod|symbian|mobile)', re.IGNORECASE)
# ANDROID_PATTERN = re.compile('android', re.IGNORECASE)

# def check_mobile():
#     view_type = request.args.get('view_type', None)
#     g.is_mobile = False
#     if view_type in ['mobile','pc']:
#         g.is_mobile = view_type == 'mobile'
#         return 
#     cookie = request.cookies.get('view_type', None)
#     if cookie:
#         g.is_mobile = cookie == 'mobile'
#         return
#     m = MOBILE_PATTERN.search(str(request.user_agent))
#     if m:
#         g.is_mobile = True
#         return

# def get_channel():
#     channel = request.args.get('channel',None)
#     if channel:
#         session['channel']=channel
#     elif 'channel' in session:
#         channel = session['channel']
#     if channel:
#         return channel
#     return g.is_mobile and "m.appchina.com" or "www.appchina.com"

# IOS9_PATTERN = re.compile('(os 9)', re.IGNORECASE)
# #log ios9 user
# def statistic():
#     pass
# '''
#     ua = str(request.user_agent)
#     m = IOS9_PATTERN.search(ua)
#     if m:
#         LOGGER.info("ios[9] " + ua)
#     else:
#         LOGGER.info("ios[other] " + ua)
# '''

# @page.before_request
# def before():
#     #if request.referrer:
#     #    print "referrer:" + request.referrer
#     set_client_session()
#     check_mobile()

# @page.after_request
# def after(resp):
#     statistic()
#     resp.headers.add('Vary','User-Agent')
#     set_cookie(resp)
#     return resp

# SPIDER_PATTERN = re.compile('(Baiduspider|Googlebot|bingbot|Yahoo! Slurp|Sogou web spider|HaosouSpider|ToutiaoSpider)')
# def isSpider(ref):
#     return SPIDER_PATTERN.search(str(request.user_agent))

# def need_to_android(ref):
#     if not isSpider(ref) and g.is_mobile and ANDROID_PATTERN.search(str(request.user_agent)):
#         log = {}
#         if request.referrer:
#             log['ref'] = request.referrer
#         log['ua']= str(request.user_agent)
#         log['url']= request.url
#         log['to_url']= 'http://m.appchina.com/'+ref
#         try:
#             LOGGER.info(json.dumps(log))
#         except:
#             pass
#         return True,log['to_url']
#     return False,None

# def get_template_name(name):
#     #shortcut.appchinc.com to mobile site
#     if g.is_mobile or request.host == 'shortcut.appchina.com':
#         template_prefix = 'mobile' 
#     else:
#         template_prefix = 'pc'
#     return "%s/%s.html"%(template_prefix,name)

# def set_cookie(resp):

#     if g.is_mobile:
#         view_type = 'mobile'
#     else:
#         view_type = 'pc'

#     resp.set_cookie(VIEW_TYPE_COOKIE_KEY, view_type, max_age = 864000)
#     if session['client']:
#         resp.set_cookie('sessionid',str(session['client']), max_age = 864000)




####
@api.route("/game/homepage/<string:signWord>")
def homepage(signWord):
    if not signWord:
        return jsonify(reslut=None)
    result = gameBizService.gameHomepageInfo(1, signWord)
    return jsonify(result = result)


##init all cache 
##if it's the first time to run this or ur cache crash  call it/
@api.route("/game/init/<string:pwd>")
def init(pwd):
    if(pwd != "h5gameforquarter"):
        return jsonify(done=False)
    ##init cache
    ##load all gameinfo
    return jsonify(done=True)

@api.route("/game/next/<string:token>/<int:id>/<int:step>")
def nextGame(token, id, step=0):
    ##check the token id is ok
    return jsonify(username="controller",pwd=123)
@api.route("/game/infos/<int:id>")
def gameInfos(id=0):
	# if(id == 0):
	# 	return jsonify(infos=gameQuestionInfoService.getAllInfos())
	return jsonify(infos=gameQuestionInfoService.getAllInfos())

@api.route("/game/question/check/<int:id>/<int:answerId>")
def checkAnswer(id, answerId):
    if(id <= 0 or answerId <= 0):
        return False
    result =  gameQuestionInfoService.checkAnswer(id, answerId)
    return jsonify(result=result)


#####game active api#####
####获取活动信息，在用户同意授权后，显示游戏首页
@api.route("/game/active/info/<string:key>/")
def getActiveInfo(key):
    if(key is None):
        return None
    if key.isdigit():
        result = gameActiveInfoService.getInfo(int(key))
    else:
        result = gameActiveInfoService.getInfo(key)
    return jsonify(result = result)

#####share api#####
######判断此用户在当前活动还可以再分享吗
@api.route("/game/share/count/check/<int:userId>/<int:activeId>")
def checkShareLimit(userId, activeId):
    if(id <= 0 or activeId <= 0):
        return False
    result = userShareLimitInfoService.incrAndcheckLimit(userId, activeId)
    return jsonify(result=result)

######获取用户分享时要展示的内容
@api.route("/game/share/content/gen/<int:userId><int:activeId>")
def genShareContent(userId, activeId):
    if(userId <= 0 and activeId <=0):
        return None
    #获取用户token传递或者其它数据库//

    ##获取活动的地址


    ##userId, userToken, activeId, activeUrl):
    result = userShareInfoService.genShareInfo(userId, userToken, activeId, activeUrl)
    return jsonify(result=result)
####share api####
#####在用户分享后将分享结果回传，用来决定用户是继续玩还是不能玩
@api.route("/game/share/feedback/<string:shareCode>/<int:result>")
def shareFeedback(shareCode, result):
    if result is None:
        return jsonify(result=False)
    if int(result) != 1 and int(result) != -1:
        return jsonify(result=False)
    shared = userShareInfoService.afterShare(shareCode, result)
    return jsonify(result=shared)


