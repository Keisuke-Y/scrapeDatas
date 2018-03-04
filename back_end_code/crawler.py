# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

class Crawler(object):
    def start_brower(self):
        self.browser = webdriver.PhantomJS() # ブラウザを操作するオブジェクトを生成

    def ajax(self, url):
        if url is not None:
            try:
                self.browser.get(url) # URLへアクセス
                print "get_html..."
            except:
                pass
        time.sleep(10)

        html_source = self.browser.page_source # アクセスしたサイトのページソースを返す
        bs_obj = BeautifulSoup(html_source,"lxml") # ページソースを引数にとり、BeautifulSoupのオブジェクトを生成

        return bs_obj
    def end_browser(self):
        self.browser.quit()#ブラウザを閉じる

    def scraping(self,url):
        html = requests.get(url).text
        bs_obj = BeautifulSoup(html,"lxml")

        return  bs_obj
