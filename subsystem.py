#!/usr/bin/python3

class subsystem(object):
	'''Common base class for subsystems'''
	def __init__(self):
		self.default_function = None
	def __repr__(self):
		return "Subsystem: "
