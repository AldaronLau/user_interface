#!/usr/bin/python3

import tkinter
from gui import gui
from communications import communications
from user_input import user_input
from information import information

class user_interface(object):
    def __init__(self):
        self.window = gui()
        self.user_in = user_input()
        self.window.setup_buttons(self)
        self.comms = communications()
        self.robot_info = information()
    def __repr__(self):
        pass
    def update_user_interface(self):
        self.user_in.check_joysticks()
        self.user_in.check_user_input_events()
        self.comms.handle_incoming_messages(self)
        if self.comms.test_comms():
            if self.robot_info.enable_state is \
                    self.robot_info.state_teleop_enabled:
                self.user_in.check_user_input_events()
                self.user_in.send_user_input_events()
        self.window.update_gui(self)
        self.window.root.after(16, lambda: self.update_user_interface())
    def quit_program(self):
        self.user_in.quit_input()
