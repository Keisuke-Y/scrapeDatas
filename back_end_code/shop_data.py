# -*- coding: utf-8 -*-


class Shop_data(object):
	def __init__(self,shop):
		if shop == "1":
			self.url = "http://boom-rocky.pt.teramoba2.com/boomtengin/rack_info_kt/?kind_code=G"
			self.root_url = "http://boom-rocky.pt.teramoba2.com"
			self.name = "boom_tenjin"
		elif shop == "2":
			self.url = "http://tsukasa-group.pt.teramoba2.com/tukiguma/rack_info_kt/?kind_code=S"
			self.root_url = "http://tsukasa-group.pt.teramoba2.com"
			self.name = "tsukasa_tsukiguma"
		elif shop == "3":
			self.url = "http://face-group.pt.teramoba2.com/hakata/rack_info_kt/?kind_code=G"
			self.root_url = "http://tsukasa-group.pt.teramoba2.com"
			self.name = "face800"
		elif shop == "4":
			self.url = "http://king.pt.teramoba2.com/honten/rack_info_kt/?kind_code=G"
			self.root_url = "http://king.pt.teramoba2.com"
			self.name ="king_honten"
		elif shop == "5":
			self.url = "http://nobuta.pt.teramoba2.com/hakata/rack_info_kt/?kind_code=G"
			self.root_url = "http://nobuta.pt.teramoba2.com"
			self.name = "hakata_123"
		elif shop == "6":
			self.url = "http://plaza-grp.pt.teramoba2.com/honten2/rack_info_kt/?kind_code=G"
			self.root_url = "http://plaza-grp.pt.teramoba2.com"
			self.name = "plaza_2"
		elif shop == "7":
			self.url = "http://plaza-grp.pt.teramoba2.com/plaza3/rack_info_kt/?kind_code=G"
			self.root_url = "http://plaza-grp.pt.teramoba2.com"
			self.name = "plaza_3"
		elif shop == "8":
			self.url = "http://plaza-grp.pt.teramoba2.com/akasaka/rack_info_kt/?kind_code=G"
			self.root_url = "http://plaza-grp.pt.teramoba2.com"
			self.name = "plaza_akasaka"
		elif shop == "9":
			self.url = "http://plaza-grp.pt.teramoba2.com/hakata/rack_info_kt/?kind_code=G"
			self.root_url = "http://plaza-grp.pt.teramoba2.com"
			self.name = "plaza_hakata"
		elif shop == "10":
			self.url = "http://eagle.pt.teramoba2.com/dazaihu/rack_info_kt/?kind_code=1"
			self.root_url = "http://eagle.pt.teramoba2.com"
			self.name = "eagle_dazaifu"
		elif shop == "11":
			self.url = "http://beam-group.pt.teramoba2.com/hl-102/rack_info_kt/?kind_code=C"
			self.root_url = "http://beam-group.pt.teramoba2.com"
			self.name = "BEAM_by_HIKARI"

		###########################################
		#ここにコード追加で他店舗も同サイト様式なら処理可能#
		###########################################

		else:
			sys.exit("不正入力のため終了します。")
