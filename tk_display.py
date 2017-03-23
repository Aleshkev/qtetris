"""
               [...] Things without all remedy
Should be without regard: what's done, is done.
- Macbeth
Do not refactor.
"""

import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter.font


from game import *


__all__ = ('TkTetrisDisplay',)


class TkTetrisDisplay:
    def __init__(self):
        self.game = TetrisGame()

        try:
            from ctypes import windll
            windll.shell32.SetCurrentProcessExplicitAppUserModelID('qtetris.qtetris.qtetris.1')
        except ImportError:
            pass

        self.tk = tk.Tk()
        self.tk.maxsize(800, 700)
        self.tk.resizable(False, False)
        self.tk.title("ℚTetris")
        self.icon_img = tk.PhotoImage(file='qtetris_logo.png')
        self.tk.tk.call('wm', 'iconphoto', self.tk._w, self.icon_img)

        self.tk.rowconfigure(2, weight=1)
        self.tk.columnconfigure(1, weight=1)
        self.tk.columnconfigure(1, weight=1)

        tk.font.nametofont('TkFixedFont').config(size=13)

        self.board_text = tk.StringVar()
        tk.Label(textvar=self.board_text, font='TkFixedFont',
                 width=self.game.board.width*2, height=self.game.board.height)\
            .grid(row=0, column=0, rowspan=8, padx=(16, 8), pady=16)

        stats_frame = ttk.Labelframe(self.tk, text="Statistics")
        stats_frame.grid(row=0, column=1, padx=(8, 16), pady=(16, 8), sticky='nesw')

        self.stats_text = tk.StringVar()
        ttk.Label(stats_frame, textvar=self.stats_text, justify='left')\
            .grid(row=0, column=0, padx=2, pady=2, sticky='nw')

        flow_settings_frame = ttk.LabelFrame(self.tk, text="Control")
        flow_settings_frame.grid(row=1, column=1, padx=(8, 16), pady=8, sticky='nesw')
        flow_settings_frame.columnconfigure(0, weight=1)
        flow_settings_frame.columnconfigure(1, weight=1)

        self.play = tk.IntVar(value=True)

        ttk.Checkbutton(flow_settings_frame, text="▷ Play", var=self.play) \
            .grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky='ew')

        ttk.Button(flow_settings_frame, text="↺ Reset", command=self.reset)\
            .grid(row=1, column=0, padx=2, pady=2, sticky='ew')

        ttk.Button(flow_settings_frame, text="↷ Step", command=self.move) \
            .grid(row=1, column=1, padx=2, pady=2, sticky='ew')

        next_block_frame = ttk.Labelframe(self.tk, text="Next block")
        next_block_frame.grid(row=2, column=1, padx=(8, 16), pady=8, sticky='nesw')
        next_block_frame.rowconfigure(0, weight=1)
        next_block_frame.columnconfigure(0, weight=1)

        self.next_block_text = tk.StringVar()
        tk.Label(next_block_frame, textvar=self.next_block_text, font='TkFixedFont', width=8, height=2)\
            .grid(row=0, column=0, padx=2, pady=2)

        control_frame = ttk.Labelframe(self.tk, text="AI settings (do not change)")
        control_frame.grid(row=3, column=1, padx=(8, 16), pady=(8, 16), sticky='nesw')
        control_frame.columnconfigure(1, weight=1)

        self.aggregate_height_weight = tk.DoubleVar(value=self.game.ai.aggregate_height_weight)
        ttk.Label(control_frame, text="Height (N): ")\
            .grid(row=0, column=0, padx=2, pady=2, sticky='w')
        ttk.Scale(control_frame, from_=-2, to=2, var=self.aggregate_height_weight)\
            .grid(row=0, column=1, padx=2, pady=2, sticky='ew')

        self.lines_weight = tk.DoubleVar(value=self.game.ai.complete_lines_weight)
        ttk.Label(control_frame, text="Lines (P): ") \
            .grid(row=1, column=0, padx=2, pady=2, sticky='w')
        ttk.Scale(control_frame, from_=-2, to=2, var=self.lines_weight) \
            .grid(row=1, column=1, padx=2, pady=2, sticky='ew')

        self.holes_weight = tk.DoubleVar(value=self.game.ai.holes_weight)
        ttk.Label(control_frame, text="Holes (N): ") \
            .grid(row=2, column=0, padx=2, pady=2, sticky='w')
        ttk.Scale(control_frame, from_=-2, to=2, var=self.holes_weight) \
            .grid(row=2, column=1, padx=2, pady=2, sticky='ew')

        self.bumpiness_weight = tk.DoubleVar(value=self.game.ai.bumpiness_weight)
        ttk.Label(control_frame, text="Diff (N): ") \
            .grid(row=3, column=0, padx=2, pady=2, sticky='w')
        ttk.Scale(control_frame, from_=-2, to=2, var=self.bumpiness_weight) \
            .grid(row=3, column=1, padx=2, pady=2, sticky='ew')

        ttk.Button(control_frame, text="Defaults", command=self.reset_weights)\
            .grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky='e')

        self.update_display()

    def reset_weights(self):
        self.aggregate_height_weight.set(self.game.ai.default_aggregate_height_weight)
        self.holes_weight.set(self.game.ai.default_holes_weight)
        self.bumpiness_weight.set(self.game.ai.default_bumpiness_weight)
        self.lines_weight.set(self.game.ai.default_complete_lines_weight)

    def reset(self):
        self.game = TetrisGame()
        self.update_display()

    def update_display(self):
        self.board_text.set(self.game.board)
        self.next_block_text.set(self.game.piece_generator.current_piece)
        self.stats_text.set(
            "Rows cleared: {board.rows_cleared}\n"
            "Moves: {board.moves}\n"
            "Moves per second: {moves_per_second}\n"
            "Debug data: {board.aggregate_height}-{board.complete_lines}-{board.holes}-{board.bumpiness}"
            "".format(self=self, board=self.game.board,
                      moves_per_second=round(self.game.get_moves_per_second(), 1))
        )

    def move(self):
        try:
            self.game.move()
        except GameOver:
            self.game_over()

        self.update_display()

    def update(self):
        self.game.ai.aggregate_height_weight = self.aggregate_height_weight.get()
        self.game.ai.complete_lines_weight = self.lines_weight.get()
        self.game.ai.holes_weight = self.holes_weight.get()
        self.game.ai.bumpiness_weight = self.bumpiness_weight.get()
        if self.play.get():
            self.move()

    def main_loop(self):
        while True:
            self.update()
            try:
                self.tk.update()
            except tk.TclError:
                break

    def game_over(self):
        tk.messagebox.showerror("AI lose", "AI lose\nYou broke it!")
        self.reset()

if __name__ == '__main__':
    TkTetrisDisplay().main_loop()
