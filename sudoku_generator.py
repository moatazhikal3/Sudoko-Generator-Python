import math
import random


class SudokuGenerator:
    def __init__(self, row_length, removed_cells, board=None):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0] * row_length for _ in range(row_length)]
        self.box_length = int(math.sqrt(row_length))

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def unused_in_row(self, row, num):
        return num not in self.board[row]

    def unused_in_col(self, col, num):
        return num not in [row[col] for row in self.board]

    def unused_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                if self.board[row][col] == num:
                    return False
        return True

    def check_if_safe(self, row, col, num):
        return (
                self.unused_in_row(row, num)
                and self.unused_in_col(col, num)
                and self.unused_in_box(
            row - row % self.box_length, col - col % self.box_length, num
        )
        )

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        index = 0
        for row in range(row_start, row_start + self.box_length):
            for col in range(col_start, col_start + self.box_length):
                self.board[row][col] = nums[index]
                index += 1

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if col >= self.row_length:
            row += 1
            col = 0
        if row >= self.row_length:
            return True

        if self.board[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, self.row_length + 1):
            if self.check_if_safe(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

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
    # #
    # sudoku.print_board()
    # print()
    # #
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board
