from math import *

from board import *
from pieces import *


__all__ = ('AI',
           'AdvancedAI')


class AI:
    def make_best_move(self, board: Board, piece: Piece, next_piece: Piece) -> bool:
        raise NotImplementedError("abstract")


class AdvancedAI(AI):
    """Very advanced AI (in fact, it sometimes can play infinitely)

    It's just a coincidence that at https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
    there are exactly the same magic numbers.


    """

    default_aggregate_height_weight = -0.510066
    default_complete_lines_weight = 0.76066
    default_holes_weight = -0.35663
    default_bumpiness_weight = -0.184483

    def __init__(self, aggregate_height_weight: float = default_aggregate_height_weight,
                 complete_lines_weight: float = default_complete_lines_weight,
                 holes_weight: float = default_holes_weight, bumpiness_weight: float = default_bumpiness_weight):

        # These can be safely changed between calls to `make_best_move()`
        self.aggregate_height_weight = aggregate_height_weight
        self.complete_lines_weight = complete_lines_weight
        self.holes_weight = holes_weight
        self.bumpiness_weight = bumpiness_weight

        self.moves_made = 0

    def make_best_move(self, board: Board, piece: Piece, next_piece: Piece) -> bool:
        best_x = best_r = None
        best_score = -inf
        for r, rotation in enumerate(piece.rotations):
            for x in range(1, board.inner_width - len(rotation.segments) + 2):
                y = board.drop_rotation(rotation, x)
                if y is None:
                    continue

                for rotation2 in next_piece.rotations:
                    for x2 in range(1, board.inner_width - len(rotation2.segments) + 2):
                        y2 = board.drop_rotation(rotation2, x2)

                        score = (board.aggregate_height * self.aggregate_height_weight +
                                 board.complete_lines * self.complete_lines_weight +
                                 board.holes * self.holes_weight +
                                 board.bumpiness * self.bumpiness_weight)
                        if score > best_score:
                            best_score = score
                            best_x, best_r = x, r

                        if y2 is not None:
                            board.undrop_rotation(rotation2, x2, y2)

                board.undrop_rotation(rotation, x, y)

        if best_score > -inf:
            board.drop_rotation(piece.rotations[best_r], best_x, final=True)
            self.moves_made += 1
            return True
        else:
            return False

