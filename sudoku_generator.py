import copy
import random

SIZE = 9
EMPTY = 0

DIFFICULTY_LEVELS = {
    'easy': 45,
    'medium': 36,
    'hard': 27,
}


def get_difficulty_clues(difficulty):
    normalized = (difficulty or 'medium').lower()
    if normalized not in DIFFICULTY_LEVELS:
        valid = ', '.join(sorted(DIFFICULTY_LEVELS))
        raise ValueError(f'Difficulty must be one of: {valid}')
    return DIFFICULTY_LEVELS[normalized]


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    for index in range(SIZE):
        if board[row][index] == num or board[index][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for row_offset in range(3):
        for col_offset in range(3):
            if board[start_row + row_offset][start_col + col_offset] == num:
                return False
    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def count_solutions(board, limit=2):
    """Count solutions up to a limit so puzzle uniqueness can be checked."""
    working = deep_copy(board)
    solutions = 0

    def backtrack():
        nonlocal solutions
        if solutions >= limit:
            return

        for row in range(SIZE):
            for col in range(SIZE):
                if working[row][col] == EMPTY:
                    for candidate in random.sample(range(1, SIZE + 1), SIZE):
                        if is_safe(working, row, col, candidate):
                            working[row][col] = candidate
                            backtrack()
                            working[row][col] = EMPTY
                            if solutions >= limit:
                                return
                    return

        solutions += 1

    backtrack()
    return solutions


def remove_cells(board, clues):
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)

    while sum(cell != EMPTY for row in board for cell in row) > clues:
        removed_any = False
        for row, col in positions:
            if board[row][col] == EMPTY:
                continue

            current = board[row][col]
            board[row][col] = EMPTY
            if count_solutions(board, limit=2) == 1:
                removed_any = True
                if sum(cell != EMPTY for row in board for cell in row) == clues:
                    return
            else:
                board[row][col] = current

        if not removed_any:
            break


def generate_puzzle(clues=None, difficulty=None):
    if difficulty is not None:
        clues = get_difficulty_clues(difficulty)
    elif clues is None:
        clues = DIFFICULTY_LEVELS['medium']

    min_clues = 17
    max_clues = SIZE * SIZE
    if clues < min_clues:
        clues = min_clues
    if clues > max_clues:
        clues = max_clues

    for _ in range(200):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        puzzle = deep_copy(board)
        remove_cells(puzzle, clues)

        if count_solutions(puzzle, limit=2) == 1 and sum(cell != EMPTY for row in puzzle for cell in row) == clues:
            return puzzle, solution

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    puzzle = deep_copy(board)
    remove_cells(puzzle, min_clues)
    if count_solutions(puzzle, limit=2) != 1:
        raise ValueError('Unable to generate a uniquely solvable Sudoku puzzle.')
    return puzzle, solution
