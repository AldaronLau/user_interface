#!/usr/bin/python3
import socket
from multiprocessing import Process, Queue, Lock
class communications(object):
    '''Class that manages communications with the user interface'''
    __SERVER_NAME = "127.0.0.1"
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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_info = (self.__SERVER_NAME, self.__PORT)
        self.server_socket.bind(server_info)
        self.server_socket.listen(1)
        self.recieved_messages = Queue(10)

        self.connection = None
        self.client_address = None
        self.connection_lock = Lock()
        pro = lambda:self.connect_to_user()
        Process(target=pro, daemon=True).start()
    def __repr__(self):
        pass
    def test_comms(self):
        
        self.connection_lock.acquire()
        connected = False if self.connection is None else True
        self.connection_lock.release()
        return connected
    def connect_to_user(self):
        '''Waits for a client to connect to the pi_bot
        
        Once connected, a new process is used to monitor recieved data
        '''
        connection, self.client_address = self.server_socket.accept()
        self.connection_lock.acquire()
        self.connection = connection
        self.connection_lock.release()
        
        pro = lambda:self.recieve_incoming_messages()
        Process(target=pro, daemon=True).start()
    def send_message(self, message):
        '''Attempts to send data to client'''
        if self.connection is not None:
            if len(message) > self.max_message_length:
                print("Message \"" + message + "\" is to long\n")#TODO: to log file
            else:
                self.connection_lock.acquire()
                self.connection.sendall(fill_out_message(message))
                self.connection_lock.release()
        else:
            '''Does not send information because no connection has been made'''
            pass
    def recieve_incoming_messages(self):
        '''Updates communications.recieved_messages with any recieved data
        
        This is a seperate process as socket.recv() will block the program
        '''
        while True:
            message = self.connection.recv(self.__MAX_MESSAGE_LENGTH)
            if message is "":
                self.connection_lock.acquire()
                self.connection = None
                self.connection_lock.release()
                pro = lambda:self.connect_to_user()
                Process(target=pro, daemon=True).start()
                break
            self.recieved_messages.put(message)
    def handle_incoming_messages(self, bot):
        '''Called by robot to handle any data sent by the user_interface'''
       # print("handleing messages")
        while not self.recieved_messages.empty():
            message = self.recieved_messages.get()
            if message is fill_out_message("DISABLE"):
                bot.disable()
            elif message is fill_out_message("ENABLE_TELEOP"):
                bot.enable_teleop()
            elif message is fill_out_message("ENABLE_AUTO"):
                bot.enable_auto()
            elif message[:3] is "JOY":
                '''Handle joystick event'''
                pass
            else:
                print("Unknown recieved message: \"" + message + "\"")#TODO: to error log file
def fill_out_message(message):
    needed_characters = "_" * (self.__MAX_MESSAGE_LENGTH - len(message))
    return message + needed_characters
