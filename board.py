from typing import List, Union

from pieces import *


__all__ = ('Board',)


class Board:
    """Board represents game state: it stores all blocks, statistics and number of moves."""

    def __init__(self, inner_width: int = 10, inner_height: int = 20):
        self.inner_width = inner_width
        self.inner_height = inner_height
        self.width = self.inner_width + 2
        self.height = self.inner_height + 2

        self.full_row_mask = (1 << self.width) - 1
        self.empty_row_mask = (1 << (self.width - 1)) + 1

        self.content = ([self.full_row_mask] +
                                   [self.empty_row_mask] * self.inner_height +
                                   [self.full_row_mask])

        self.column_heights = [0] * self.width

        self.aggregate_height = 0
        self.complete_lines = 0
        self.blocks = 0
        self.holes = self.aggregate_height - self.blocks
        self.bumpiness = 0

        self.rows_cleared = 0
        self.moves = 0

    def get_block(self, x: int, y: int) -> bool:
        return bool(self.content[y] & (1 << x))

    def _bit_set_block(self, x: int, y: int) -> None:
        self.content[y] |= (1 << x)

    def _bit_unset_block(self, x: int, y: int) -> None:
        self.content[y] &= ~(1 << x)

    def stack_block(self, x: int, y: int, h: int = 1) -> None:
        """This function can be called only under quite restrictive conditions.
        If something doesn't work, check this function.

        This updates all statistics needed by AI.
        """
        new_height = y + h - 1
        old_height = self.column_heights[x]
        self.column_heights[x] = new_height

        self.aggregate_height += (new_height - old_height)

        for i in range(y, y + h):
            self._bit_set_block(x, i)
            if self.content[i] == self.full_row_mask:
                self.complete_lines += 1
        self.blocks += h

        self.holes = self.aggregate_height - self.blocks

        if x > 1:
            self.bumpiness -= (abs(old_height - self.column_heights[x - 1]) -
                               abs(new_height - self.column_heights[x - 1]))
        if x < self.inner_width:
            self.bumpiness -= (abs(old_height - self.column_heights[x + 1]) -
                               abs(new_height - self.column_heights[x + 1]))

    def unstack_block(self, x: int, y: int, h: int = 1):
        """Only stacked block (with `stack_block()`) can be unstacked!

        This updates all statistics needed by AI.
        """

        new_height = y - 1
        while not self.get_block(x, new_height):
            new_height -= 1
        old_height = self.column_heights[x]
        self.column_heights[x] = new_height

        self.aggregate_height -= old_height
        self.aggregate_height += new_height

        for i in range(y, y + h):
            if self.content[i] == self.full_row_mask:
                self.complete_lines -= 1
            self._bit_unset_block(x, i)
        self.blocks -= h

        self.holes = self.aggregate_height - self.blocks

        if x > 1:
            self.bumpiness -= (abs(old_height - self.column_heights[x - 1]) -
                               abs(new_height - self.column_heights[x - 1]))
        if x < self.inner_width:
            self.bumpiness -= (abs(old_height - self.column_heights[x + 1]) -
                               abs(new_height - self.column_heights[x + 1]))

    def find_drop_y(self, rotation: Rotation, x: int) -> int:
        """Finds minimum y at which `rotation` can be safely placed"""

        return max(self.column_heights[x + dx] - segment.y + 1 for dx, segment in enumerate(rotation.segments))

    def drop_rotation(self, rotation: Rotation, x: int, final: bool = False) -> Union[int, None]:
        """Drops `rotation` (places at minimum possible y).
        Returns y: int on success (used later to `undrop_rotation()`,
        None if `rotation` can't be placed in given column.

        If `final` is `True`, `moves` is incremented.
        """

        y = self.find_drop_y(rotation, x)

        if y + max(segment.y + segment.h for segment in rotation.segments) - 1 > self.inner_height:
            return None

        for dx, segment in enumerate(rotation.segments):
            self.stack_block(x + dx, y + segment.y, segment.h)

        if final:
            self.moves += 1

        return y

    def undrop_rotation(self, rotation: Rotation, x: int, y: int) -> None:
        """Only dropped rotation (with `drop_block()`) can be undropped.
        `y` should be a result from `drop_block()`
        """

        for dx, segment in enumerate(rotation.segments):
            self.unstack_block(x + dx, y + segment.y, segment.h)

    def collect_rows(self) -> None:
        for i in range(1, len(self.content) - 1):
            while self.content[i] == self.full_row_mask:
                self.content.pop(i)
                self.content.pop()
                self.content.append(self.empty_row_mask)
                self.content.append(self.full_row_mask)

                self.rows_cleared += 1
                self.blocks -= self.inner_width
        self.complete_lines = 0

    def __str__(self) -> str:
        return "\n".join("".join("██" if self.get_block(x, y) else "  "
                                 for x in range(0, self.width)) for y in range(self.height - 1, -1, -1))
