import tkinter as tk
from tkinter import messagebox
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
        self.root = tk.Tk()
        self.root.title('Тетріс')
        self.root.resizable(False, False)

        # Створюємо основне ігрове поле
        self.canvas = tk.Canvas(
            self.root,
            width=self.FIELD_WIDTH * self.BLOCK_SIZE,
            height=self.FIELD_HEIGHT * self.BLOCK_SIZE,
            bg='black'
        )
        self.canvas.pack(side='left', padx=10, pady=10)

        # Створюємо бічну панель
        self.side_panel = tk.Frame(self.root)
        self.side_panel.pack(side='left', padx=10)

        # Показ наступної фігури
        self.next_shape_canvas = tk.Canvas(
            self.side_panel,
            width=4 * self.BLOCK_SIZE,
            height=4 * self.BLOCK_SIZE,
            bg='white'
        )
        self.next_shape_canvas.pack()

        # Рахунок
        self.score_var = tk.StringVar(value="Рахунок:0")
        self.score_label = tk.Label(
            self.side_panel,
            textvariable=self.score_var,
            font=('Arial', 14)
        )
        self.score_label.pack(pady=10)

        # Кнопка нової гри
        self.new_game_btn = tk.Button(
            self.side_panel,
            text="Нова гра",
            command=self.new_game
        )
        self.new_game_btn.pack(pady=10)

        # Управління
        self.root.bind('<Left>', lambda e: self.move(-1, 0))
        self.root.bind('<Right>', lambda e: self.move(1, 0))
        self.root.bind('<Down>', lambda e: self.move(0, 1))
        self.root.bind('<Up>', lambda e: self.rotate())
        self.root.bind('<space>', lambda e: self.drop())
        self.root.bind('<a>', lambda e: self.move(-1, 0))
        self.root.bind('<d>', lambda e: self.move(1, 0))
        self.root.bind('<s>', lambda e: self.move(0, 1))
        self.root.bind('<w>', lambda e: self.rotate())
        self.root.bind('<space>', lambda e: self.drop())

        self.new_game()
        self.update()
        self.root.mainloop()

    def new_game(self):
        """Почати нову гру"""
        self.field = [[None] * self.FIELD_WIDTH for _ in range(self.FIELD_HEIGHT)]
        self.score = 0
        self.score_var.set(f"Рахунок: {self.score}")
        self.game_over = False
        self.current_shape = None
        self.current_x = 0
        self.current_y = 0
        self.current_color = None
        self.level = 1
        self.speed = 500  # Початкова швидкість падіння (мс)
        self.new_shape()

    def new_shape(self):
        """Створити нову фігуру"""
        if self.current_shape is not None:
            self.next_shape_canvas.delete('all')

        if not hasattr(self, 'next_shape'):
            # Перший запуск
            self.next_shape = random.randint(0, len(self.SHAPES) - 1)
            self.next_color = random.randint(0, len(self.COLORS) - 1)

        self.current_shape = self.SHAPES[self.next_shape]
        self.current_color = self.COLORS[self.next_color]

        # Підготовка наступної фігури
        self.next_shape = random.randint(0, len(self.SHAPES) - 1)
        self.next_color = random.randint(0, len(self.COLORS) - 1)

        # Відображення наступної фігури
        self.draw_next_shape()

        # Розміщення нової фігури звурху поля
        self.current_y = 0
        self.current_x = self.FIELD_WIDTH // 2 - len(self.current_shape[0]) // 2

        if not self.is_valid_move(self.current_x, self.current_y):
            self.game_over = True
            messagebox.showinfo("Гра закінчена!", f"Ваш рахунок: {self.score}")
            self.new_game()

    def draw_next_shape(self):
        """Відобразити наступну фігуру"""
        self.next_shape_canvas.delete('all')
        shape = self.SHAPES[self.next_shape]
        color = self.COLORS[self.next_color]

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.next_shape_canvas.create_rectangle(
                        x * self.BLOCK_SIZE + 10,
                        y * self.BLOCK_SIZE + 10,
                        (x + 1) * self.BLOCK_SIZE + 10,
                        (y + 1) * self.BLOCK_SIZE + 10,
                        fill=color,
                        outline='gray'
                    )

    def draw(self):
        """Відтворити ігрове поле"""
        self.canvas.delete('all')

        # Відображення зафіксованих фігур
        for y, row in enumerate(self.field):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(x, y, cell)

        # Відображення поточної фігури
        if self.current_shape:
            for y, row in enumerate(self.current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_block(
                            self.current_x + x,
                            self.current_y + y,
                            self.current_color
                        )

    def draw_block(self, x, y, color):
        """Відобразити один блок"""
        self.canvas.create_rectangle(
            x * self.BLOCK_SIZE,
            y * self.BLOCK_SIZE,
            (x + 1) * self.BLOCK_SIZE,
            (y + 1) * self.BLOCK_SIZE,
            fill=color,
            outline='gray'
        )

    def is_valid_move(self, new_x, new_y, shape=None):
        """Перевірити, чи можливе переміщення"""
        if shape is None:
            shape = self.current_shape

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if (new_x + x < 0 or
                            new_x + x >= self.FIELD_WIDTH or
                            new_y + y >= self.FIELD_HEIGHT or
                            (new_y + y >= 0 and
                             self.field[new_y + y][new_x + x] is not None)):
                        return False
        return True

    def move(self, dx, dy):
        """Перемістити поточну фігуру"""
        if not self.game_over and self.is_valid_move(self.current_x + dx, self.current_y + dy):
            self.current_x += dx
            self.current_y += dy
            self.draw()
            return True
        return False

    def rotate(self):
        """Повернути поточну фігуру"""
        if self.game_over:
            return

        # Отримуємо перевернуту фігуру
        new_shape = list(zip(*reversed(self.current_shape)))

        if self.is_valid_move(self.current_x, self.current_y, new_shape):
            self.current_shape = new_shape
            self.draw()

    def drop(self):
        """Скинути фігуру вниз"""
        if self.game_over:
            return

        while self.move(0, 1):
            pass
        self.freeze()

    def freeze(self):
        """Зафіксувати фігуру"""
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.field[self.current_y + y][self.current_x + x] = self.current_color

        self.remove_full_lines()
        self.new_shape()
        self.draw()

    def remove_full_lines(self):
        """Видалити заповненні лінії лінії"""
        lines_to_remove = []
        for y in range(self.FIELD_HEIGHT):
            if all(cell is not None for cell in self.field[y]):
                lines_to_remove.append(y)

        for y in lines_to_remove:
            del self.field[y]
            self.field.insert(0, [None] * self.FIELD_WIDTH)
            self.score += 100 * len(lines_to_remove)
            self.score_var.set(f"Рахунок: {self.score}")

            # Збільшення швидкості кожні 1000 очків
            self.level = self.score // 1000 + 1
            self.speed = max(100, 500 - (self.level - 1) * 50)

    def update(self):
        """Оновлення гри"""
        if not self.game_over:
            if not self.move(0, 1):
                self.freeze()
            self.root.after(self.speed, self.update)


if __name__ == '__main__':
    game = Tetris()