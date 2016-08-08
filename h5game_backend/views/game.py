# -*- coding: utf-8 -*-

import sys, traceback

from flask import render_template,jsonify,Blueprint,url_for,redirect,request,session,g
import re
import random
import json
import math
import uuid

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from services import GameBizService
from services import WeixinService
from services import JsApiService
from services import UserInfoService
from services import RedisAdmin

from models import *
from utils import *
from h5game_backend import app
from h5game_backend import LOGGER


game = Blueprint("game", __name__)


gameBizService = GameBizService.GameBizService()
weixinService = WeixinService.WeixinService(app.config.get("APP_ID"), app.config.get("APP_SECERT"))
jsApiService = JsApiService.JsApiService(app.config.get("APP_SHARED_ID"), app.config.get("APP_SHARED_SECERT"))
userInfoService = UserInfoService.UserInfoService()
redisAdmin = RedisAdmin.RedisAdmin();

@game.route("/redirect/<string:signWord>")
@game.route("/redirect/<string:signWord>/")
@game.route("/redirect/<string:signWord>/<string:shareCode>")
@game.route("/redirect/<string:signWord>/<string:shareCode>/")
def redirectShare(signWord, shareCode = None):
	if not signWord:
		return render_template("404.html"), 404
	if shareCode:
		return redirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx4d1ff3f3dbe1505f&redirect_uri=http%3A%2F%2Fapi.yiketalks.com%2FV2%2Fcommand%2FwechatTokenSend%3Furl%3Dhttp%3A%2F%2Fh5.yiketalks.com/game%2Fwelcome%2Fshare%2Fcallback%2F"+ shareCode +"%26sign%3D" + signWord + "&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect", code = 302)
	else:
		return redirect("https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx4d1ff3f3dbe1505f&redirect_uri=http%3A%2F%2Fapi.yiketalks.com%2FV2%2Fcommand%2FwechatTokenSend%3Furl%3Dhttp%3A%2F%2Fh5.yiketalks.com/game%2Fwelcome%2Fcallback%26sign%3D" + signWord + "&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect", code = 302)


@game.route("/welcome/share/callback/<string:shareCode>")
def shareCallback(shareCode = None):
	sign = request.args.get("sign")
	if not sign:
		return render_template("404.html"), 404
	code = request.args.get("code")
	if not code:
		return render_template("404.html"), 404
	return redirect(url_for('.callback', sign = sign, shareCode = shareCode, code = code))


@game.route("/welcome/callback")
@game.route("/welcome/callback/")
@game.route("/welcome/callback/<string:sign>")
def callback(sign = None):
	try:
		#FOR DEBUG
		if not sign:
			sign = request.args.get("sign")
		LOGGER.debug("Sign:" + sign)
		if not sign:
			return render_template("404.html"), 404
		shareCode = request.args.get("shareCode")
		code = request.args.get("code")
		if not code:
			return render_template("404.html"), 404
		LOGGER.debug("Code:" + code)
		###code access
		userOpenInfo = weixinService.getOpenInfo(code)
		if userOpenInfo is None:
			return render_template("404.html"), 404
		LOGGER.debug("UserOpenInfo:" + str(userOpenInfo))
		openid = userOpenInfo['openid']
		if not userInfoService.getUserId(openid):
			userWeiXinInfo = weixinService.getUserInfo(openid, userOpenInfo['access_token'])
			if userWeiXinInfo is None:
				return render_template("404.html"), 404
			if hasattr(userWeiXinInfo, 'errcode'):
				userOpenInfo = weixinService.refreshOpenInfo(openid, userOpenInfo['refresh_token'])
				userWeiXinInfo = weixinService.getUserInfo(openid, userOpenInfo['access_token'])
				if userWeiXinInfo is None or hasattr(userWeiXinInfo, 'errcode'):
					return render_template("404.html"), 404
		####Init user
			LOGGER.debug("code" + code + ",userWeiXinInfo:" + str(userWeiXinInfo))
			userInfoService.addInfo(userWeiXinInfo)

		session['openId'] = openid
		return redirect(url_for('.welcome', signWord = sign, shareCode = shareCode, openId = openId))
	except Exception as e:
		LOGGER.debug("Uncatch exception:" + str(e))
		return render_template("404.html")

