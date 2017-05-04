import time
import socket
import select
import sys
from chat_utils import *
import client_state_machine as csm

import threading

class Client:
    def __init__(self):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''        
        
    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        
    def get_name(self):
        return self.name
        
    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        
        # if len(argv) > 1, we assume they're giving an IP address to connect to
        # else, use the localhost as defined in chat_utils.py
        if len(sys.argv) > 1:
            alt_IP = sys.argv[-1]
            alt_SERVER = (alt_IP, CHAT_PORT)
            self.socket.connect(alt_SERVER)
        else:
            self.socket.connect(SERVER)

        self.sm = csm.ClientSM(self.socket)
        reading_thread = threading.Thread(target=self.read_input)
        reading_thread.daemon = True
        reading_thread.start()
        
    def shutdown_chat(self):
        return
        
    def send(self, msg):
        mysend(self.socket, msg)
        
    def recv(self):
        return myrecv(self.socket)
        
    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        peer_code = M_UNDEF
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
            peer_code = peer_msg[0]
            peer_msg = peer_msg[1:]
        return my_msg, peer_code, peer_msg
        
    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            self.system_msg = ''
                
    def login(self):
        my_msg, peer_code, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = M_LOGIN + self.name
            self.send(msg)
            response = self.recv()
            if response == M_LOGIN+'ok':
                self.state = S_LOGGEDIN
# zz: change!
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response == M_LOGIN + 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        while True:         # uncomment the below for a stress test
#            if self.state == S_CHATTING:
#                text = 'adfadsfafd' + self.name
#                time.sleep(2)
#            else:
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()      
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_code, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_code, peer_msg)
