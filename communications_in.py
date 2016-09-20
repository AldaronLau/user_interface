#!/usr/bin/python3

from information import pi_bot_info

class communications_in(object):
	'''Class tasked with handleing pi_bot wireless comms'''
	def __init__(self):
		input_queue = []
	def __repr__(self):
		pass
	def test_comms_in(self):
		'''Returns whether comms have been established with the pi_bot'''
		pass
	def update_information(self):
		'''Updates information based on results gotten from the pi_bot
		
		input is stored in communications_in.input_queue
		'''
		pass
comms_in = communications_in()
