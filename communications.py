#!/usr/bin/python3
import socket
from multiprocessing import Process, Queue, Pipe
from information import information

class communications(object):
    '''Class that manages communications with the user interface'''
    __SERVER_NAME = "192.168.42.1"
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
        self.conn_recv, self.conn_send = Pipe(True)
        self.connected = False
        pro = lambda:self.connect_to_server(self.conn_send)
        Process(target=pro, daemon=True).start()
    def __repr__(self):
        pass
    def is_connected(self):
        if self.conn_recv.poll():
            self.connected = self.conn_recv.recv()
        return self.connected
    def connect_to_server(self, conn_send):
        '''Attempts to connect to the server
        
        Once connected, a new process is used to monitor recieved data
        '''
        print("comms?")
        while True:
            '''Loop until a connection is found'''
            try:
                self.sock.connect(self.server_info)
            except ConnectionRefusedError:
                '''Don't break the loop just because no connection was found'''
                continue
            '''Break loop because connection was not refused'''
            break
        print("comms!")
        conn_send.send(True)
        '''Updates communications.recieved_messages with any recieved data
        
        This is a seperate process as socket.recv() will block the thread
        '''
        while True:
            try:
                bytes = self.sock.recv(self.__MAX_MESSAGE_LENGTH)
            except KeyboardInterrupt:
                self.sock.shutdown(1)
                self.sock.close()
                break
            message = bytes.decode('utf-8')
            if message is "":
                print("setting connection to false")
                conn_send.send(False)
                self.connect_to_server(conn_send)
                return
            self.recieved_messages.put(message)
    def send_message(self, message):
        '''Attempts to send data to client'''
        if self.is_connected():
            if len(message) > self.__MAX_MESSAGE_LENGTH:
                print("Message \"" + message + "\" is to long\n")#TODO: to log file
            else:
                print(message + " sent")
                bytes = self.fill_out_message(message).encode('utf-8')
                self.sock.sendall(bytes)
        else:
            print("Prevented information send because no connection has been made")
            pass
    def handle_incoming_messages(self, ui):
        '''Called by robot to handle any data sent by the user_interface'''
        while not self.recieved_messages.empty():
            message = self.recieved_messages.get()
            print(message)
            if message == self.fill_out_message("DISABLE"):
                ui.robot_info.enable_state = information.state_disabled
            elif message == self.fill_out_message("ENABLE_TELEOP"):
                ui.robot_info.enable_state = information.state_teleop_enabled
            elif message == self.fill_out_message("ENABLE_AUTO"):
                ui.robot_info.enable_state = information.state_auto_enabled
            else:
                print("Unknown recieved message: \"" + message + "\"")
                #TODO: to error log file
    def fill_out_message(self, message):
        needed_characters = "_" * (self.__MAX_MESSAGE_LENGTH - len(message))
        return message + needed_characters
