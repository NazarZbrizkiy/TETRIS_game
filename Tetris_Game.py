import tkinter as tk

class Tetris:
    FIELD_WIDTH = 10
    FIELD_HEIGHT = 20
    BLOCK_SIZE = 30

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
        self.root.mainloop()

if __name__ == '__main__':
    Tetris()