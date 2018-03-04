# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import csv
import datetime
import sqlite3
import scipy.misc as scm

class JugglerData():
	def __init__(self,data_list):
		for c,i in enumerate(data_list):
			if i.isdigit() ==False:
				data_list[c] = 0
			else:
				data_list[c] = int(data_list[c]) 

		self.No = data_list[0]
		self.BB = data_list[1]
		self.RB = data_list[2]
		self.start = data_list[3]
		if self.start == 0:
			self.BBp = 0
			self.RBp = 0
		else:
			self.BBp = 1.0*self.BB/self.start
			self.RBp = 1.0*self.RB/self.start
		self.p1 = -1
		self.p2 = -1
		self.p3 = -1
		self.p4 = -1
		self.p5 = -1
		self.p6 = -1

def get_data(soup):
	data = {}
	a = soup.find_all("div",class_="swiper-slide")

	for counter,i in enumerate(a):
		try:
			#日にち取得
			d = a[counter].find("p",class_="date").string
			d = re.sub(r" \(.*\)","",d)
			data[d] = {}
			

			#情報収集（スペック）
			datas = a[counter].find_all("h2")
			spec_data = []
			for k in datas:
				spec_data.append(k.text)	

			#情報収集（数値的なもの）
			t = a[counter].find_all("div",class_="digitbox"or"digitbox rate")

			z = []
			data_list = []
			for c,j in enumerate(t):
				s = j.find_all("div",class_="daidigit num ll red")
				for k in s:
					w = k.text
					try:
						w = int(w)
						data_list.append(k.text)
					except ValueError:
						w = 0
						data_list.append(w)
				if len(data_list) <= 8:
					s = j.find_all("div",class_="daidigit num ll blue")
					for k in s:
						w = k.text
						try:
							w = int(w)
							data_list.append(k.text)
						except ValueError:
							w = 0
							data_list.append(w)
				if len(data_list) <= 8:
					s = j.find_all("div",class_="daidigit num s orange")
					for k in s:
						w = k.text
						try:
							w = int(w)
							data_list.append(k.text)
						except ValueError:
							w = 0
							data_list.append(w)
				if len(data_list) <= 8:
					s = j.find_all("div",class_="daidigit num s green")
					for k in s:
						w = k.text
						try:
							w = int(w)
							data_list.append(k.text)
						except ValueError:
							w = 0
							data_list.append(w)
				if len(data_list) <= 8:
					s = j.find_all("div",class_="daidigit num ss green")
					for k in s:
						q = k.text
						try:
							w = float(q[4:])
							data_list.append(w)
						except ValueError:
							w = 0
							data_list.append(w)

			for spec,count in zip(spec_data,data_list):
				data[d][spec] = count



		except AttributeError:
			pass

	return data

def get_juggler_data(url,data_name):
	html = requests.get(url).text

	bsObj = BeautifulSoup(html, "html.parser")

	#テーブルを指定
	table = bsObj.findAll("table",{"class":"standlist sorter tablesorter"})[0]
	rows = table.findAll("tr")

	csvFile = open(data_name, 'wt')
	writer = csv.writer(csvFile)

	try:
		for row in rows:
			csvRow = []
			for cell in row.findAll(['td', 'th']):
				csvRow.append(cell.get_text().encode("utf-8"))
			writer.writerow(csvRow)
	finally:
		csvFile.close()

