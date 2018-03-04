# -*- coding: utf-8 -*-
from datetime import datetime as dt
import datetime
import time
import get_data_from_db as gd


def select_shop():#店の指定
	print "店舗の指定を行います。\nboom天神なら「１」、つかさ月隈なら「２」を入力してください。"
	shop = raw_input()
	return shop

def input_date():#日付入力 
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

	return (s_date_time,e_date_time)

def select_model(shop_No):#機種の指定
	gd.get_model(shop_No)
	r = 0
	e_model = 0
	s_model = 0
	while 1:
		print "機種の指定を行います。全台なら「all」　機種指定があるなら「select」を入力してください"
		all_or_select = raw_input()
		if all_or_select == "all":
			def __all_select():
				while 1:
					print "全機種対象にします。いいでしょうか？ (y or n)"
					y_n = raw_input()

					if y_n == "y":
						r = "all"
						break
					elif y_n =="n":
						r = 0
						break
					else:
						print "不正入力　y か nで入力してください"
				return r
			r = __all_select()

		elif all_or_select == "select":
			while 1:
				print "除く台を選ぶならe、調べる台を指定するならsを選択してください"
				e_s = raw_input()

				if e_s == "e":#除くモードの時
					print "除く台の指定を行います."
					e_model = []
					while 1:
						print "除きたい機種の番号を入力してください.終了する場合は[exit]"
						e_m = raw_input()

						if e_m.isdigit() == True:
							e_model.append(int(e_m))

						elif e_m == "exit":
							print "指定を終了します"
							break
						else:
							print "入力不正"

				elif e_s == "s":#選択モードの時
					print "選ぶ台の指定を行います."
					s_model = []
					while 1:
						print "選びたい機種の番号を入力してください.終了する場合は[exit]"
						s_m = raw_input()

						if s_m.isdigit() == True:
							s_model.append(int(s_m))

						elif s_m == "exit":
							print "指定を終了します"
							break
						else:
							print "入力不正"

				else:
					print "不正入力"

				if e_model != 0:
					#r = e_model
					break
				elif s_model != 0:
					#r = s_model
					break
		else:
			print "不正入力"


		if r != 0 or e_model != 0 or s_model != 0:
			break

	if r != 0:
		return ("all","all")
	elif e_model != 0:
		return ("except",e_model)
	elif s_model != 0:
		return ("select",s_model) 

def get_between_day(s_time,e_time):#日付の間の日を取得
	all_date = []
	end = "{0}-{1:02d}-{2:02d}".format(e_time.year,e_time.month,e_time.day)

	while 1:
		all_date.append("{0}-{1:02d}-{2:02d}".format(s_time.year,s_time.month,s_time.day))
		#print "{0}-{1:02d}-{2:02d}".format(s_time.year,s_time.month,s_time.day)
		if "{0}-{1:02d}-{2:02d}".format(s_time.year,s_time.month,s_time.day) == end:
			break
		s_time = s_time + datetime.timedelta(days=1)

	return all_date#取得するデータ選択









if __name__ == "__main__":
	s = select_shop()
	print select_model(s)
