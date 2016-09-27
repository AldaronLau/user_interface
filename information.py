#!/usr/bin/python3

class information(object):
	'''Container class for pi_bot information obtained wirelessly
	
	Modified by communications.in
	Used to update remote_interface
	'''
	
	state_disabled = "DISABLED"
	state_teleop_enabled = "ENABLED_TELEOP"
	state_auto_enabled = "ENABLED_AUTO"
	
	def __init__(self):
		self.enable_state = self.state_disabled
	def __repr___(self):
		pass
