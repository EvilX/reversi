import logging
import copy

log = logging.getLogger(__file__)


class InvalidTurn(Exception):
    pass


class Game(object):
    size_x = 8
    size_y = 8

    def __init__(self):
        self.board = []
        self.score = [0, 0]
        self.order = 0

    def reset(self): 
        self.board = []
        for _ in range(self.size_y):
            self.board.append([-1 for _ in range(self.size_y)])
        # Init state
        self.board[3][3] = 0
        self.board[3][4] = 1
        self.board[4][4] = 0
        self.board[4][3] = 1
        self.score = [0, 0]
        self.order = 0

    def turn(self, x: int, y: int, player: int):
        log.debug(f'Turn: {player} ({x}, {y})')
        self.process_turn(x, y, player)
        self.calculate_score()

        if self.order == 0:
            self.order = 1
        else:
            self.order = 0

    def process_turn(self, x: int, y: int, player: int):
        """
        Process the turn
        """
        if self.board[x][y] != -1:
            raise InvalidTurn()

        board_state = copy.deepcopy(self.board)
        is_allowed = False

        # All directions
        vectors = (
            (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
        )
        
        for dx, dy in vectors:
            point_x = x + dx
            point_y = y + dy
            count = 0
            tmp_board_state = copy.deepcopy(board_state)
            tmp_board_state[x][y] = player

            while True:
                if (not (0 <= point_x < self.size_x) or not (0 <= point_y < self.size_y)) \
                    or tmp_board_state[point_x][point_y] == -1:
                    # The end of the board or an empty cell
                    count = 0
                    break                    
                if tmp_board_state[point_x][point_y] == player:
                    # Own
                    break

                tmp_board_state[point_x][point_y] = player
                count += 1
                point_x += dx
                point_y += dy

            if count > 0:
                is_allowed = True
                board_state = tmp_board_state
        
        # The turn is not valid. 
        if not is_allowed:
            raise InvalidTurn()

        # Update the field with a new state
        self.board = board_state

    def calculate_score(self):
        score = [0, 0]
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] != -1:
                    score[self.board[x][y]] += 1

        self.score = score
