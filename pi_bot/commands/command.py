#!/usr/bin/python3

class command(object):
	'''Base class for commands that can be triggered by operator input'''
	
	'''Affects flow when a value is passed as 'event_flag' in command.process()'''
	when_released = 0b000
	when_pressed = 0b001
	while_released = 0b010
	while_held = 0b100
	'''
	when_released - command.begin() is called when release_event is passed
	when_pressed - command.begin() is called when press_event is passed
	while_released - command.begin() is called when release_event is passed
		and command.terminate() is called when press_event is passed
	while_held - command.begin() is called when press_event is passed
		and command.terminate() is called when release_event is passed
	'''
	
	def __init__(self, action):
		'''Initialize command class
		
		self._action - determines when command.begin() is called
			and may affect when command.terminate() is called
		self._event_listen - used to determine if the command ends prematurely
		self._active - if 
		'''
		self._action = action
		self._event_listen = \
				(command.while_held | command.while_released) & action
		self._active = 0
	def __repr__(self):
		return "Command " + self.__class__.__name__ + " is " + ("", "not")[self._active] + " active"
	def begin(self):
		'''Code to execute when command has started'''
		pass
	def execute(self):
		'''Code to execute while not command is not finished'''
		pass
	def is_finished(self):
		'''Check if command should finish'''
		pass
	def terminate(self):
		'''Code to execute to finish the command'''
		pass
	def process(self, event_flag):
		'''Executes, and tests if command should terminate
		
		The command will adjust self.active if the appropriate flag
			is passed depending on self.action
		
		The command will terminate with 1 of 2 conditions:
			1. Overridden self.is_finished() returns 1
			2. conditions are met with
				self._event_listen being while_held or while_released
		'''
		if (event_flag != 0b10) and (not self._active):
			self._active = event_flag == (self._action | self._action >> 2)
			if self._active:
				self.begin()
		if self._active:
			self.execute()
			if self.is_finished() or ((self._event_listen & (~((event_flag + 1) << 1)) \
					) if event_flag is not 0b10 else 0):
				self.terminate()
				self._active = 0
			
