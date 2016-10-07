#!/usr/bin/python3

from .clock import clock
from .subsystem import subsystem
from .communications import communications

class robot(object):
    '''General robot class'''
    __state_disabled = 0
    __state_teleop_enabled = 1
    __state_auto_enabled = 2
    def __init__(self):
        self._subsystems = []
        self._enable_state = robot.__state_disabled
        self.oi = None
        self.robot_map = None
        self.comms = communications()
    def __repr__(self):
        if not self.subsystems:
            return "This robot had no subsystems attached"
        details = str(self.subsystems[0])
        for system in self.subsystems[1:]:
            details += "\n" + str(system)
        return details
    def update(self):
        if not self.comms.get_client():
            self.disable()
        self.comms.handle_incoming_messages(self)
        if self._enable_state is robot.__state_disabled:
            return 0
        self.oi.update_button_commands()
        for system in self._subsystems:
            system.update()
        if self._enable_state is robot.__state_disabled:
            if not self.comms.test_comms():
                self.disable()
        elif self._enable_state is robot.__state_teleop_enabled:
            print("running teleop per")
            self.teleop_periodic()
        elif self._enable_state is robot.__state_auto_enabled:
            print("running auto per")
            self.auto_periodic()
    def enable_teleop(self):
        self.teleop_init()
        self._enable_state = robot.__state_teleop_enabled
        self.comms.send_message("ENABLE_TELEOP")
    def enable_auto(self):
        self.auto_init()
        self._enable_state = robot.__state_auto_enabled
        self.comms.send_message("ENABLE_AUTO")
    def disable(self):
        self._enable_state = robot.__state_disabled
        self.comms.send_message("DISABLE")
    def teleop_init(self):
        pass
    def teleop_periodic(self):
        pass
    def auto_init(self):
        pass
    def auto_periodic(self):
        pass
    def add_subsystem(self, system):
        self._subsystems.append(system)
