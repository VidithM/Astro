import socket
import threading
import sys
import pickle
from loguru import logger

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
        logger.info('SERVER STARTED')
        new_client_thread = threading.Thread(target=self.accept_connection)
        new_client_thread.start()


    def broadcast(self, msg, **kwargs):
        for client in self.clients:
            if(client == kwargs.get('exclude')):
                continue
            conn = self.clients[client]
            conn.send(pickle.dumps(msg))
            
    def process_req(self, msg, addr, conn):
        typ = msg.req_type
        if(typ == REQ_TYPES.JOIN_LOBBY):
            logger.info(f'RECEIVED JOIN LOBBY REQ FROM {addr}')
            if((not addr in self.clients) and (not self.inGame)):
                self.clients[addr] = conn
                logger.info(f'CONNECTED CLIENT {addr}')
                conn.send(pickle.dumps(Message(REQ_TYPES.APPROVED)))
                if(len(self.clients) == 4):
                    #start game
                    self.inGame = True
                    dummy = Message(REQ_TYPES.GAMESTATE)
                    self.broadcast(dummy)
            else:
                logger.error(f'CLIENT COULD NOT JOIN LOBBY! {addr}')
                conn.send(pickle.dumps(Message(REQ_TYPES.DENIED)))                       
        elif(typ == REQ_TYPES.LEAVE_LOBBY):
            if(addr in self.clients):
                self.clients.pop(addr)
            else:
                logger.error(f'CLIENT NOT FOUND! {addr}')
            
        elif(typ == REQ_TYPES.GAMESTATE):
            msg = Message(REQ_TYPES.GAMESTATE)
            if((addr in self.clients)):
                self.broadcast(msg, {'exclude' : addr})
        else:
            logger.error(f'INVALID REQUEST CODE! {addr}')
            pass
        

    def accept_connection(self):
        logger.info(f'TCP SOCKET OPENED ON {self.ip}:{self.port}')
        self.endpoint.listen()
        while(True):
            (conn, addr) = self.endpoint.accept()
            logger.info(f'OPENED CONNECTION W/ {addr[0]}')
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
                logger.info(f'CLOSED CONNECTION W/ {addr}')
                conn.send(pickle.dumps(Message(REQ_TYPES.DISCONNECT)))
                conn.close()
                break #Thread is suspended once function returns

if __name__ == '__main__':
    nw = Network()
