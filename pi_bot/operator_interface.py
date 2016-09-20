#!/usr/bin/python3

from .commands.command import command
from .input.joystick import joystick
from .input.joystick_button import joystick_button

class operator_interface(object):
	'''Base class that interfaces between the operator and various controls'''
	
	def __init__(self):
		self.joysticks = []
	def __repr__(self):
		pass
	def joystick_button_event(self, joystick_i, button_i, event):
		self.joysticks[joystick_i].buttons[button_i].event = event
	def update_button_commands(self):
		'''Updates button commands'''
		for stick in self.joysticks:
			for button in stick.buttons:
				button.update_commands()
