#!/usr/bin/python3

from .command import command
import copy

class operator_interface(object):
    '''Base class that interfaces between the operator and various controls'''
    
    __max_joystick_count = 5
    def __init__(self):
        self.joysticks = [joystick(i) for i in range(self.__max_joystick_count)]
    def __repr__(self):
        pass
    def joystick_button_event(self, joystick_i, button_i, event):
        self.joysticks[joystick_i].buttons[button_i].set_event(event)
    def update_button_commands(self):
        '''Updates button commands'''
        for stick in self.joysticks:
            for button in stick.buttons:
                button.update_commands()
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
        self.active_commands = []
    def __repr__(self):
        return "Joystick button " + str(self.button_number) + " is currently"
    def set_event(self, event):
        '''Sets button's event value
        
        event - event button.event is set to
        '''
        self.event = event
        if event is not self.no_event:
            self.raw_value = 1 if event is self.press_event else 0
    def add_command(self, command):
        '''Binds a command to the joystickk_button
        
        command - command object to attach
        '''
        self.commands.append(command)
    def update_commands(self):
        '''Updates button's attached commands
        
        '''
        for com in self.commands:
            if (self.event != joystick_button.no_event):
                if self.event & (com.action | com.action >> 2):
                    self.active_commands.append(copy.deepcopy(com))
                    self.active_commands[-1].begin()
        for com in self.active_commands:
            if ((not com.process()) or
                (com.action == command.while_held and
                 self.event == joystick_button.release_event) or 
                (com.action == command.while_released and
                 self.event == joystick_button.press_event)):
                com.terminate()
                self.active_commands.remove(com)
        self.event = self.no_event
class joystick_axis(object):
    '''Handler for analog operator input'''
    
    def __init__(self, axis_num):
        '''Initialize joystick_axis'''
        self.axis = axis_num
        self.raw_value = 0.0
    def __repr__(self):
        return "Axis " + str(self.axis) + " has value: " + str(self.value)
