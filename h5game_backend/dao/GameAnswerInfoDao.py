# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing

__author__ = 'luofei'

sql = '''SELECT id, title, resource_url, resource_type FROM h5_game_answer_info WHERE status = 0'''

class AnswerInfoDao:
	def queryAllInfos(self):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(sql)
			retlist = cur.fetchall()
			dbConn.commit()
		return retlist