# -*- coding: utf-8 -*-
import sqlite3
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/back_end_code')
import shop_data as sd

def samai(data):
	j = json.loads(data)
	samai = j["23.5"]
	return samai

def get_data(shop_No,from_day,end_day=0,today=False,model=0):
	shop = sd.Shop_data(shop_No)
	db = "./back_end_code/DB/{0}.db".format(shop.name)
	connect = sqlite3.connect(db)
	cur = connect.cursor()
	print "DB connecting..."

	"""SQLの生成"""
	sql = "SELECT * FROM data WHERE day >= ? "
	if end_day != 0:
		sql = sql + "and day <= ?"
	if today == True:
		sql = "SELECT * FROM data WHERE day = ? "
	if model != 0:
		sql = sql + "and model = ?"


	if model ==0 and today == True:
		cur.execute(sql,(from_day,))
	elif model != 0 and today == True:
		cur.execute(sql,(from_day,model))
	elif model == 0 and end_day ==0:
		cur.execute(sql,(from_day,))
	elif model != 0 and end_day != 0:
		cur.execute(sql,(from_day,end_day,model))

	l = []
	all_start = 0
	sama = 0

	for d,m,No,BB,RB,ART,s,a_s,slump in cur.fetchall():
		data = [d,m,No,BB,RB,ART,s,a_s,slump]
		print No,a_s,samai(slump)
		all_start += a_s
		sama += samai(slump)

	print "all_data 差枚={0},　回転数={1}".format(sama,all_start)
	print u"{0}の機械割 {1}%".format(model,100*((all_start*3.0+sama)/(all_start*3)))

def get_model(shop_No):
	shop = sd.Shop_data(shop_No)
	db = "./back_end_code/DB/{0}.db".format(shop.name)
	connect = sqlite3.connect(db)
	cur = connect.cursor()
	print "DB connecting..."

	sql = "SELECT DISTINCT(model) from data"
	cur.execute(sql)

	get_list = [1,2,19,20,21,27,28,29,31,32,33,34,38,40,42,43,48,49,50,51,52,37]
	#get_list = [0,1,2,27,28,29,30,31,32,33]
	l = []
	s = u""
	for c,m in enumerate(cur.fetchall()):
		if c == 0:
			s += u" '{0}'".format(m[0])
		elif c in get_list:
			s += u" or model = '{0}'".format(m[0])
		l.append((c,m[0]))
		#print c,m[0]
	return s

def get_samai(shop_No,day,model=0):
	shop = sd.Shop_data(shop_No)
	db = "./back_end_code/DB/{0}.db".format(shop.name)
	connect = sqlite3.connect(db)
	cur = connect.cursor()
	print "DB connecting..."


	sql = u"SELECT day,model,all_start,slump FROM data "

	if model != 0:
		sql = sql + u"WHERE model = {0}".format(model)
	cur.execute(sql)
	
	sama = 0
	soukaiten = 0
	for d, m ,a_s, s in cur.fetchall():
		if d == day:
			sama += samai(s)
			soukaiten += a_s
			#print d,m,a_s,samai(s)

	print "{0} 差枚{1}枚　総回転{2}回転".format(day,sama,soukaiten)

	try:
		print "機械割{0}%".format(100.0*(soukaiten*3.0+sama)/(soukaiten*3.0))
	except ZeroDivisionError:
		print "新台入れ替え"






if __name__ == "__main__":
	m=get_model("2")

	get_samai("2",u"2017/02/23",m)