@game.route('/welcome/<string:signWord>')
@game.route('/welcome/<string:signWord>/<string:shareCode>')
def welcome(signWord, shareCode=None):
	try:
		#FOR DEBUG
		if request.args.get("browser"):
			openId = request.args.get("openId")
		else:
			openId = session["openId"]
		if not openId:
			openId = request.args.get("openId")
			if not openId:
				return redirect(url_for('.redirectShare', signWord = signWord, shareCode = shareCode))
		LOGGER.debug("openId:" + str(openId))
		session['openId'] = openId
		userId = userInfoService.getUserId(openId)
		if not userId:
			return render_template("404.html"), 404

		resp = gameBizService.gameHomepageInfo(userId, signWord)
		LOGGER.debug("gameHomepageInfo:" + str(resp))
		if resp is None:
			return render_template("404.html"), 404
		
		if resp is not None and shareCode is not None:
			resp['shareCode'] = shareCode		
		_initUserShareContent(userId, openId, resp)
		resp['openId'] = openId
		if resp.get('success'):
			if resp.get('prized'):
				LOGGER.debug("render to prized.html with resp:" + str(resp))
				return render_template("prized.html", resp = resp)
		resp['signWord'] = signWord
		LOGGER.debug("render to welcome.html with resp:" + str(resp))
		return render_template("welcome.html", resp = resp)
	except Exception as e:
		LOGGER.debug(str(e))
		return render_template("404.html")

@game.route("/homepage/<string:signWord>")
@game.route("/homepage/<string:signWord>/")
@game.route("/homepage/<string:signWord>/<string:shareCode>")
@game.route("/homepage/<string:signWord>/<string:shareCode>/")
def homepage(signWord, shareCode = None):
	try:
		###FOR DEUBG
		#openId = request.args.get("openId")		
		if request.args.get("browser"):
			openId = request.args.get("openId")
		else:
			openId = session["openId"]		
		if not openId:
			return render_template("404.html"), 404
		userId = userInfoService.getUserId(openId) 
		if not userId:
			return render_template("404.html"), 404

		resp = gameBizService.gameHomepageInfo(userId, signWord)
		if resp is None:
			return render_template("404.html"), 404
		if resp is not None and shareCode is not None:
			resp['shareCode'] = shareCode
		_initUserShareContent(userId, openId, resp)
		resp['openId'] = openId
		if resp.get('success'):
			if resp.get('prized'):
				return render_template("prized.html", resp = resp)
		return render_template("homepage.html", resp = resp)
	except Exception as e:
		LOGGER.debug(str(e))
		return render_template("404.html")


####由系统后台自动生成的供用户直接游戏的地址，在没有自有游戏的情况下，如有分享的游戏没玩完，则完分享的，否则告诉用户无法玩了
@game.route('/play/<int:activeId>', methods=['GET', 'POST'])
@game.route('/play/<int:activeId>/', methods=['GET', 'POST'])
@game.route('/play/<int:activeId>/<string:shareCode>', methods=['GET', 'POST'])
def play(activeId, shareCode=None):
	try:	
		openId = session["openId"]
		userId = userInfoService.getUserId(openId)
		if userId is None:
			LOGGER.debug("Play User id is None")
			return render_template("404.html"), 403
		
		if request.method == 'POST':
			questionId = request.form['questionId']
			answerId = request.form['answerId']
			if questionId and answerId and shareCode:
				return _playSharedWithAnswer(userId, openId, activeId, shareCode, questionId, answerId)
				###共享游戏
			elif questionId  and answerId:
				return _playOriginWithAnswer(userId, openId, activeId, questionId, answerId)
			else:
				LOGGER.debug("No questionId no answerId")
				return render_template("404.html"),403
		if shareCode:
			return _playShareGame(userId, openId, activeId, shareCode)
		resp = gameBizService.playGame(userId, activeId)
		if not resp:
			LOGGER.debug("Play game no resp.")
			return render_template("404.html"), 403
		if not resp.get('success'):
			if resp.get('failedType') == 'server':###服务器压力过大，请稍候
				LOGGER.debug("failedType == server," + str(resp))
				return render_template("404.html"), 
			elif resp.get('failedType') == 'illegal':####数据问题
				LOGGER.debug("failedType == illegal," + str(resp))
				return render_template("404.html"), 403
			else:###达到用户限制，也无法分享
				_initUserShareContent(userId, openId, resp)
				return render_template('share.html', resp = resp)
		_initUserShareContent(userId, openId, resp)
		##可以玩
		if(resp.get('play')):
			return render_template("game.html", resp = resp)
		##已中奖
		elif(resp.get('prized')):
			return render_template("prized.html", resp = resp)
	##需要分享才能玩
		elif(resp.get('needShare')):
			return render_template("nomoreplay.html", resp = resp)
		##当前游戏不能玩了，等待下次	
		else:
			return render_template("nomoreplay.html", resp = resp)
	except Exception as e:
		LOGGER.debug(str(e))
	  	return render_template("404.html"), 500