def get_csv_all_juggler_data():
	root_url = "http://tsukasa-group.pt.teramoba2.com/tukiguma/standlist_slot/?target_date="
	bottom_url_3 = "&machine_name=%2525EF%2525BE%25258F%2525EF%2525BD%2525B2%2525EF%2525BD%2525BC%2525EF%2525BE%25259E%2525EF%2525BD%2525AC%2525EF%2525BD%2525B8%2525EF%2525BE%25259E%2525EF%2525BE%252597%2525EF%2525BD%2525B0%2525E2%252585%2525A2&kind_code=S"
	bottom_url_2 = "&machine_name=%2525E3%252583%25259E%2525E3%252582%2525A4%2525E3%252582%2525B8%2525E3%252583%2525A3%2525E3%252582%2525B0%2525E3%252583%2525A9%2525E3%252583%2525BC%2525E2%252585%2525A1&kind_code=S"
	today = datetime.date.today()
	

	for i in range(8):
		d = today - datetime.timedelta(days=i)
		date = "{0}-{1}-{2}".format('{0:02d}'.format(d.year),'{0:02d}'.format(d.month),'{0:02d}'.format(d.day))
		url = root_url+date+bottom_url_3
		file_name = "./sample_data/{0}_MyJuggler3.csv".format(date)
		get_juggler_data(url,file_name)
		url = root_url+date+bottom_url_2
		file_name = "./sample_data/{0}_MyJuggler2.csv".format(date)
		get_juggler_data(url,file_name)

def get_data_from_csv():
	today = datetime.date.today()

	data_list = {}
	for i in range(8):
		li = []
		d = today - datetime.timedelta(days=i)
		date = "{0}-{1}-{2}".format('{0:02d}'.format(d.year),'{0:02d}'.format(d.month),'{0:02d}'.format(d.day))


		file_name = "./sample_data/{0}_MyJuggler3.csv".format(date)
		f = open(file_name,"r")
		line = f.readlines()
		f.close()
		for c,l in enumerate(line):
			if c == 0:
				pass
			else:
				score = l[:-2].split(",")
				li.append(JugglerData(score))

		file_name = "./sample_data/{0}_MyJuggler2.csv".format(date)
		f = open(file_name,"r")
		line = f.readlines()
		f.close()
		for c,l in enumerate(line):
			if c == 0:
				pass
			else:
				score = l[:-2].split(",")
				li.append(JugglerData(score))
		data_list[date] = li

	return data_list

def MyJuggler_setting_persentage(d):
	reg_p = [
	0,
	1/431.2,
	1/364.1,
	1/314.3,
	1/292.6,
	1/277.7,
	1/240.9]



	for i in range(1,7):
		
		px = scm.comb(d.start,d.RB) * pow(reg_p[i],d.RB) * pow((1-reg_p[i]),(d.start-d.RB))

		if d.p1 == -1:
			d.p1 = px
		elif d.p2 == -1:
			d.p2 = px
		elif d.p3 == -1:
			d.p3 = px
		elif d.p4 == -1:
			d.p4 = px
		elif d.p5 == -1:
			d.p5 = px
		elif d.p6 == -1:
			d.p6 = px

	num = d.p1+d.p2+d.p3+d.p4+d.p5+d.p6
	if num == 6:
		d.p1 = 0
		d.p2 = 0
		d.p3 = 0
		d.p4 = 0
		d.p5 = 0
		d.p6 = 0
	else:
		d.p1 = d.p1 / num * 100
		d.p2 = d.p2 / num * 100
		d.p3 = d.p3 / num * 100
		d.p4 = d.p4 / num * 100
		d.p5 = d.p5 / num * 100
		d.p6 = d.p6 / num * 100

def MyJuggler_add_db():
	all_data = get_data_from_csv()

	date_key = all_data.keys()
	
	db = "./sample_data/Juggler.db"
	connect = sqlite3.connect(db)
	cur = connect.cursor()

	for d in date_key:
		for i in all_data[d]:
			MyJuggler_setting_persentage(i)
			sql = "INSERT INTO Juggler VALUES(?,?,?,?,?,?,?,?,?,?,?)"
			try:
				cur.execute(sql,(d,i.No,i.BB,i.RB,i.start,i.p1,i.p2,i.p3,i.p4,i.p5,i.p6))
			except sqlite3.IntegrityError:
				sql = "UPDATE Juggler SET BB=?,RB=?,start=?,p1=?,p2=?,p3=?,p4=?,p5=?,p6=? WHERE date=? and No=?"
				cur.execute(sql,(i.BB,i.RB,i.start,i.p1,i.p2,i.p3,i.p4,i.p5,i.p6,d,i.No))
	connect.commit()
	connect.close()



if __name__ == "__main__":
	get_csv_all_juggler_data()
	MyJuggler_add_db()

	
	
			















