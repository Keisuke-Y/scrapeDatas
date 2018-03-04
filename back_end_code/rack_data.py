# -*- coding: utf-8 -*-
import sys

class Rack_data(object):
	def __init__(self,data):
		self.date      = data["date"]
		self.name      = data["name"]
		self.No        = data["No"]
		self.BB        = data["BB"]
		self.RB        = data["RB"]
		self.ART       = data["ART"]
		self.start     = data["start"]
		self.all_start = data["all_start"]
		self.slump     = data["slump"]



