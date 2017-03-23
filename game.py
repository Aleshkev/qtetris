from time import *

from board import *
from ai import *
from piece_generator import *


__all__ = ('TetrisGame',
           'GameOver')


class TetrisGame:
    """Game manages Board, AI and Piece Generator."""
    def __init__(self, board: Board = None, ai: AI = None,
                 piece_generator: PieceGenerator = None):
        self.board = board if board is not None else Board()
        self.ai = ai if ai is not None else AdvancedAI()
        self.piece_generator = piece_generator if piece_generator is not None else SevenSystemPieceGenerator()

        self.total_time = 0
        self.moves = 0

    def move(self):
        start = perf_counter()

        if not self.ai.make_best_move(self.board, self.piece_generator.current_piece, self.piece_generator.next_piece):
            raise GameOver()
        self.piece_generator.advance()
        self.board.collect_rows()

        end = perf_counter()
        self.total_time += (end - start)
        self.moves += 1

    def get_moves_per_second(self):
        return self.moves / self.total_time if self.total_time != 0 else 0.0


class GameOver(BaseException):
    pass

