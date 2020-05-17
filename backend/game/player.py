import uuid


class Player(object):
    def __init__(self, websocket, username):
        self.websocket = websocket
        self.username = username
        self.uuid = str(uuid.uuid4())

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'username': self.username
        }
