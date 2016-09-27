#!/usr/bin/python3
import socket
from multiprocessing import Process, Queue, Lock
from information import information

class communications(object):
    '''Class that manages communications with the user interface'''
    __SERVER_NAME = ""
    __PORT = 4321
    __MAX_MESSAGE_LENGTH = 16
    def __init__(self):
        '''Initializes pi_bot server socket
        
        communications.server_socket - main communication socket
        communications.recieved_messages - multiprocess friendly list
                used to store recieved messages until they can be handled
        communications.connection - socket of the accepted line of communication
        communications.connection_lock - lock to help make
                communications.connection multiprocess frienly
        communications.client_address - address of the accepted client
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_info = (self.__SERVER_NAME, self.__PORT)
        self.recieved_messages = Queue(20)
        self.connected = False
        self.connection_lock = Lock()
        pro = lambda:self.connect_to_server()
        Process(target=pro, daemon=True).start()
    def __repr__(self):
        pass
    def test_comms(self):
        
        self.connection_lock.acquire()
        connected = False if self.connected is None else True
        self.connection_lock.release()
        return connected
    def connect_to_server(self):
        '''Attempts to connect to the server
        
        Once connected, a new process is used to monitor recieved data
        '''
        while True:
            '''Loop until a connection is found'''
            try:
                self.sock.connect(self.server_info)
            except ConnectionRefusedError:
                '''Don't break the loop because no connection was found'''
                continue
            '''Break loop because connection was not refused'''
            break
        self.connection_lock.acquire()
        self.connected = True
        self.connection_lock.release()
        
        pro = lambda:self.recieve_incoming_messages()
        Process(target=pro, daemon=True).start()
    def send_message(self, message):
        '''Attempts to send data to client'''
        print(message)
        if self.connected:
            if len(message) > self.max_message_length:
                print("Message \"" + message + "\" is to long\n")#TODO: to log file
            else:
                self.connection_lock.acquire()
                self.sock.sendall(fill_out_message(message))
                self.connection_lock.release()
        else:
            '''Does not send information because no connection has been made'''
            pass
    def recieve_incoming_messages(self):
        '''Updates communications.recieved_messages with any recieved data
        
        This is a seperate process as socket.recv() will block the program
        '''
        while True:
            message = self.sock.recv(self.__MAX_MESSAGE_LENGTH)
            if message is "":
                self.connection_lock.acquire()
                self.connected = False
                self.connection_lock.release()
                pro = lambda:self.connect_to_server()
                Process(target=pro, daemon=True).start()
                break
            self.recieved_messages.put(message)
    def handle_incoming_messages(self, ui):
        '''Called by robot to handle any data sent by the user_interface'''
        while not self.recieved_messages.empty():
            message = self.recieved_messages.get()
            print(message)
            if message is self.fill_out_message("DISABLE"):
                ui.robot_info.enable_state = information.state_disabled
            if message is self.fill_out_message("ENABLE_TELEOP"):
                ui.robot_info.enable_state = information.state_teleop_enabled
            if message is self.fill_out_message("ENABLE_AUTO"):
                ui.robot_info.enable_state = information.state_auto_enabled
            else:
                print("Unknown recieved message: \"" + message + "\"")
                #TODO: to error log file
    def fill_out_message(self, message):
        needed_characters = "_" * (self.__MAX_MESSAGE_LENGTH - len(message))
        return message + needed_characters
