#!/usr/bin/python3

from .operator_inputimport operator_input

class analog_input(operator_input):
	'''Handler for analog operator input'''
	def __init__(self, input_pin):
		super().__init__(self, input_pin)
	def __repr__(self):
		return "Input pin " + str(self._input_pin) +\
			" has an analog value of " + str(self.get_input())
	def get_input(self):
		'''Returns input'''
		return self.get_raw_input()
