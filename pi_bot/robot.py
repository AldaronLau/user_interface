#!/usr/bin/python3

from .clock import clock
from .subsystem import subsystem

class robot(object):
	'''General robot class'''
	
	__state_disabled = 0
	__state_teleop_enabled = 1
	__state_auto_enabled = 2
	
	def __init__(self):
		self.subsystems = []
		self._enable_state = robot.__state_disabled
	def __repr__(self):
		if not self.subsystems:
			return "This robot had no subsystems attached"
		details = str(self.subsystems[0])
		for system in self.subsystems[1:]:
			details += "\n" + str(system)
		return details
	def update(self):
		if self._enable_state is robot.__state_disabled:
			return 0
		for system in self.subsystems:
			system.update()
		if self._enable_state is robot.__state_teleop_enabled:
			self.teleop_periodic()
		elif self._enable_state is robot.__state_auto_enabled:
			self.auto_periodic()
	def enable_teleop(self):
		self.teleop_init()
		self._enable_state = robot.__state_teleop_enabled
	def enable_auto(self):
		self.auto_init()
		self._enable_state = robot.__state_auto_enabled
	def disable(self):
		self._enable_state = robot.__state_disabled
	def teleop_init(self):
		pass
	def teleop_periodic(self):
		pass
	def auto_init(self):
		pass
	def auto_periodic(self):
		pass
