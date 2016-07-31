# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import UserPlayOriginGameInfo


#####用户玩游戏信息
#####userId, activeId, questionIds, playQuestionId, result):
__author__ = 'luofei'

######用户玩共享过来的游戏的情况
#######id, keyword, signWord, url, title content, resource_url
TABLE_NAME= " user_play_origin_game_info "
COLUMNS = " user_id, active_id, question_ids, play_question_id, failed_count ,result "
INSERT_SQL = '''INSERT INTO ''' + TABLE_NAME + '''(id, user_id, active_id, ''' \
		+ '''question_ids, play_question_id, failed_count, result, status, update_time, create_time) ''' \
		+ ''' VALUES (null, %s, %s, %s, %s, 0, 0, 0, now(), now())'''
UPDATE_SQL = ''' UPDATE ''' + TABLE_NAME + ''' SET play_question_id = %s WHERE user_id = %s AND active_id = %s'''
UPDATE_RESULT_FAILEDCOUNT_SQL = '''UPDATE ''' + TABLE_NAME + ''' SET result = %s, failed_count = failed_count + %s WHERE user_id = %s AND active_id = %s'''
UK_SQL = '''SELECT ''' + COLUMNS +  ''' FROM ''' + TABLE_NAME + '''WHERE status = 0 AND user_id = %s AND active_id = %s'''
COUNT_SQL = '''SELECT COUNT(*) FROM ''' + TABLE_NAME + ''' WHERE status = 0 AND user_id = %s AND active_id = %s'''

class UserPlayOriginGameInfoDao:
	def insert(self, userId, activeId, randomQuestionIds, playQuestionId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(INSERT_SQL, (str(userId), str(activeId), str(randomQuestionIds), str(playQuestionId)))
		dbConn.commit()

	def queryInfo(self, userId, activeId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UK_SQL, (str(userId), str(activeId)))
			result = cur.fetchone()
		return self._toObject(result)

	def updateResultFailedCount(self, userId, activeId, result, failedCount):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UPDATE_RESULT_FAILEDCOUNT_SQL, (str(result), str(failedCount), str(userId), str(activeId)))
		dbConn.commit()

	def updatePlayQuestionId(self, userId, activeId, playQuestionId):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(UPDATE_SQL, (str(playQuestionId), str(userId), str(activeId)))
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
		return UserPlayOriginGameInfo(db_item[0], db_item[1], db_item[2], db_item[3], db_item[4], db_item[5])
