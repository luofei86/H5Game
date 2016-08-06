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
from services import UserInfoService

from models import *
from utils import *
from h5game_backend import app
from h5game_backend import LOGGER


page = Blueprint("page", __name__)


gameBizService = GameBizService.GameBizService()
userInfoService = UserInfoService.UserInfoService()


@page.route("/welcome/callback")
@page.route("/welcome/callback/")
def callback():
	sign = request.args.get("sign")
	LOGGER.debug(sign)
	if not sign:
		return render_template("404.html"), 404
	shareCode = request.args.get("shareCode")
	code = request.args.get("code")
	if not code:
		return render_template("404.html"), 404
	####Init user
	LOGGER.debug(code)
	userInfoService.addInfo(code)
	session['unionId'] = code
	return redirect(url_for('.welcome', signWord = sign, shareCode = shareCode))

@page.route('/welcome/<string:signWord>')
@page.route('/welcome/<string:signWord>/<string:shareCode>')
def welcome(signWord, shareCode=None):
	try:
		unionId = session["unionId"]
		if not unionId:
			return render_template("404.html"), 404
		if not userInfoService.getUserId(unionId):
			return render_template("404.html"), 404

		resp = gameBizService.gameHomepageInfo(1, signWord)
		if resp is None:
			return render_template("404.html"), 404
		if resp is not None and shareCode is not None:
			resp['shareCode'] = shareCode
		resp['unionId'] = unionId
		LOGGER.debug(str(resp))
		if resp.get('success'):
			if resp.get('prized'):
				return render_template("prized.html", resp = resp)
		resp['signWord'] = signWord
		return render_template("welcome.html", resp = resp)
	except:
		return render_template("404.html")

@page.route("/homepage/<string:signWord>")
@page.route("/homepage/<string:signWord>/")
@page.route("/homepage/<string:signWord>/<string:shareCode>")
@page.route("/homepage/<string:signWord>/<string:shareCode>/")
def homepage(signWord, shareCode = None):
	try:
		unionId = session["unionId"]
		if not unionId:
			return render_template("404.html"), 404
		if not userInfoService.getUserId(unionId):
			return render_template("404.html"), 404

		resp = gameBizService.gameHomepageInfo(1, signWord)
		if resp is None:
			return render_template("404.html"), 404
		if resp is not None and shareCode is not None:
			resp['shareCode'] = shareCode
		resp['unionId'] = unionId
		if resp.get('success'):
			if resp.get('prized'):
				return render_template("prized.html", resp = resp)
		return render_template("homepage.html", resp = resp)
	except:
		return render_template("404.html")


####由系统后台自动生成的供用户直接游戏的地址，在没有自有游戏的情况下，如有分享的游戏没玩完，则完分享的，否则告诉用户无法玩了
@page.route('/play/<int:activeId>', methods=['GET', 'POST'])
@page.route('/play/<int:activeId>/', methods=['GET', 'POST'])
@page.route('/play/<int:activeId>/<string:shareCode>', methods=['GET', 'POST'])
def play(activeId, shareCode=None):
	try:	
		unionId = session["unionId"]
		userId = userInfoService.getUserId(unionId)
		if userId is None:
			return render_template("404.html"), 403
		LOGGER.debug(str(userId))
		if request.method == 'POST':
			questionId = request.form['questionId']
			answerId = request.form['answerId']
			if questionId and answerId and shareCode:
				return _playSharedWithAnswer(userId, unionId, activeId, shareCode, questionId, answerId)
				###共享游戏
			elif questionId  and answerId:
				return _playOriginWithAnswer(userId, unionId, activeId, questionId, answerId)
			else:
				return render_template("404.html"),403
		if shareCode:
			return _playShareGame(userId, unionId, activeId, shareCode)
		resp = gameBizService.playGame(userId, activeId)
		if not resp:
			return render_template("404.html"), 403
		if not resp.get('success'):
			if resp.get('failedType') == 'server':###服务器压力过大，请稍候
				return render_template("404.html"), 
			elif resp.get('failedType') == 'illegal':####数据问题
				return render_template("404.html"), 403
			else:###达到用户限制，也无法分享
				return render_template('share.html', resp = resp)
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
	except:
	 	return render_template("404.html"), 500

def _playOriginWithAnswer(userId, unionId, activeId, questionId, answerId):
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
			return render_template('share.html', resp = resp)
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

@page.route("/sharedtoplay/", methods=['GET', 'POST'])
def sharedToPlay():
	# try:
	unionId = session["unionId"]
	userId = userInfoService.getUserId(unionId)
	id = request.form['id']
	shareCode = request.form['shareCode']
	resp = gameBizService.userShared(id, shareCode)
	if not resp:
		return render_template("404.html"), 403
	if resp.get('success'):
		if(resp.get('play')):
			return redirect("/page/play/" + str(resp.get('playInfo').get('activeId')), code=302)			
		return render_template("404.html", resp = resp)	
	else:
		if resp.get("failedType") == 'limit':
			return render_template('nomoreplay.html', resp = resp)
		else:
			return render_template("404.html"), 403

def _playShareGame(userId, unionId, activeId, shareCode):
	resp = gameBizService.playShareGame(userId, unionId, activeId, shareCode)	
	if not resp:
		return render_template("404.html"), 
	LOGGER.info(resp)
	if not resp.get('success'):
		####数据问题
		if resp.get('failedType') == 'illegal':
			return render_template("404.html"), 403	
		###服务器压力过大，请稍候	
		elif resp.get('failedType') == 'server':
			return render_template("404.html"), 
		else:###达到用户限制，也无法分享
			return render_template('share.html', resp =resp)
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
def _playSharedWithAnswer(userId, unionId, activeId, shareCode, questionId, answerId):
	resp = gameBizService.shareGameNext(userId, activeId, shareCode, questionId, answerId)
	LOGGER.info(resp)
	if not resp:
		return render_template("404.html"), 
	if not resp.get('success'):
		if resp.get('failedType') == 'server':###服务器压力过大，请稍候
			return render_template("404.html"), 
		elif resp.get('failedType') == 'illegal':####数据问题
			return render_template("404.html"), 403
		else:###达到用户限制，也无法分享
			return render_template('nomoreplay.html', resp = resp)
	if(resp.get('play')):
		return render_template("game.html", resp = resp)
	##已中奖
	elif(resp.get('prized')):
		return render_template("prized.html", resp = resp)
	else:###达到用户限制，也无法分享
		return render_template('nomoreplay.html', resp = resp)
