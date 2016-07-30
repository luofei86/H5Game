# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing
from models import GameQuestionInfo

__author__ = 'luofei'

ALL_SQL = '''SELECT id, title, resource_url, resource_type, possible_answer_ids, right_answer_id, tips FROM h5_game_question_info WHERE status = 0'''
ID_SQL = '''SELECT id, title, resource_url, resource_type, possible_answer_ids, right_answer_id, tips FROM h5_game_question_info WHERE status = 0 AND id = %s'''

class GameQuestionInfoDao:
	def queryAllInfos(self):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ALL_SQL)
			result = cur.fetchall()
		if result is None:
			return None
		values = []
		for r in result:
			value = self._toObject(r)
			if value is None:
				continue
			values.append(value)
		return values

	def queryInfo(self, id):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(ID_SQL, (str(id)))
			result = cur.fetchone()
		return self._toObject(result)



	def _toObject(self, db_item):
		if db_item is None:
			return None

		result = GameQuestionInfo(db_item[0], db_item[1], db_item[2], db_item[3], 
									db_item[4], db_item[5], db_item[6])
		return result