import socket
import threading
import sys
import pickle
from termcolor import cprint

sys.path.append('../util/')

from protocol import *
from message import Message

class Network:
    def __init__(self):
        self.inGame = False
        self.clients = {} #Maps ip -> TCP connection

        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.endpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endpoint.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.endpoint.bind((self.ip, self.port))

        self.req_queue = []

        new_client_thread = threading.Thread(target=self.accept_connection)
        new_client_thread.start()


    def broadcast(self, msg):
        for client in self.clients:
            conn = self.clients[client]
            conn.send(pickle.dumps(msg))
            
    def process_req(self, msg, addr, conn):
        typ = msg.req_type
        if(typ == REQ_TYPES.JOIN_LOBBY):
            cprint('[LOG] RECEIVED JOIN LOBBY REQ FROM ' + str(addr), 'yellow')
            if((not addr in self.clients) and (not self.inGame) and len(self.clients) < 4):
                self.clients[addr] = conn
                cprint('[LOG] CONNECTED CLIENT ' + str(addr), 'yellow')
                print(self.clients)
            else:
                cprint('[ERR] CLIENT COULD NOT JOIN LOBBY! ' + str(addr), 'red')                         
        elif(typ == REQ_TYPES.LEAVE_LOBBY):
            if(addr in self.clients):
                self.clients.pop(addr)
            else:
                cprint('[ERR] CLIENT NOT FOUND! ' + str(addr), 'red')
            
        elif(typ == REQ_TYPES.GAMESTATE):
            msg = Message(REQ_TYPES.GAMESTATE)
            if((addr in self.clients)):
                self.broadcast(msg)
        else:
            cprint('[ERR] INVALID REQUEST CODE! ' + str(addr), 'red')
            pass
        

    def accept_connection(self):
        cprint('[LOG] SERVER STARTED', 'yellow')
        cprint('[LOG] TCP SOCKET OPENED ON ' + str(self.ip) + ' ' + str(self.port), 'yellow')
        self.endpoint.listen()
        while(True):
            (conn, addr) = self.endpoint.accept()
            cprint('[LOG] OPENED CONNECTION W/ ' + str(addr), 'yellow')
            handle_req_thread = threading.Thread(target=self.handle_req, args=(conn, addr[0]))
            handle_req_thread.start()


    def handle_req(self, conn, addr):
        while(True):
            #First check for incoming requests
            sz = conn.recv(1024).decode('utf-8')
            if(sz):
                sz = int(sz)
                msg = pickle.loads(conn.recv(sz))
                self.process_req(msg, addr, conn)

            #Check for client disconnect
            if(not (addr in self.clients)):
                cprint('[LOG] CLOSED CONNECTION W/ ' + str(addr), 'yellow')
                conn.close()
                break #Thread is suspended once function returns

if __name__ == '__main__':
    nw = Network()
