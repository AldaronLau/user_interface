#!/usr/bin/python3

from .joystick_button import joystick_button
from .joystick_axis import joystick_axis

class joystick(object):
	'''Class representing operator joystick
	
	Contains buttons, axes
	TODO: add:
			- hats
			- trackballs?
	'''
	
	__max_button_count = 25
	__max_axis_count = 20
	def __init__(self, joy_index):
		'''Initializes joystick
		
		
		'''
		self.joystick_index = joy_index
		self.buttons = []
		for button_i in range(self.__max_button_count):
			self.buttons.append(joystick_button(button_i))
		
		self.axes = []
		for axis_i in range(self.__max_axis_count):
			self.axes.append(joystick_axis(axis_i))
	def button_event(self, button_num, event):
		'''Sets event for a button corresponding to an operator event'''
		self.buttons[button_num].set_event(event)
	def __repr__(self):
		pass