def _playOriginWithAnswer(userId, openId, activeId, questionId, answerId):
	resp = gameBizService.originGameNext(userId, activeId, questionId, answerId)
	if not resp:
		return render_template("404.html"), 
	if not resp.get('success'):
		if resp.get('failedType') == 'server':###服务器压力过大，请稍候
			return render_template("404.html"), 
		elif resp.get('failedType') == 'illegal':####数据问题
			return render_template("404.html"), 403
		else:###达到用户限制，也无法分享
			LOGGER.debug(resp)
			_initUserShareContent(userId, openId, resp)
			return render_template('share.html', resp = resp)
	
	_initUserShareContent(userId, openId, resp)	
		
	if(resp.get('play')):
		return render_template("game.html", resp = resp)
	##已中奖
	elif(resp.get('prized')):
		return render_template("prized.html", resp = resp)
	##需要分享才能玩
	elif(resp.get('needShare')):
		return render_template("nomoreplay.html", resp = resp)
	else:###达到用户限制，也无法分享
		return render_template('nomoreplay.html', resp = resp)

@game.route("/user/shared/<int:userId>/<string:shareCode>/<int:activeId>")
@game.route("/user/shared/<int:userId>/<string:shareCode>/<int:activeId>/")
def userShared(userId, shareCode, activeId):
	gameBizService.afterShared(userId, shareCode, activeId)
	return jsonify(done=True)


@game.route("/admin/flushcache/<string:pwd>")
@game.route("/admin/flushcache/<string:pwd>/")
def adminFlushcache(pwd):
	if pwd and str(pwd) == "yiketalksflushcache":
		redisAdmin.flushcache()
		return jsonify(done=True)
	return jsonify(done=False)

def _playShareGame(userId, openId, activeId, shareCode):
	resp = gameBizService.playShareGame(userId, openId, activeId, shareCode)	
	if not resp:
		return render_template("404.html"), 

	if not resp.get('success'):
		####数据问题
		if resp.get('failedType') == 'illegal':
			return render_template("404.html"), 403	
		###服务器压力过大，请稍候	
		elif resp.get('failedType') == 'server':
			return render_template("404.html"), 
		else:###达到用户限制，也无法分享
			_initUserShareContent(userId, openId, resp)
			return render_template('share.html', resp =resp)
	_initUserShareContent(userId, openId, resp)
	if(resp.get('play')):
		return render_template("game.html", resp = resp)
	##已中奖
	elif(resp.get('prized')):
		return render_template("prized.html", resp = resp)
	##需要分享才能玩
	elif(resp.get('needShare')):
		return render_template("nomoreplay.html", resp = resp)
	else:###达到用户限制，也无法分享
		return render_template('nomoreplay.html', resp = resp)

###共享玩的
def _playSharedWithAnswer(userId, openId, activeId, shareCode, questionId, answerId):
	resp = gameBizService.shareGameNext(userId, activeId, shareCode, questionId, answerId)
	if not resp:
		return render_template("404.html"), 
	if not resp.get('success'):
		if resp.get('failedType') == 'server':###服务器压力过大，请稍候
			return render_template("404.html"), 
		elif resp.get('failedType') == 'illegal':####数据问题
			return render_template("404.html"), 403
		else:###达到用户限制，也无法分享
			_initUserShareContent(userId, openId, resp)
			return render_template('nomoreplay.html', resp = resp)
	_initUserShareContent(userId, openId, resp)
	if(resp.get('play')):
		return render_template("game.html", resp = resp)
	##已中奖
	elif(resp.get('prized')):
		return render_template("prized.html", resp = resp)
	else:###达到用户限制，也无法分享
		return render_template('nomoreplay.html', resp = resp)

def _initUserShareContent(userId, openId, resp):
	LOGGER.debug("Get share url by userId:"+ str(userId)+ ", openId:"+str(openId)+", resp:"+str(resp))
	###def genUserShareContent(self, userId, openId, activeId, appId, signWord):
	userShareInfo = gameBizService.genUserShareContent(userId, openId, \
				resp['activeInfo']['id'], app.config.get("APP_SHARED_ID"), resp['activeInfo']['signWord'])
	LOGGER.debug("share url:" + str(userShareInfo))
	resp['userShareInfo'] = userShareInfo
	_initCurPageSignInfo(resp)

def _initCurPageSignInfo(resp):	
	curPage = request.url
	LOGGER.debug("Sign url:" + curPage)
	weiXinSignInfo = jsApiService.sign(curPage)
	if weiXinSignInfo:
		resp['weiXinSignInfo'] = weiXinSignInfo
		
