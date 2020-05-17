import json
import logging
import websockets

from game.player import Player
from game.room import Room
from game.utils import ERROR_UNSUPPORTED_PAYLOAD

log = logging.getLogger(__file__)


class GameManager(object):
    players = set()
    rooms = set()

    async def connect(self, websocket: websockets.WebSocketServerProtocol, path):
        """
        Wait the login message
        {
            "method": "login",
            "payload": {
                "username": "USERNAME",
            }
        }
        """
        try:
            data = await websocket.recv()
            message = json.loads(data)
            method = message.get('method')
            if method == 'login':
                username = message['payload']['username']
                player = Player(websocket, username)
                log.info(f'Logged in {username}')
        except Exception as E:
            log.error(f'Protocol error: {E}')
            try:
                websocket.close(ERROR_UNSUPPORTED_PAYLOAD, json.dumps({'error': 'Wrong initial message'}))
            except:
                pass
            self.players.remove(websocket)
        else:
            self.players.add(player)
            await self.cycle(player)

    async def cycle(self, player: Player):
        """Main cycle"""
        await self.send(player, 'players', self.get_all_players())
        await self.send(player, 'rooms', self.get_all_rooms())
        await self.send(player, 'start', {
            'username': player.username
        })
        await self.broadcast('player_update', player.to_dict())
        try:
            while True:
                data = await player.websocket.recv()
                message = json.loads(data)
                method = message.get('method')
                if method == 'new_game':
                    await self.game(player)
                    await self.send(player, 'dashboard', {})
                if method == 'enter_game':
                    game_uuid = message['payload']['game_uuid']
                    await self.game(player, game_uuid=game_uuid)                
                    await self.send(player, 'dashboard', {})
        except Exception as E:
            log.error(f'Disconnect player: {E}')
            await self.disconnect(player)

    async def disconnect(self, player):
        self.players.remove(player)
        try:
            await player.websocket.close(ERROR_UNSUPPORTED_PAYLOAD, json.dumps({'error': 'Wrong initial message'}))
        except:
            pass
        await self.broadcast('player_delete', {
            'uuid': player.uuid
        })
        
        for room in self.rooms:
            if player in room.players:
                room.disconnect(player)

    async def game(self, player, game_uuid=None):
        """Enther the game"""
        if not game_uuid:
            room = self.new_room()
        else:
            room = self.find_room(game_uuid)
        
        if room is not None:
            await room.connect(player)

    def new_room(self):
        """Create a new room"""
        room = Room(self)
        self.rooms.add(room)
        return room

    def find_room(self, game_uuid):
        """Find a room by uuid"""
        for room in self.rooms:
            if room.uuid == game_uuid:
                return room
        return None

    async def update_room(self, room: Room):
        """Send room update to all clients"""
        if room.is_empty:
            self.rooms.remove(room)
            await self.delete_room(room)
        else:
            await self.broadcast('room_update', room.to_dict())

    async def delete_room(self, room: Room):
        """Send room delete to all clients"""
        await self.broadcast('room_delete', room.to_dict())

    def get_all_rooms(self) -> dict:
        """Get the all rooms dict"""
        rooms = {}
        for room in self.rooms:
            rooms[room.uuid] = room.to_dict()
        return rooms

    def get_all_players(self) -> dict:
        """Get the all players dict"""
        players = {}
        for player in self.players:
            players[player.uuid] = player.to_dict()
        return players

    async def broadcast(self, message, payload):
        """Broadcast a message to all connected players"""
        message = {
            "message": message,
            "payload": payload
        }
        for player in self.players:
            try:
                await player.websocket.send(json.dumps(message))
            except Exception as E:
                log.debug(f'Send error: {E}')

    async def send(self, player, message, payload):
        message = {
            "message": message,
            "payload": payload
        }
        try:
            await player.websocket.send(json.dumps(message))
        except Exception as E:
            log.debug(f'Send error: {E}')
