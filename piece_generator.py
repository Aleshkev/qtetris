from random import *

from pieces import *


__all__ = ('PieceGenerator',
           'SimpleRandomPieceGenerator', 'SevenSystemPieceGenerator')


class PieceGenerator:
    """Abstract class for Piece Generators.

    Piece Generator generates Tetris pieces. They can be accessed with `current_piece` and `next_piece` properties.
    When a piece is placed, `advance()` should be called to generate new piece.
    """

    @property
    def current_piece(self) -> Piece:
        raise NotImplementedError("abstract")

    @property
    def next_piece(self) -> Piece:
        raise NotImplementedError("abstract")

    def advance(self) -> None:
        raise NotImplementedError("abstract")


class SimpleRandomPieceGenerator(PieceGenerator):
    """Simple Piece Generator implementation returning always random piece"""

    def __init__(self):
        self.next_pieces = []
        self.advance()

    def advance(self):
        if len(self.next_pieces) > 0:
            self.next_pieces.pop(0)
        while len(self.next_pieces) < 2:
            self.next_pieces.append(choice(TETRIMINOS))

    @property
    def current_piece(self):
        return self.next_pieces[0]

    @property
    def next_piece(self):
        return self.next_pieces[1]


class SevenSystemPieceGenerator(SimpleRandomPieceGenerator):
    """More complex implementation of Piece Generator, which uses Seven System Random Generator
    (http://tetris.wikia.com/wiki/Random_Generator).
    """

    def advance(self):
        if len(self.next_pieces) > 0:
            self.next_pieces.pop(0)
        if len(self.next_pieces) < 2:
            l = list(TETRIMINOS)
            shuffle(l)
            self.next_pieces.extend(l)
