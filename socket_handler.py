from typing import List, Any

import socketio

from models.entities.active_player import ActivePlayer
from models.events.event import EventName


class SocketHandler:
    def __init__(self):
        self.active_players: List[ActivePlayer] = []
        self.sio_server = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
        self.app = socketio.ASGIApp(socketio_server=self.sio_server, socketio_path='sockets')
        self.register_event_handlers()

    def register_event_handlers(self):
        @self.sio_server.event
        async def connect(sid, environ, auth):
            found_player = next((x for x in self.active_players if
                                 x.token == environ['HTTP_AUTHORIZATION'].split('Bearer ')[1]), None)
            if not found_player:
                self.active_players.append(
                    ActivePlayer(sid=sid,
                                 token=environ['HTTP_AUTHORIZATION'].split('Bearer ')[1]))
                await self.sio_server.emit(EventName.ActivePlayers, len(self.active_players))

        @self.sio_server.event
        async def disconnect(sid):
            self.active_players = [x for x in self.active_players if x.sid != sid]
            await self.sio_server.emit(EventName.ActivePlayers, len(self.active_players))

    async def emit(self, event_name: EventName, data: Any, to=None):
        if to:
            sid = next((x.sid for x in self.active_players if x.token == to), None)
            await self.sio_server.emit(event_name, data, sid)
        else:
            await self.sio_server.emit(event_name, data)


socket_handler = SocketHandler()
