# -*- coding: utf-8 -*-
from checkers.game import Game


BLACK = 1
BLACK2 = BLACK + 2
WHITE = 2
WHITE2 = WHITE + 2
EMPTY = 0
WCELL = -1
BCELL = -2

COLS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
ROWS = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']
DISCS = [
    {
        BLACK: '🔴',
        BLACK2: '🟠',
        WHITE: '🔵',
        WHITE2: '🟢',
        WCELL: '⬜',
        BCELL: '⬛',
    },
]


class Board:
    def __init__(self, board: str = None) -> None:
        self.game = Game()
        if board:
            lines = board.split('\n')
            self.theme = int(lines.pop(0))
            for mv in lines.pop(0).split():
                self.game.move(list(map(int, mv.split(','))))
        else:
            self.theme = 0

    @property
    def turn(self):
        return self.game.board.player_turn

    def export(self):
        moves = ' '.join('{},{}'.format(*mv) for mv in self.game.moves)
        return '\n'.join((str(self.theme), moves))

    def __str__(self):
        board = [[BCELL if (i+j+1) % 2 == 0 else WCELL for j in range(8)]
                 for i in range(8)]
        for p in self.game.board.pieces:
            if not p.position:
                continue
            disc = p.player + 2 if p.king else p.player
            i, j = self.position2coord(p.position)
            board[i][j] = disc
        text = '|'.join(COLS) + '\n'
        for i, row in enumerate(board):
            for d in row:
                text += self.get_disc(d) + '|'
            text += ROWS[i] + '\n'
        return text

    def position2coord(self, position: int) -> tuple:
        pos = 1
        for i in range(8):
            for j in range(8):
                if (i+j+1) % 2 == 0:
                    if pos == position:
                        return (i, j)
                    pos += 1
        return (-1, -1)

    def get_disc(self, disc) -> str:
        return DISCS[self.theme][disc]

    def get_position(self, coord: str) -> int:
        sorted_coord = sorted(coord.lower())
        x = 'abcdefgh'.find(sorted_coord[1])
        y = '12345678'.find(sorted_coord[0])
        if x < 0 or y < 0 or (x + y + 1) % 2 != 0:
            return -1

        pos = 1
        for i in range(8):
            for j in range(8):
                if (i, j) == (x, y):
                    return pos
                if (i + j + 1) % 2 == 0:
                    pos += 1

        return -1  # impossible

    def move(self, coords: str) -> None:
        x = self.get_position(coords[:2])
        y = self.get_position(coords[2:])
        if x < 0 or y < 0:
            raise ValueError('Invalid move')

        self.game.move([x, y])

    def result(self) -> int:
        if not self.game.is_over():
            return -1
        return self.game.get_winner() or 0
