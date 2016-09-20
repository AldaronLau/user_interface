#!/usr/bin/python3

from ..commands.command import command

class joystick_axis(object):
	'''Handler for analog operator input'''
	
	def __init__(self, axis_num):
		'''Initialize joystick_axis'''
		self.axis = axis_num
		self.raw_value = 0.0
	def __repr__(self):
		return "Axis " + str(self.axis) + " has value: " + str(self.value)
