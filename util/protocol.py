from enum import Enum 

class REQ_TYPES(Enum):
    JOIN_LOBBY = 1
    LEAVE_LOBBY = 2
    GAME_COUNTDOWN = 3
    LOBBY_DATA = 4
    GAMESTATE = 5
    DISCONNECT = 6
    DENIED = 7
    APPROVED = 8

def validate_request(req):
    pass