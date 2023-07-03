from enum import Enum


class EventName(str, Enum):
    Connect = "connect"
    Disconnect = "disconnect"
    Game = "game"
    ActivePlayers = "active_players"
    Time = 'time'
    Score = 'score'
