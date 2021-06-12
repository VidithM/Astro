class Message:
    def __init__(self, req_type):
        self.params = {}
        self.req_type = req_type 
    
    def add_param(self, key, val):
        self.params[key] = val
    