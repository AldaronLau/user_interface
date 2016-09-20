#!/usr/bin/python3

from ..commands.command import command

class joystick_button(object):
	'''Handler for digital operator input'''
	
	'''Flags for operator input event'''
	release_event = 0b00
	press_event = 0b01
	no_event = 0b10
	'''
	release_event - flag used when digital input goes from 1 ~~> 0
	press_event - flag used when digital input goes from 0 ~~> 1
	no_event - flag used when no digital input event has occurred
	'''
	
	def __init__(self, button_num):
		'''Initialize joystick_button
		
		self.raw_value - 1 if the corresponding button is pressed
		self.button_num - button number corresponding to operator's controller
		self.event - event sent from operator_interface
			if no event has occurred, is valued self.no_event
		self.commands - list of commands attached to this button
		'''
		self.raw_value = 0
		self.button_number = button_num
		self.event = self.no_event
		self.commands = []
	def __repr__(self):
		pass#return "Joystick button " + str(self.button_number) + " is currently"
	def set_event(self, event):
		'''Sets button's event value
		
		event - event button>event is set to
		'''
		self.event = event
		if event is not self.no_event:
			self.raw_value = 1 if event is press_event else 0
	def add_command(self, command):
		'''Binds a command to the joystickk_button
		
		command - command object to attach
		'''
		self.commands.append(command)
	def update_commands(self):
		'''Updates button's attached commands
		
		passes joystick_button.event
		'''
		for command in self.commands:
			command.process(self.event)
		self.event = self.no_event
