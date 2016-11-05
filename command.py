#!/usr/bin/python3

from .clock import clock

class command(object):
        '''Base class for commands that can be triggered by operator input'''

        '''Affects flow when button event happens'''
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
                self.action = action
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
        def process(self):
                '''Executes, and tests if command should terminate
                '''
                self.execute()
                if self.is_finished():
                        return False
                else:
                        return True
class timeout_command(command):
        def __init__(self, action, duration_ms):
                super().__init__(action)
                self._time_keeper = clock()
                self._duration_ms = duration_ms
        def __repr__(self):
                pass
        def begin(self):
                '''Code to execute when command has started'''
                self._time_keeper = clock()
                self._time_keeper.start()
        def execute(self):
                '''Code to execute while not command is not finished'''
                pass
        def is_finished(self):
                '''Command after self.duration milliseconds'''
                return self._time_keeper.current_ms() > self._duration_ms
        def terminate(self):
                '''Code to execute to finish the command'''
                self.__time_keeper.stop()
