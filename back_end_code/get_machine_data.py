# -*- coding: utf-8 -*-
import rack_data as rd
import shop_data as sd
import regist_new_machine as mu
import crawler
import time
from bs4 import BeautifulSoup
import json
import sqlite3
import datetime

"""
def select_shop():#店の指定
	print "店舗の指定を行います。\nboom天神なら「１」、つかさ月隈なら「２」を入力してください。"
	shop = raw_input()
	return shop
"""

def get_rack_data(rack_url,rack_No,Crawler):#スランプデータの回収
	print rack_No
	bs = Crawler.ajax(rack_url)
	print "open_URL..."

	def __get_srump(bs,rack_url):#八日間のスランプデータ取得 return list（上から新しい）
		while 1:
			try:
				slump_ = []
				for i in range(8):#八日間データ取得
					day_data = {}
					No = 8-i
					class_name = "linechart_slump_{0}".format(No)

					slump = bs.find("input", {"name":class_name})
					slump_json = json.loads(slump.get("value"))
					#スランプデータの取得
					slump_graph = slump_json["slumpData"]

					start_time =  int(slump_json["hallDefine"]["start_time"])
					end_time = int(slump_json["hallDefine"]["end_time"])

					for j in range(start_time-1,end_time):

						#時間の設定
						timer = 1.0 * j / 2
						if timer * int(timer) == timer*timer:#時間が整数ならINTへ
							timer = int(timer)
						
						for k in slump_graph:
							if k[u"x"] == timer:
								day_data[timer] = int(k[u"y"])
								break
							else:
								a = timer - 0.5
								if a * int(a) == a*a:
									a = int(a)
								day_data[timer] = day_data[a]
					day_data = json.dumps(day_data,ensure_ascii=False)
					slump_.append(day_data)
				break

			except AttributeError:
				print "caused_error..."
				time.sleep(100)
				bs = Crawler.ajax(rack_url)

		return slump_
	def __get_rack_digit(bs):#８日間の数値データ取得
		rack_data = bs.find("div",class_="digitPanel history")
		rack_day = rack_data.find_all("div",class_="swiper-slide")

		all_rack_digit_data = []
		for i in rack_day:
			def __get_date(bs):#日付取得
				date = bs.find("p",class_="date").string
				l = len(date)
				date = date[:10-l]
				return date
			def __get_BB(bs):#BB取得
				BB_outer = bs.find("div",class_="leftBox bb dailist_boxheight_slotbb")
				BB_inser = BB_outer.find("div",class_="daidigit num ll big")
				BB = BB_inser.string
				try:
					BB = int(BB)
				except TypeError:
					BB = 0
				return BB
			def __get_RB(bs):#RB取得
				RB_outer = bs.find("div",class_="centerBox rb")
				RB_inser = RB_outer.find("div",class_="daidigit num ll reg")
				RB = RB_inser.string
				try:
					RB = int(RB)
				except TypeError:
					RB = 0
				return RB
			def __get_ART(bs):#ART取得
				ART_outer = bs.find("div",class_="rightBox art dailistnum_boxheight_slotart")
				ART_inser = ART_outer.find("div",class_="daidigit num s art")
				ART = ART_inser.string
				try:
					ART = int(ART)
				except TypeError:
					ART = 0
				return ART
			def __get_start(bs):#現在のスタート
				start_outer = bs.find("div",class_="tables doubleBox topBorder dailist_boxheight_slot")
				start_inner = start_outer.find("div",class_="daidigit num s green")
				start = start_inner.string
				try:
					start = int(start)
				except TypeError:
					start = 0
				return start
			def __get_all_start(bs):#総回転数
				all_start_outer = bs.find("div",class_="right soukaiten")
				all_start_inner = all_start_outer.find("div",class_="daidigit num s green")
				all_start = all_start_inner.string
				try:
					all_start = int(all_start)
				except TypeError:
					all_start = 0
				return all_start
			def __rack_digit_data(bs):#全数値データ取得
				rack_digit_data = {}
				rack_digit_data["date"]      = __get_date(bs)
				rack_digit_data["BB"]        = __get_BB(bs)
				rack_digit_data["RB"]        = __get_RB(bs)
				rack_digit_data["ART"]       = __get_ART(bs)
				rack_digit_data["start"]     = __get_start(bs)
				rack_digit_data["all_start"] = __get_all_start(bs)
		
				return rack_digit_data


			all_rack_digit_data.append(__rack_digit_data(i))

		leng = len(all_rack_digit_data)
		sorded_all_rack_digit_data = []
		for i in range(leng):
			sorded_all_rack_digit_data.append(all_rack_digit_data[leng-i-1])

		return sorded_all_rack_digit_data

	all_slump = __get_srump(bs,rack_url)
	all_digit = __get_rack_digit(bs)

	date = datetime.date.today()

	name_list = []
	for i in range(8):
		day = date - datetime.timedelta(days=i)
		str_day = u"{0}-{1:02d}-{2:02d}".format(day.year,day.month,day.day)
		url = rack_url + u"&target_date="+str_day

		soup = Crawler.scraping(url)
		name = soup.find("h1",class_="st01 title").string
		name_list.append(name)
		print name
		time.sleep(3)

		

	all_data = []
	for i,j,k in zip(all_slump,all_digit,name_list):
		d = j
		d["slump"] = i
		d["No"] = rack_No
		d["name"] = k
		all_data.append(rd.Rack_data(d))
	return all_data

