import tkinter as tk
import random

class Tetris:
    FIELD_WIDTH = 10
    FIELD_HEIGHT = 20
    BLOCK_SIZE = 30
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 0, 1]],  # J
        [[1, 1, 0], [0, 1, 1]],  # S
        [[0, 1, 1], [1, 1, 0]]  # Z
    ]
    COLORS = ['cyan', 'yellow', 'purple', 'orange', 'blue', 'green', 'red']

    def __init__(self):
        # Create the main window and canvas
        self.root = tk.Tk()
        self.root.title('Tetris')
        self.canvas = tk.Canvas(
            self.root,
            width=self.FIELD_WIDTH * self.BLOCK_SIZE,
            height=self.FIELD_HEIGHT * self.BLOCK_SIZE,
            bg='black'
        )
        self.canvas.pack(padx=10, pady=10)

        # Initialize the game field and state
        self.field = [[None] * self.FIELD_WIDTH for _ in range(self.FIELD_HEIGHT)]
        self.game_over = False
        self.new_shape()
        self.draw()
        self.root.mainloop()

    def new_shape(self):
        # Create a new shape
        shape_idx = random.randint(0, len(self.SHAPES) - 1)
        self.current_shape = self.SHAPES[shape_idx]
        self.current_color = self.COLORS[shape_idx]
        self.current_x = self.FIELD_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_y = 0

        # Check if the new shape fits, else end the game
        if not self.is_valid_move(self.current_x, self.current_y):
            self.game_over = True
            self.root.destroy()

    def draw(self):
        # Clear the canvas
        self.canvas.delete('all')

        # Draw fixed blocks
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        x * self.BLOCK_SIZE, y * self.BLOCK_SIZE,
                        (x + 1) * self.BLOCK_SIZE, (y + 1) * self.BLOCK_SIZE,
                        fill=cell, outline='gray'
                    )

        # Draw the current shape
        if self.current_shape:
            for y, row in enumerate(self.current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.canvas.create_rectangle(
                            (self.current_x + x) * self.BLOCK_SIZE,
                            (self.current_y + y) * self.BLOCK_SIZE,
                            (self.current_x + x + 1) * self.BLOCK_SIZE,
                            (self.current_y + y + 1) * self.BLOCK_SIZE,
                            fill=self.current_color, outline='gray'
                        )

    def is_valid_move(self, new_x, new_y, shape=None):
        # Check if the move is valid
        if shape is None:
            shape = self.current_shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if (new_x + x < 0 or
                            new_x + x >= self.FIELD_WIDTH or
                            new_y + y >= self.FIELD_HEIGHT or
                            (new_y + y >= 0 and self.field[new_y + y][new_x + x] is not None)):
                        return False
        return True

if __name__ == '__main__':
    Tetris()