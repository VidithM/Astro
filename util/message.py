import time
import hashlib

class Message:
    def __init__(self, req_type):
        self.params = {'id' : hashlib.sha256(str(time.time()).encode()).hexdigest()}
        self.req_type = req_type 
    
    def add_param(self, key, val):
        self.params[key] = val
    