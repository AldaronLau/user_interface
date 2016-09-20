#!/usr/bin/python3

class subsystem(object):
	'''Common base class for subsystems'''
	def __init__(self):
		pass
	def __repr__(self):
		return "Subsystem: "
	def update(self, delta_ms):
		pass
