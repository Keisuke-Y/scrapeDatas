# -*- coding: utf-8 -*-
from datetime import datetime as dt
import datetime
import sqlite3 
import time

class Juggler():
	def __init__(self,data):
		d = data
		self.date = d[0]
		self.No = d[1]
		self.BB = d[2]
		self.RB = d[3]
		self.start = d[4]
		self.p1 = d[5]
		self.p2 = d[6]
		self.p3 = d[7]
		self.p4 = d[8]
		self.p5 = d[9]
		self.p6 = d[10]
		self.setting = (self.p1 * 1 + self.p2 * 2 + self.p3 * 3 + self.p4 * 4 + self.p5 * 5 + self.p6 * 6 )/100

def input_date():


	while 1:
		print "スタートの日を YYYY-MM-DD で入力してください"
		s_date = raw_input()
		try:
			s_date_time = dt.strptime(s_date,"%Y-%m-%d")
			break
		except ValueError:
			print "不正な文字列です.　再度入力してください"
			print "\n\n------------------------------\n"

	while 1:
		print "\n-----------------\n終わりの日を YYYY-MM-DD で入力してください"
		print "本日までの場合は「today」を入力してください"
		e_date = raw_input()
		if e_date == "today":
			e_date_time = datetime.date.today()
			break
		try:
			e_date_time = dt.strptime(e_date,"%Y-%m-%d")
			break

		except ValueError:
			print "不正な文字列です.　再度入力してください"
			print "\n\n------------------------------\n"

	return (s_date_time,e_date_time)#日付入力 

def get_between_day(s_time,e_time):
	all_date = []
	end = "{0}-{1:02d}-{2:02d}".format(e_time.year,e_time.month,e_time.day)

	while 1:
		all_date.append("{0}-{1:02d}-{2:02d}".format(s_time.year,s_time.month,s_time.day))
		#print "{0}-{1:02d}-{2:02d}".format(s_time.year,s_time.month,s_time.day)
		if "{0}-{1:02d}-{2:02d}".format(s_time.year,s_time.month,s_time.day) == end:
			break
		s_time = s_time + datetime.timedelta(days=1)

	return all_date#取得するデータ選択

def get_data_from_db(all_date):
	db = "./sample_data/Juggler.db"
	connect = sqlite3.connect(db)
	cur = connect.cursor()

	sql = """SELECT * FROM Juggler WHERE date = "{0}" """.format(str(all_date[0]))

	for c, d in enumerate(all_date):
		if c == 0:
			pass
		sql = sql + """ or date = "{0}" """.format(str(d))
	cur.execute(sql)
	#print sql 

	all_data = {}

	for date,No,BB,RB,start,p1,p2,p3,p4,p5,p6 in cur.fetchall():
		if all_data.has_key(date) == False:
			all_data[date] = {}
		li = [date,No,BB,RB,start,p1,p2,p3,p4,p5,p6]
		all_data[date][No] = Juggler(li)

	return all_data#日付に従ってデータ取得

def input_option():
	while 1:
		s = 0
		print """回転数が少ない台を無視しない場合は"1"
3000回転以上を加味する場合は"2"
7000回転以上を加味する場合は"3"を入力してください

またその他回転数の指定があればその数値を入力してください """
		s = raw_input()
		if s == "1":
			start_limit = 0
			break
		elif s == "2":
			start_limit = 3000
			break
		elif s == "3":
			start_limit = 7000
			break
		elif s.isdigit():
			start_limit = int(s)
			break
		else:
			print "不正な入力です. もう一度入力してください\n---------------\n"
	return start_limit

def output_about_data(get_data,start_limit):

	today = datetime.date.today()
	f_name = "./sample_data/Juggler_{0}-{1}-{2}.csv".format(today.year,today.month,today.day)
	f = open(f_name,"w")

	d_key = get_data.keys()
	d_no = get_data[d_key[0]].keys()

	d_key.sort()
	d_no.sort()

	line = "setting"

	for i in d_no:
		line = line + ",{0}".format(i)
	f.write(line)
	f.write("\n")

	for i in d_key:
		line = "{0}".format(i)
		for j in d_no:
			if start_limit <= get_data[i][j].start:
				line = line + ",{0}".format(get_data[i][j].setting)
			else:
				line = line + ",{0}".format(0)
		f.write(line)
		f.write("\n")
	f.close()

def output_No_data(get_data,No):
	sql = ""


if __name__ == "__main__":
	s_time,e_time = input_date()
	all_date = get_between_day(s_time,e_time)
	get_data = get_data_from_db(all_date)#get_data[date][No]
	start_limit = input_option()
	output_about_data(get_data,start_limit)




	
			

	






