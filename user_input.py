#!/usr/bin/python3

import tkinter
import pygame
from pygame.locals import JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP
from communications import communications
from information import information

class user_input(object):
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joysticks = []
        self.check_joysticks()
        self.events = []
        self.check_user_input = 1
        self.reset_button_text = tkinter.StringVar()
        self.reset_button_text.set("Reset User Input")
    def __repr__(self):
        '''Returns a string that represents user_input'''
        rep = ""
        for stick in self.joysticks:
            rep+=str(stick.get_id())+" : "+stick.get_name()+"\n"
            rep+="\tAxes:\n"
            for axis_i in range(stick.get_numaxes()):
                rep+="\t"+str(axis_i)+" : "+str(stick.get_axis(axis_i))+"\n"
            rep+="\tButtons:\n"
            for button_i in range(stick.get_numbuttons()):
                rep+="\t"+str(button_i)+" : "+str(stick.get_button(button_i))+"\n"
            rep+="\n"
        return rep
    def pause_user_input(self):
        self.check_user_input = 0
    def unpause_user_input(self):
        self.check_user_input = 1
    def reset_user_input(self, ui, state=0):
        if not self.check_user_input and state is 0:
            return 0
        if state == 0:
           if ui.robot_info.enable_state == information.state_disabled:
                self.check_user_input = False
                self.reset_button_text.set("Resetting")
                ui.window.root.after(500, lambda : self.reset_user_input(ui, 1))
        elif state == 1:
            ui.window.root.after(500, lambda : self.reset_user_input(ui, 2))
            self.reset_button_text.set("Resetting.")
        elif state == 2:
            ui.window.root.after(500, lambda : self.reset_user_input(ui, 3))
            self.reset_button_text.set("Resetting..")
        elif state == 3:
            ui.window.root.after(500, lambda : self.reset_user_input(ui, 4))
            self.reset_button_text.set("Resetting...")
        elif state == 4:
            self.reset_button_text.set("Reset User Input")
            self.check_user_input = True
        pygame.joystick.quit()
        pygame.joystick.init()
        self.check_joysticks()
    def check_joysticks(self):
        '''Checks for changes in the available user controls'''
        self.num_joysticks_on_enable = pygame.joystick.get_count()
        self.joysticks = [pygame.joystick.Joystick(x) for \
                x in range(self.num_joysticks_on_enable)]
        for stick in self.joysticks:
            if not stick.get_init():
                stick.init()
    def joystick_active(self, joystick_i):
        '''Retruns 1 if any button on the joystick is pressed down
        
        Returns 0 otherwise
        '''
        joy = pygame.joystick.Joystick(joystick_i)
        for button_i in range(joy.get_numbuttons()):
            if joy.get_button(button_i):
                return 1
        return 0
    def check_user_input_events(self):
        '''Checks user input events and stores events in user_input.events
        Example event string
        
        Event string is made up of 4 parts:
        1. joystick number: ...
        2. event type: a - axis or b - button
        3. event type number: _th axis, _th button
        4. value of event: axis pos, 1-button press 0-button release
        
        Examples:
        joystick 1, button, button 2, release	JOY:1:b:2:0:
        joystick 6, axis, axis 1, 0.7071  	JOY:6:a:1:0.7071:
        joystick 3, button, button 5, press  	JOY:3:b:5:1:
        '''
        for event in pygame.event.get():
            event_string = "JOY:" + str(event.joy)
            if event.type == JOYAXISMOTION:
                event_string += ":a:"+str(event.axis)+":"+str(event.value)+":"
            elif event.type == JOYBUTTONDOWN:
                event_string += ":b:" + str(event.button) + ":1:"
            elif event.type == JOYBUTTONUP:
                event_string += ":b:" + str(event.button) + ":0:"
            else:
                continue
        self.events.append(event_string)
        print(event_string + "\n")
    def send_user_input_events(self, ui):
        '''Sends events in user_input.events to the pi_bot
        
        Assumes user_input.check_user_input() was called
        following the last call to user_input.send_user_input_events()
        '''
        #comms_out.send_string("output")
        for event in self.events:
            ui.comms.send_message(self.events)
        self.clear_user_input_events()
    def clear_user_input_events(self):
        '''Deletes all event strings from the string array'''
        del self.events[:]
