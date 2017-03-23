"""
More unit tests? No! What your code needs is petrol and a match.
"""


from pygame import *

from game import *

from logging import warning
warning("Pygame display is very limited: use tkinter display (from tk_display.py) whenever possible")


__all__ = ('PygameTetrisDisplay',)


WHITE = Color('white')


class PygameTetrisDisplay:
    def __init__(self):
        self.game = TetrisGame()

        self.screen = display.set_mode((self.game.board.width * 16 + 32, self.game.board.height * 16 + 32))

        self.paused = False

    def main_loop(self):
        while True:
            for e in event.get():
                if e.type == QUIT:
                    return
                elif e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.paused = not self.paused

            if not self.paused:
                self.game.move()

            self.draw()

            display.update()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for y in range(self.game.board.height):
            for x in range(self.game.board.width):
                if self.game.board.get_block(x, y):
                    draw.rect(self.screen, WHITE, (16 + x * 16, (self.game.board.height - y - 1) * 16 + 16,
                                                   16, 16))


if __name__ == '__main__':
    PygameTetrisDisplay().main_loop()

