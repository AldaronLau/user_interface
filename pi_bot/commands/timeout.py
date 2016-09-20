#!/usr/bin/python3

from .command import command
from ..clock import clock

class timeout_command(command):
	def __init__(self, action, duration_ms):
		super().__init__(action)
		self._time_keeper = None
		self._duration_ms = duration_ms
	def __repr__(self):
		pass
	def begin(self):
		'''Code to execute when command has started'''
		self._time_keeper = clock()
	def execute(self):
		'''Code to execute while not command is not finished'''
		pass
	def is_finished(self):
		'''Command is finished self.duration milliseconds after self.begin() was called'''
		return self._time_keeper.current_ms() > self._duration_ms
	def terminate(self):
		'''Code to execute to finish the command'''
		pass
