# -*- coding: utf-8 -*-

import MySQLdb
from _mysql_exceptions import OperationalError
from services.DbService import get_db
from contextlib import closing

__author__ = 'luofei'

sql = '''SELECT id, title, resource_url, resource_type, possible_answer_ids, right_answer_id FROM h5_game_info WHERE status = 0'''

class GameInfoDao:
	def queryAllInfos(this):
		dbConn = get_db()
		with closing(dbConn.cursor()) as cur:
			cur.execute(sql)
			retlist = cur.fetchall()
			dbConn.commit()
		return retlist;