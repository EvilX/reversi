import json
import logging
from uuid import uuid4

from game.game import Game, InvalidTurn
from game.manager import Player


log = logging.getLogger(__file__)


class RoomError(Exception):
    pass


class Room(object):
    def __init__(self, manager):
        self.manager = manager
        self.uuid = str(uuid4())
        self.game = Game()
        self.players = [None, None]

    async def connect(self, player: Player):
        """Connect a new player to the room"""
        if self.is_running:
            return 

        for index, p in enumerate(self.players):
            if p is None:
                self.players[index] = player
                await self.send(player, 'game_enter', {
                    'index': index, 
                    'game_uuid': self.uuid
                })
                break
        
        await self.manager.update_room(self)

        await self.chat(f'{player.username} is connected!')

        if self.is_running:
            log.debug(f'Game started: {self.uuid}')
            self.game.reset()            

            await self.broadcast('game_start', self.to_dict())
            await self.send_state()
            await self.chat('Game started!')

        await self.cycle(player)

    @property
    def is_running(self):
        """Check the game is running"""
        return self.players[0] is not None and self.players[1] is not None

    @property
    def is_empty(self):
        """Check is the room is empty"""
        return self.players[0] is None and self.players[1] is None

    def to_dict(self):
        """Convert a room to the dict"""
        players = {player.uuid: player.to_dict() for player in self.players if player is not None}
        return {
            'uuid': self.uuid,
            'players': players,
            'is_running': self.is_running,
        }

    async def send(self, player: Player, message: str, payload: dict):
        """Send a message to the user"""
        try:
            await player.websocket.send(json.dumps({
                "message": message,
                "payload": payload
            }))
        except Exception as E:
            log.error(f'Send error: {E}')
            await self.disconnect(player)

    async def broadcast(self, message: str, payload: dict):
        """Broadcast a message to all players"""
        for p in self.players:
            if p is not None:
                await self.send(p, message, payload)

    async def send_state(self):
        """Send a state of the game to all users"""
        board = []
        for x, board_line in enumerate(self.game.board):
            line = {
                'line': x,
                'values': []
            }
            for y, value in enumerate(board_line):
                line['values'].append({
                    'index': x + y,
                    'x': x,
                    'y': y,
                    'value': value
                })
            board.append(line)

        await self.broadcast('game_state', {
                'board': board,
                'score': self.game.score,
                'order': self.game.order
            })

    async def turn(self, payload, player):
        """Process a turn"""
        x = payload['x']
        y = payload['y']
        try:
            self.game.turn(x, y, self.players.index(player))
        except InvalidTurn:
            await self.send(player, 'error', {
                'type': 'invalid_turn',
                'args': payload
            })
        else:
            await self.send_state()

    async def chat(self, text, player=None):
        """Send a message to the chat"""
        await self.broadcast('game_chat', {
            'author': player.username if player else None,
            'text': text
        })

    async def cycle(self, player):
        """Main game cycle"""
        try:
            while True:
                data = await player.websocket.recv()
                try:
                    message = json.loads(data)
                except Exception as E:
                    log.error(f'Invalid game message: {E}, {data}')
                    continue
                log.debug(f'Process message: {message} from {player.username}')

                if message['method'] == 'chat':
                    await self.chat(message['payload']['text'], player)
                if message['method'] == 'turn' and self.is_running:
                    await self.turn(message['payload'], player)
                if message['method'] == 'exit':
                    break
        except Exception as E:
            log.error(f'Room error: {E}')
        finally:
            await self.disconnect(player)

    async def disconnect(self, player):
        """Disconnect a player"""
        self.players[self.players.index(player)] = None
        await self.chat(f'{player.username} disconnected')
        await self.broadcast('game_stop', self.to_dict())
        await self.manager.update_room(self)
