import asyncio
import logging
import sys

import websockets

from game.manager import GameManager


def setup_log():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == '__main__':
    setup_log()
    log = logging.getLogger(__file__)
    manager = GameManager()
    server = websockets.serve(
        manager.connect, "0.0.0.0", 8081
    )
    log.info('Start the servers')
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
