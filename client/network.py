import socket
import threading
import pickle
from termcolor import cprint
import sys

sys.path.append('../util')

from protocol import *

class Network:
    def __init__(self, ip, port):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port 
        self.ip = ip 
        self.endpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endpoint.connect((ip, port))

    def make_request(self, req):
        validate_request(req) #Throws exception for illegal requests

        serialized_req = pickle.dumps(req)
        req_sz = str(len(serialized_req)).encode('utf-8')
        send_sz = req_sz + (b' ' * (1024 - len(req_sz))) #1024 byte header
        self.endpoint.send(send_sz)
        self.endpoint.send(serialized_req)
       


        
