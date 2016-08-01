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
from services import UserInfoService
from models import *
from utils import *
from h5game_backend import LOGGER

page = Blueprint("page", __name__)

gameActiveInfoService = GameActiveInfoService.GameActiveInfoService()
gameQuestionInfoService = GameQuestionInfoService.GameQuestionInfoService()
userShareInfoService = UserShareInfoService.UserShareInfoService()
userShareLimitInfoService = UserShareLimitInfoService.UserShareLimitInfoService()
gameBizService = GameBizService.GameBizService()
userInfoService = UserInfoService.UserInfoService()


@page.route('/welcome/<string:signWord>')
def welcome(signWord):
    resp = gameBizService.gameHomepageInfo(1, signWord)
    return render_template("welcome.html", resp = resp)

#####userInfoService get openId from cookie
@page.route('/play/<int:activeId>')
def play(activeId):
	LOGGER.info("Come")
	openId = "aadfadflkjcao12-AAL-AC"
	userId = userInfoService.getUserId(openId)
	# if request.method == 'POST':
	# 	questionId = request.form[questionId]
	# 	answerId = request.form[questionId]
	# 	if questionId is not None and answerId is not None:
	# 		return self._playWithAnswer(userId, openId, activeId, questionId, answerId)
	if userId is None:
		return render_template("403.html"), 403
	resp = gameBizService.firstPlay(userId, activeId)
	if not resp:
		return render_template("403.html"), 403
	##可以玩
	if(resp.get('play')):
		return render_template("game.html", resp = resp)
	##已中奖
	elif(resp.get('prized')):
		return render_template("prized.html", resp = resp)
##需要分享才能玩
	elif(resp.get('needShare')):
		return render_template("share.html", resp = resp)
	##当前游戏不能玩了，等待下次
	else:
		return render_template("waitnext.html", resp = resp)

def _playWithAnswer(self, userId, openId, activeId, questionId, answerId):
	resp = gameBizService.next(userId, activeId, questionId, answerId)
	if not resp:
		return render_template("403.html"), 
	if not resp.get('success'):
		if resp.get['failedType'] == 'server':###服务器压力过大，请稍候
			return render_template("500.html"), 
		elif resp.get['failedType'] == 'illegal':####数据问题
			return render_template("403.html"), 403
		else:###达到用户限制，也无法分享
			return render_template('waitnext.html')
	if(resp.get('play')):
		return render_template("game.html", resp = resp)
	##已中奖
	elif(resp.get('prized')):
		return render_template("prized.html", resp = resp)
	##需要分享才能玩
	elif(resp.get('needShare')):
		return render_template("share.html", resp = resp)
	else:###达到用户限制，也无法分享
		return render_template('waitnext.html')


@page.route('/shareplay/<int:activeId>/<string:shareCode>')
def sharePlay(activeId, shareCode):
	openId = "aadfadflkjcao12-AAL-AC"
	userId = userInfoService.getUserId(openId)
	resp = gameBizService.sharePlay(userId, activeId, shareCode)	
	
	if not resp:
		return render_template("403.html"), 
	LOGGER.info(resp)
	if not resp.get('success'):
		if str(resp.get['failedType']) == 'illegal':####数据问题
			return render_template("403.html"), 403		
		elif str(resp.get['failedType']) == 'server':###服务器压力过大，请稍候
			return render_template("500.html"), 
		else:###达到用户限制，也无法分享
			return render_template('waitnext.html')
	if(resp.get('play')):
		return render_template("game.html", resp = resp)
	##已中奖
	elif(resp.get('prized')):
		return render_template("prized.html", resp = resp)
	##需要分享才能玩
	elif(resp.get('needShare')):
		return render_template("share.html", resp = resp)
	else:###达到用户限制，也无法分享
		return render_template('waitnext.html')


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

