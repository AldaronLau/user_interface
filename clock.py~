#!/usr/bin/python3
import datetime
class clock(object):
	'''Object which keeps track of time (in milliseconds) since it's creation'''
	def __init__(self):
		self.__starting_datetime = datetime.datetime.now()
		self._last_advance = 0.0
		self._delta_ms = 0.0
	def __repr__(self):
		'''Returns string which tells current lifetime of the clock'''
		return "The clock is currently at " + str(self.current_ms()) + " milliseconds"
	def current_ms(self):
		'''Returns milliseconds since the clock was created'''
		dt = datetime.datetime.now() - self.__starting_datetime
		return (dt.days * 86400000.0) + (dt.seconds * 1000.0) + (dt.microseconds / 1000.0)
	def advance(self):
		'''Advances the clock, returning the time (in milliseconds) since the last call'''
		self._delta_ms = self.current_ms() - self._last_advance
		self._last_advance = self._last_advance + self._delta_ms
		return self._delta_ms
		
