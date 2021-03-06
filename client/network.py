import socket
import threading
import pickle
import sys
from loguru import logger

sys.path.append('../util')

from protocol import *

class Network:
    def __init__(self, ip, port):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port 
        self.ip = ip 
        self.endpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endpoint.connect((ip, port))
        self.connected = True
        self.msg_queue = []

        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def make_request(self, req):
        validate_request(req) #Throws exception for illegal requests

        serialized_req = pickle.dumps(req)
        req_sz = str(len(serialized_req)).encode('utf-8')
        send_sz = req_sz + (b' ' * (1024 - len(req_sz))) #1024 byte header
        self.endpoint.send(send_sz)
        self.endpoint.send(serialized_req)
    
    def listen(self):
        while(True):
            data = self.endpoint.recv(1024)
            if(data):
                msg = pickle.loads(data)
                self.msg_queue.append(msg)
    
    def active(self):
        return self.connected

       


        
