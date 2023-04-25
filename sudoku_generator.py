import math
import random


class SudokuGenerator:

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * row_length for _ in range(row_length)]

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)
        print()

    def valid_in_row(self, row_index, num):
        row = self.board[row_index]
        count = row.count(num)
        if count > 0:
            # 'true' if. Contain
            return True
        else:
            # 'false' if. Does not contain
            return False

    def valid_in_col(self, col, num):
        for i in range(self.row_length):
            if self.board[i][col] == num:
                return True
        return False

    def valid_in_box(self, row, col, num):

        if row == 2 or row == 5 or row == 8:
            row = row - 2
        elif row == 1 or row == 4 or row == 7:
            row = row - 1

        if col == 2 or col == 5 or col == 8:
            col = col - 2
        elif col == 1 or col == 4 or col == 7:
            col = col - 1

        box_size = int(math.sqrt(self.row_length))
        for i in range(box_size):
            for j in range(box_size):
                row_length = row + i
                col_length = col + j
                if self.board[row_length][col_length] == num:
                    return True
        return False

    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num) and not self.valid_in_col(col, num) and not self.valid_in_box(row, col, num):
            return False
        else:
            return True

    def fill_box(self, row_start, col_start):
        for i in range(3):
            for j in range(3):
                while True:
                    num = random.randint(1, 9)
                    if not self.valid_in_box(row_start + i, col_start + j, num):
                        self.board[row_start + i][col_start + j] = num
                        break

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

        """
Fills the three boxes along the main diagonal of the board
These are the boxes which start at (0,0), (3,3), and (6,6)

Parameters: None
Return: None
"""

    def fill_remaining(self, row, col):
        if col >= self.row_length:
            row += 1
            col = 0
        if row >= self.row_length:
            return True

        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, self.row_length + 1):
            if not self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, 0)
        """
    Constructs a solution by calling fill_diagonal and fill_remaining

    Parameters: None
    Return: None
    """

    def remove_cells(self):
        count = self.removed_cells
        while count != 0:
            cell_num = random.randint(0, self.row_length * self.row_length - 1)
            row = cell_num // self.row_length
            col = cell_num % self.row_length
            if self.board[row][col] != 0:
                count -= 1
                self.board[row][col] = 0


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.print_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
