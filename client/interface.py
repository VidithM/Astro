import pygame
import sys 
import threading
import atexit
from network import Network

sys.path.append('../util')

from protocol import REQ_TYPES
from message import Message

my_conn = None 
my_gamestate = None 

in_lobby = False 

my_conn = Network('192.168.1.244', 5050)
send = Message(REQ_TYPES.JOIN_LOBBY)
my_conn.make_request(send)

def render_main_menu():
    pass

def render_lobby():
    pass 

def render_game():
    pass 

#Keeps running until a disconnect is received
def scan_queue():
    while(True):
        if(len(my_conn.msg_queue) > 0):
            top = my_conn.msg_queue[0]
            my_conn.msg_queue.pop(0)
            if(top.req_type == REQ_TYPES.LOBBY_DATA):
                pass
            elif(top.req_type == REQ_TYPES.GAMESTATE):
                pass

#scan_thread.start()

def close_conn():
    send = Message(REQ_TYPES.LEAVE_LOBBY)
    my_conn.make_request(send)

atexit.register(close_conn)

while(True):
    scan_queue()
    if(in_lobby):
        render_lobby()
    elif(in_game):
        render_game()
    else:
        render_main_menu()
