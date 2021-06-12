import socket
import threading
import sys
import pickle
from termcolor import cprint

sys.path.append('../util/')

from protocol import REQ_TYPES
from message import Message

class Network:
    def __init__(self):
        self.inGame = False
        self.clients = {} #Mapping ip -> TCP connection

        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.endpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endpoint.bind((self.ip, self.port))

        self.req_queue = []

        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

        self.process_queue()


    def broadcast(self, msg):
        #for client in clients:
        pass
            

    def process_queue(self):
        while(True):
            if(len(self.req_queue) > 0):
                (conn, addr) = self.req_queue[0]
                sz = conn.recv(1024).decode('utf-8') #1024 byte header
                if (sz):
                    sz = int(sz)
                    msg = pickle.loads(conn.recv(sz))
                    typ = msg.req_type
                    if(typ == REQ_TYPES.JOIN_LOBBY):
                        cprint('[LOG] RECEIVED JOIN LOBBY REQ FROM ' + str(addr[0]), 'yellow')
                        if((not self.inGame) and len(self.clients) < 4):
                            self.clients[addr[0]] = conn
                            cprint('[LOG] CONNECTED CLIENT ' + str(addr[0]), 'yellow')
                            print(self.clients)
                        else:
                            pass                            
                    elif(typ == REQ_TYPES.LEAVE_LOBBY):
                        if(addr[0] in self.clients):
                            self.clients.get(addr[0]).close()
                            cprint('[LOG] CLOSED CONNECTION W/ ' + str(addr[0]), 'yellow')
                            self.clients.pop(addr[0])
                        else:
                            cprint('[ERR] CLIENT NOT FOUND! ' + str(addr[0]), 'red')
                        conn.close()
                    elif(typ == REQ_TYPES.GAMESTATE):
                        pass 
                        conn.close()
                    else:
                        #Invalid request type
                        pass
                        conn.close()
            
                self.req_queue.pop(0)
        

    def listen(self):
        cprint('[LOG] SERVER STARTED', 'yellow')
        cprint('[LOG] TCP SOCKET OPENED ON ' + str(self.ip) + ' ' + str(self.port), 'yellow')
        self.endpoint.listen()
        while(True):
            (conn, addr) = self.endpoint.accept()
            self.req_queue.append((conn, addr))

if __name__ == '__main__':
    nw = Network()
    print('passed')
