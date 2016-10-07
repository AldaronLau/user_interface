#!/usr/bin/python3
import socket
from multiprocessing import Process, Queue, Pipe
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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.__SERVER_NAME, self.__PORT))
        self.server_socket.listen(1)
        self.recieved_messages = Queue(10)
        self.conn_recv, self.conn_send = Pipe(True)
        self.client = None
        pro = lambda:self.connect_to_user(self.conn_send)
        Process(target=pro, daemon=True).start()
    def __repr__(self):
        pass
    def get_client(self):
        if self.conn_recv.poll():
            self.client = self.conn_recv.recv()
        return self.client
    def connect_to_user(self, conn_send):
        '''Waits for a client to connect to the pi_bot
        
        Once connected, a new process is used to monitor recieved data
        '''
        try:
            client, address = self.server_socket.accept()
        except BaseException as error:
            self.server_socket.shutdown(1)
            self.server_socket.close()
            raise error
        conn_send.send(client)
        
        '''Updates communications.recieved_messages with any recieved data
        
        This is a seperate process as socket.recv() will block the program
        '''
        while True:
            print("waiting for message...")
            try:
                bytes = client.recv(self.__MAX_MESSAGE_LENGTH)
            except BaseException as error:
                self.server_socket.shutdown(1)
                self.server_socket.close()
                raise error
            message = bytes.decode('utf-8')
            if message is "":
                conn_send.send(None)
                self.connect_to_user(conn_send)
                return
            self.recieved_messages.put(message)
    def send_message(self, message):
        '''Attempts to send data to client'''
        if self.get_client():
            if len(message) > self.__MAX_MESSAGE_LENGTH:
                print("Message \"" + message + "\" is to long\n")#TODO: to log file
            else:
                bytes = self.fill_out_message(message).encode('utf-8')
                self.client.sendall(bytes)
        else:
            '''Does not send information because no connection has been made'''
            pass
    def handle_incoming_messages(self, bot):
        '''Called by robot to handle any data sent by the user_interface'''
        self.get_client()
        while not self.recieved_messages.empty():
            message = self.recieved_messages.get()
            print("recieved message : " + message)
            if message == self.fill_out_message("DISABLE"):
                bot.disable()
            elif message == self.fill_out_message("ENABLE_TELEOP"):
                bot.enable_teleop()
            elif message == self.fill_out_message("ENABLE_AUTO"):
                bot.enable_auto()
            elif message[:3] == "JOY":
                '''Handle joystick event'''
                pass
            else:
                print("Unknown recieved message: \"" + message + "\"")#TODO: to error log file
    def fill_out_message(self, message):
        needed_characters = "_" * (self.__MAX_MESSAGE_LENGTH - len(message))
        return message + needed_characters
