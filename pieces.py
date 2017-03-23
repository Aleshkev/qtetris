from typing import Tuple

__all__ = ('Segment', 'Rotation', 'Piece',
           'TETRIMINOS')


class Segment:
    def __init__(self, y: int, h: int = 1):
        self.y = y
        self.h = h


class Rotation:
    def __init__(self, *segments: Tuple[Segment, ...]):
        self.segments = segments

        # Very slow generation of textual representation - makes this constructor very expensive
        w = len(self.segments)
        h = max(segment.y + segment.h for segment in self.segments)
        grid = [[False for x in range(w)] for y in range(h)]
        for x, segment in enumerate(self.segments):
            for y in range(segment.y, segment.y + segment.h):
                grid[y][x] = True
        self.str = "\n".join("".join("██" if grid[y][x] else "  " for x in range(0, w)) for y in range(h - 1, -1, -1))

    def __str__(self):
        return self.str


class Piece:
    def __init__(self, *rotations: Tuple[Rotation, ...]):
        self.rotations = rotations

    def __str__(self):
        return self.rotations[0].__str__()


_p, _r, _s = Piece, Rotation, Segment
TETRIMINOS = (_p(_r(_s(0, 2), _s(0, 2)), ),  # O
              _p(_r(_s(0, 1), _s(0, 1), _s(0, 1), _s(0, 1)), _r(_s(0, 4))),  # I
              _p(_r(_s(0, 2), _s(0, 1), _s(0, 1)), _r(_s(0, 3), _s(2, 1)),  # J
                 _r(_s(1, 1), _s(1, 1), _s(0, 2)), _r(_s(0, 1), _s(0, 3))),
              _p(_r(_s(0, 1), _s(0, 1), _s(0, 2)), _r(_s(0, 3), _s(0, 1)),  # L
                 _r(_s(0, 2), _s(1, 1), _s(1, 1)), _r(_s(2, 1), _s(0, 3))),
              _p(_r(_s(0, 1), _s(0, 2), _s(1, 1)), _r(_s(1, 2), _s(0, 2))),  # S
              _p(_r(_s(1, 1), _s(0, 2), _s(0, 1)), _r(_s(0, 2), _s(1, 2))),  # Z
              _p(_r(_s(0, 1), _s(0, 2), _s(0, 1)), _r(_s(0, 3), _s(1, 1)),  # T
                 _r(_s(1, 1), _s(0, 2), _s(1, 1)), _r(_s(1, 1), _s(0, 3))))


"""
# How does it work?

You see, every Piece has some Rotations. For example, T piece has four of them:

           ##    ######    ##
      ##   ####    ##    ####
    ###### ##              ##

But S piece has only two:

              ##
    ####    ####
      ####  ##

And O piece has one:

    #####
    #####

So, every Piece has few Rotations.


To optimize operations on these pieces, I sliced every Rotation into Segments. So,

    ####
      ####

is encoded as

    [Segment(y=1, h=1),
     Segment(y=0, h=2),
     Segment(y=0, h=1)]

because

    x=0:
    y = 1, height = 1
    ##        1
              0

    x = 1:
    y = 0, height = 2
    ## ##     1
       ##     0

    x = 2:
    y = 0, height = 1
    ## ##     1
       ## ##  0

what gives us

    ####
      ####

"""
