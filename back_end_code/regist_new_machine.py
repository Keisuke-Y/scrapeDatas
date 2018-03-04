# -*- coding: utf-8 -*-
import crawler
from bs4 import BeautifulSoup
import shop_data as sd

def all_model_url(shop_No):#店の機種全部確認

	root_url = sd.Shop_data(shop_No).url

	print "機種の回収開始....."

	scraping = crawler.Crawler()
	bs = scraping.scraping(root_url)

	url_data = bs.find_all("p" , class_="p_l3 p_r3 p_t7 p_b8 fs_18")

	all_data = []
	for i in url_data:
		url =  sd.Shop_data(shop_No).root_url + i.a.get("href")
		name =  i.find("a").text
		#print name

		all_data.append((url,name))

	return all_data

def rack_url(model_url,shop_No,model_name):#店の特定機種のすべてのurl回収 return(machine_URL,machine_No,machine_name)
	print "台データの回収開始.....{0}".format(model_name.encode("utf-8"))

	scraping = crawler.Crawler()
	bs = scraping.scraping(model_url)

	root_url = sd.Shop_data(shop_No).root_url

	url_data = bs.table.find_all("a",class_="btn-base")

	all_url = []
	for i in url_data:
		No = i.string
		url =  root_url + i.get("href")
		all_url.append((url,No,model_name))

	return all_url

def all_rack_url(model_url,shop_No):#店の前代データのuRL return(machine_URL,machine_No,machine_name)
	d = []
	for machine in model_url:
		a = rack_url(machine[0],shop_No,machine[1])
		d = d + a
	return d

def get_all_machine_URL(shop_No):#return(machine_URL,machine_No,machine_name)
	machine_data = all_model_url(shop_No)
	a = all_rack_url(machine_data,shop_No)

	return a

if __name__ == "__main__":
	shop = "2"
	a=get_all_machine_URL(shop)
	

	









