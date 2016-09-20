#!/usr/bin/python3

class communications_out(object):
	'''Class tasked with handleing pi_bot wireless comms'''
	def __init__(self):
			pass
	def __repr__(self):
		pass
	def test_comms_out(self):
		'''Returns whether comms can output to the pi_bot'''
		self.send_string("Hellow World")
		
	def send_string(self, out):
		'''Ouputs info to the pi_bot'''
		print("outputing to pi_bot: " + out)
comms_out = communications_out()
