#!/usr/bin/python3

import tkinter
from gui import gui
from communications_in import comms_in
from user_input import user_input

class user_interface(object):
	def __init__(self):
		self.window = gui()
		self.user_in = user_input()
		self.window.setup_buttons(self.user_in)
	def __repr__(self):
		pass
	def update_user_interface(self):
		self.user_in.check_joysticks()
		
		#if enabled
		self.user_in.check_user_input_events()
		self.user_in.send_user_input_events()
		#end if enabled
		self.window.update_gui(self.user_in)
		self.window.root.after(16, lambda: self.update_user_interface())
ui = user_interface()
