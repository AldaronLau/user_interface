#!/usr/bin/python3

import tkinter
from tkinter import font
import pygame
from information import information
from communications import communications

class gui(object):
    '''Class to handle communicating between the GUI'''
    
    __interface_name = "pi_bot - remote display"
    __interface_size = "600x400"
    
    __teleop_selection = 0
    __auto_selection = 1
    __test_selection = 2
    __enable_mode_options = ["", "", ""]
    __enable_mode_options[__teleop_selection] = "TELEOP"
    __enable_mode_options[__auto_selection] = "AUTO"
    __enable_mode_options[__test_selection] = "TEST"
    
    __enable_button = 0
    __disable_button = 1

    __max_joystick_count = 4
    
    def __init__(self, ):
        '''Create GUI'''
        self.root = tkinter.Tk()
        self.root.title(self.__interface_name)
        self.root.geometry(self.__interface_size)
        self.root.configure(background = "#555555")
    def setup_buttons(self, ui):
        '''Buttons to select which enable state to enable when ENABLE is pressed'''
        self.enable_mode_buttons = []
        self.enable_mode_options_font = font.Font(family="Helvetica", size=10, weight="bold")
        for option in range(len(self.__enable_mode_options)):
            enable_mode_button = tkinter.Button(self.root, \
                    text=self.__enable_mode_options[option], \
                    bg="#555555", fg="#eeeeee", \
                    activebackground="#555555", activeforeground="#eeeeee", \
                    highlightthickness=1.5, \
                    highlightbackground="#333333", \
                    borderwidth=0, anchor="w", \
                    width=20, height=1, \
                    font=self.enable_mode_options_font, \
                    command=lambda option=option: self.select_enable_mode(option))
            self.enable_mode_buttons.append(enable_mode_button)
            self.enable_mode_buttons[-1].pack()
        self.selected_enable_mode = self.__teleop_selection
        
        '''Buttons to enable/disable the pi_bot
        
        Shows if the pi_bot is currently enabled
        '''
        self.enable_status_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.enable_buttons = []
        for index in range(2):
            enable_button = tkinter.Button(self.root, \
                    text=("ENABLE", "DISABLE")[index], \
                    font=self.enable_status_font, \
                    highlightthickness=1.5, \
                    highlightbackground="#333333", \
                    borderwidth=0, \
                    width=7, height=1, \
                    bg="#555555", activebackground="#555555", \
                    fg=("#009900", "#990000")[index], \
                    activeforeground=("#009900", "#990000")[index], \
                    command=(lambda: self.enable_pi_bot(ui), \
                    lambda: self.disable_pi_bot(ui))[index])
            self.enable_buttons.append(enable_button)
            self.enable_buttons[-1].pack()
            
        '''Joystick indicators'''
        self.joystick_labels = []
        joystick_label_font = font.Font(family="Helvetica", size=10, weight="bold")
        for joystick_i in range(self.__max_joystick_count):
            joystick_label = tkinter.Label(font=joystick_label_font, \
                    highlightbackground="#333333", \
                    highlightthickness=1, \
                    width=65, height=2, \
                    bg="#555555", fg="#eeeeee", \
                    activebackground="#555555", activeforeground="#eeeeee")
            self.joystick_labels.append(joystick_label)
            self.joystick_labels[-1].pack()

        '''Joystick reset button'''
        self.joystick_reset_button = tkinter.Button( \
                textvariable=ui.user_in.reset_button_text, \
                command=lambda : ui.user_in.reset_user_input(ui))
        self.joystick_reset_button.pack()
    def __repr__(self):
        pass
    def update_gui(self, ui):
        '''Updates various gui elements
        
        Updates based on stored interface values
        and information obtained from the pi_bot via communications_in
        '''
        
        for option in range(len(self.__enable_mode_options)):
            if option == self.selected_enable_mode:
                self.enable_mode_buttons[option].configure(bg="#333333", \
                        activebackground="#333333")
            else:
                self.enable_mode_buttons[option].configure(bg="#555555", \
                        activebackground="#555555")
        
        '''Update various gui elements based on if the pi_bot is enabled'''
        if ui.robot_info.enable_state != information.state_disabled:
            self.enable_buttons[self.__enable_button].configure( \
                    bg="#333333", \
                    activebackground="#333333")
            self.enable_buttons[self.__disable_button].configure( \
                    bg="#555555", \
                    activebackground="#555555")
        else:
            self.enable_buttons[self.__enable_button].configure( \
                    bg="#555555", \
        	    activebackground="#555555")
            self.enable_buttons[self.__disable_button].configure( \
                    bg="#333333", \
                    activebackground="#333333")
            
        '''Update gui representation of the joysticks'''
        if ui.user_in.check_user_input == 1:
            ui.user_in.check_joysticks()
            for joystick_i in range(pygame.joystick.get_count()):
                active_joy = ui.user_in.joystick_active(joystick_i)
                self.joystick_labels[joystick_i].configure( \
                        text=str(joystick_i) + ": " + \
                        pygame.joystick.Joystick(joystick_i).get_name(), \
                        bg=("#555555", "#333333")[active_joy], \
                        fg=("#eeeeee", "#33ee33")[active_joy], \
                        activebackground=("#555555", "#333333")[active_joy], \
                        activeforeground=("#eeeeee", "#33ee33")[active_joy])
            for joystick_i in range(pygame.joystick.get_count(), \
                    self.__max_joystick_count):
                self.joystick_labels[joystick_i].configure( \
                        text=str(joystick_i) + ": no joystick", \
                        bg="#555555", \
                        fg="#eeeeee", \
                        activebackground="#555555", \
                        activeforeground="#eeeeee")
        else:
            for joystick_i in range(self.__max_joystick_count):
                self.joystick_labels[joystick_i].configure( \
                        text=str(joystick_i) + ": Resetting User Input", \
                        bg="#555555", \
                        fg="#eeeeee", \
                        activebackground="#555555", \
                        activeforeground="#eeeeee")
    def select_enable_mode(self, enable_mode):
        '''Select mode to enable if ENABLE is pressed
        
        Options are:
        TELEOP, AUTO, TEST
        '''
        self.selected_enable_mode = enable_mode
    def enable_pi_bot(self, ui):
        '''Tells comms_out to enable the robot in the selected mode'''
        ui.comms.send_message("ENABLE_" + \
                self.__enable_mode_options[self.selected_enable_mode])
    def disable_pi_bot(self, ui):
        '''Tells comms_out to disable the robot regardless of selected mode'''
        ui.comms.send_message("DISABLE")
