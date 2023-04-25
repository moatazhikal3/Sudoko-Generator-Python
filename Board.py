import pygame
from Cell import Cell
from sudoku_generator import generate_sudoku
from sudoku_generator import SudokuGenerator


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.board = generate_sudoku(9, difficulty)
        self.original_board = [row[:] for row in self.board]
        self.cells = [[Cell(self.board[row][col], row, col, screen) for col in range(9)] for row in range(9)]
        self.selected_cell = None
        self.cell_size = self.cells[0][0].width
        self.sudoku_generator = SudokuGenerator(9, difficulty)

    def draw(self):
        # Draw grid lines
        for i in range(10):
            thickness = 4 if i % 3 == 0 else 1  # Bold lines for 3x3 boxes
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (self.width // 1, i * self.cell_size),
                             thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_size, 0), (i * self.cell_size, self.height // 1.25),
                             thickness)

        # Draw cells
        for i in range(9):
            for j in range(9):
                cell_rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (0, 255, 255), cell_rect, 1)
                self.cells[i][j].draw()

    def select_cell(self, row, col):
        if self.selected_cell:
            self.cells[self.selected_cell[0]][self.selected_cell[1]].selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)

    def click(self, x, y):
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < 9 and 0 <= col < 9:
            return row, col
        else:
            return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].value is not None and not self.cells[row][col].readonly:
                self.cells[row][col].set_cell_value(None)
                self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if value == 0:
                self.cells[row][col].set_sketched_value(0)
            elif 1 <= value <= 9:
                self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].value is not None and not self.cells[row][col].readonly:
                self.cells[row][col].set_cell_value(value)

    def reset_to_original(self):
        self.board = [row[:] for row in self.original_board]
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set_cell_value(self.board[i][j])
                self.cells[i][j].set_sketched_value(0)

    def is_full(self):
        """
        Returns True if the board is full and False otherwise
        """
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return False
        return True

    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = self.cells[i][j].value

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def check_board(self):
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                if value != 0:
                    # Set the current cell value to 0 to avoid conflict when checking the validity
                    self.board[row][col] = 0
                    if not self.sudoku_generator.is_valid(row, col, value):
                        # Set the cell value back to its original value if the check is invalid
                        self.board[row][col] = value
                        return False
                    # Set the cell value back to its original value after checking
                    self.board[row][col] = value
        return True

    # def check_board(self):
    #     # Check rows
    #     for row in range(9):
    #         values = set()
    #         for col in range(9):
    #             if self.board[row][col] in values:
    #                 return False
    #             values.add(self.board[row][col])
    #     # Check columns
    #     for col in range(9):
    #         values = set()
    #         for row in range(9):
    #             if self.board[row][col] in values:
    #                 return False
    #             values.add(self.board[row][col])
    #             # Check 3x3 boxes
    #         for box_row in range(0, 9, 3):
    #             for box_col in range(0, 9, 3):
    #                 values = set()
    #                 for row in range(box_row, box_row + 3):
    #                     for col in range(box_col, box_col + 3):
    #                         if self.board[row][col] in values:
    #                             return False
    #                         values.add(self.board[row][col])
    #         return True
