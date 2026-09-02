from sudoku_generator import EMPTY, SIZE, generate_puzzle
from sudoku_validator import (
    get_hint_move,
    get_incorrect_positions,
    is_board_complete_and_correct,
)


class SudokuGameService:
    def __init__(self):
        self.puzzle = None
        self.solution = None
        self.hints_used = 0

    def new_game(self, difficulty=None, clues=None):
        puzzle, solution = generate_puzzle(difficulty=difficulty, clues=clues)
        self.puzzle = puzzle
        self.solution = solution
        self.hints_used = 0
        return puzzle, solution

    def require_game(self):
        if self.puzzle is None or self.solution is None:
            raise ValueError('No game in progress')

    def fixed_positions(self):
        self.require_game()
        return {
            (row, col)
            for row in range(SIZE)
            for col in range(SIZE)
            if self.puzzle[row][col] != EMPTY
        }

    def get_hint(self, board):
        self.require_game()
        move = get_hint_move(board, self.solution, self.fixed_positions())
        if move is None:
            raise ValueError('No available hint')

        row, col = move
        self.hints_used += 1
        return row, col, self.solution[row][col], self.hints_used

    def check(self, board):
        self.require_game()
        fixed = self.fixed_positions()
        incorrect = get_incorrect_positions(board, self.solution, fixed)
        solved = is_board_complete_and_correct(board, self.solution)
        return incorrect, solved