def regist_all_data(shop_No):#データの登録
	db = "./DB/{0}.db".format(sd.Shop_data(shop_No).name)
	connect = sqlite3.connect(db)
	cur = connect.cursor()

	sql = """CREATE TABLE data (
			day text,
			model text,
			machine_No int,
			BB int,
			RB int,
			ART int,
			start int,
			all_start int,
			slump text,
			PRIMARY KEY(day,machine_No)) """
	try:
		cur.execute(sql)
	except sqlite3.OperationalError:
		pass
	
	all_machine_URL = mu.get_all_machine_URL(shop_No)#(machine_URL,machine_No,machine_name)
	print "差枚データ、BBデータ回収開始"
	scraping = crawler.Crawler()
	scraping.start_brower()
	for i in all_machine_URL:
		data = get_rack_data(i[0],i[1],scraping)
		for j in data:
			sql = "INSERT INTO data VALUES(?,?,?,?,?,?,?,?,?)"
			try:
				cur.execute(sql,(j.date,j.name,j.No,j.BB,j.RB,j.ART,j.start,j.all_start,j.slump))
			except sqlite3.IntegrityError:
				sql = "UPDATE data SET model=?,BB=?,RB=?,ART=?,start=?,all_start=?,slump=? WHERE day = ? and machine_No = ?"
				cur.execute(sql,(j.name,j.BB,j.RB,j.ART,j.start,j.all_start,j.slump,j.date,j.No))
		connect.commit()
	scraping.end_browser()
	connect.close()

def judge_get_data(shop_No):
	get_flg = True
	day = datetime.date.today()
	day_string = u"{0}/{1:02d}/{2:02d}".format(day.year,day.month,day.day)
	db = "./DB/{0}.db".format(sd.Shop_data(shop_No).name)
	connect = sqlite3.connect(db)
	cur = connect.cursor()

	max_day = 0
	sql = "SELECT max(day) FROM data"
	cur.execute(sql)
	for i in cur.fetchall():
		max_day = i[0]

	if max_day == day_string:
		get_flg = False

	return get_flg

def roop_func(shop_count):
	while 1:
		s_time = datetime.date.today()
		for i in range(1,shop_count):
			shop_No = str(i)
			get_flg = judge_get_data(shop_No)
			if get_flg == True:
				regist_all_data(shop_No)
		e_time = datetime.date.today()

		if s_time.day == e_time.day:
			time.sleep(60*60)

if __name__ == "__main__":
	shop_count = 11
	roop_func(shop_count)

	
	






