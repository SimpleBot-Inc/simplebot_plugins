# -*- coding: utf-8 -*-
import io

import chess
import chess.pgn
# typing
from typing import List
# ===


ranks = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
files = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭']
pieces = {
    'r': '♜',
    'n': '♞',
    'b': '♝',
    'q': '♛',
    'k': '♚',
    'p': '♟',
    'R': '♖',
    'N': '♘',
    'B': '♗',
    'Q': '♕',
    'K': '♔',
    'P': '♙',
    '.': ' ',
}


class Board:
    def __init__(self, game: str=None, p1: str=None, p2: str=None) -> None:
        if game:
            self.game = chess.pgn.read_game(io.StringIO(game))
            self.board = self.game.board()
            for move in self.game.mainline_moves():
                self.board.push(move)
        else:
            assert None not in (p1, p2)
            self.game = chess.pgn.Game()
            self.game.headers['White'] = p1
            self.game.headers['Black'] = p2
            self.board = self.game.board()

    def __str__(self) -> str:
        rboard: List[List[str]] = [[]]*8
        for i, line in enumerate(str(self.board).splitlines()):
            for j, cell in enumerate(line.split()):
                if cell == '.':
                    cell = '⬛' if (i+j+1) % 2 == 0 else '⬜'
                else:
                    cell = pieces[cell]
                rboard[j].insert(0, cell)

        text = '|'.join(ranks) + '\n'
        for i, row in enumerate(rboard):
            for cell in row:
                text += cell + '|'
            text += files[i] + '\n'
        return text

    @property
    def white(self) -> str:
        return self.game.headers['White']

    @property
    def black(self) -> str:
        return self.game.headers['Black']

    @property
    def turn(self) -> str:
        if self.board.turn == chess.WHITE:
            return self.white
        return self.black

    def move(self, mv: str) -> None:
        try:
            m = self.board.push_san(mv)
        except ValueError:
            m = self.board.push_uci(mv)
        self.game.end().add_variation(m)

    def export(self) -> str:
        return str(self.game)

    def result(self) -> str:
        return self.board.result()
