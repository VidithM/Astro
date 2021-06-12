import pygame
import sys 
from network import Network 

sys.path.append('../util')

from protocol import REQ_TYPES
from message import Message

my_conn = None 
in_lobby = False 

my_conn = Network('192.168.1.244', 5050)
send = Message(REQ_TYPES.LEAVE_LOBBY)
my_conn.make_request(send)


