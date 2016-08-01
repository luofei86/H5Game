# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserPlayShareGameInfo


#####用户玩游戏信息
#####userId, activeId, shareCode, questionIds, playQuestionId, result):
__author__ = 'luofei'

######用户玩共享过来的游戏的情况
#######id, keyword, signWord, url, title content, resource_url
TABLE_NAME= " user_play_share_game_info "
COLUMNS = " id, user_id, active_id, share_code, question_ids, play_question_id, result "
INSERT_SQL = '''INSERT INTO ''' + TABLE_NAME + '''(id, user_id, active_id, share_code, ''' \
		+ '''question_ids, play_question_id, result, status, update_time, create_time) ''' \
		+ ''' VALUES (null, %s, %s, %s, %s, %s, %s, 0, now(), now())'''
UPDATE_PLAY_QUESTION_IDSQL = ''' UPDATE ''' + TABLE_NAME + ''' SET play_question_id = %s WHERE id = %s'''
UPDATE_RESULT_SQL = '''UPDATE ''' + TABLE_NAME + ''' SET result = %s WHERE id = %s'''
UK_SQL = '''SELECT ''' + COLUMNS +  ''' FROM ''' + TABLE_NAME + '''WHERE status = 0 AND user_id = %s AND active_id = %s AND share_code = %s '''
LAST_SQL = '''SELECT ''' + COLUMNS +  ''' FROM ''' + TABLE_NAME + '''WHERE status = 0 AND user_id = %s AND active_id = %s ORDER BY `id` DESC LIMIT 1 '''
COUNT_SQL = '''SELECT COUNT(*) FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND user_id = %s AND active_id  = %s'''

class UserPlayShareGameInfoDao:	
	def insert(self, userId, activeId, sahreCode, randomQuestionIds, playQuestionId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(userId), str(activeId), str(sahreCode), str(randomQuestionIds), str(playQuestionId)))
		dbConn.commit()

	def queryInfoByUk(self, userId, activeId, shareCode):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(userId), str(activeId), str(shareCode)))
			result = cur.fetchone()
		return self._toObject(result)

	def queryLastInfo(self, userId, activeId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(LAST_SQL, (str(userId), str(activeId)))
			result = cur.fetchone()
		return self._toObject(result)

	def updateResult(self, id, result):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UPDATE_RESULT_SQL, (str(result), str(id)))
		dbConn.commit()

	def updatePlayQuestionId(self, id, playQuestionId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UPDATE_PLAY_QUESTION_IDSQL, (str(playQuestionId), str(id)))
		dbConn.commit()

	def count(self, userId, activeId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(COUNT_SQL, (str(userId), str(activeId)))
			count = cur.fetchone()
			if count is not None:
				return count[0]
		return 0

#######id, keyword, sign_word, url, title content, resource_url
	def _toObject(self, db_item):
		if db_item is None:
			return None
		return UserPlayShareGameInfo(db_item[0], db_item[1], db_item[2], db_item[3], db_item[4], db_item[5], db_item[6])
