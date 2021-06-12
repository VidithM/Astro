import pygame
import sys 
from network import Network 

sys.path.append('../util')

from protocol import REQ_TYPES
from message import Message

my_conn = None 
in_lobby = False 

my_conn = Network('192.168.1.244', 5050)

while(True):
    typ = input()

    send = Message(REQ_TYPES[typ])
    my_conn.make_request(send)