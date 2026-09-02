from sudoku_generator import EMPTY, SIZE


def is_valid_move(board, row, col, value):
    if value == EMPTY:
        return True

    for index in range(SIZE):
        if index != col and board[row][index] == value:
            return False

    for index in range(SIZE):
        if index != row and board[index][col] == value:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for current_row in range(start_row, start_row + 3):
        for current_col in range(start_col, start_col + 3):
            if (current_row, current_col) != (row, col) and board[current_row][current_col] == value:
                return False

    return True


def get_invalid_positions(board, fixed_positions=None):
    fixed = set() if fixed_positions is None else set(fixed_positions)
    invalid = []

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY or (row, col) in fixed:
                continue
            if not is_valid_move(board, row, col, board[row][col]):
                invalid.append([row, col])

    return invalid


def get_incorrect_positions(board, solution, fixed_positions=None):
    """Return editable cells that are blank or do not match the solution."""
    fixed = set() if fixed_positions is None else set(fixed_positions)
    incorrect = []

    for row in range(SIZE):
        for col in range(SIZE):
            if (row, col) not in fixed and board[row][col] != solution[row][col]:
                incorrect.append([row, col])

    return incorrect


def is_board_complete_and_correct(board, solution):
    if solution is None:
        return False

    return all(
        board[row][col] == solution[row][col]
        for row in range(SIZE)
        for col in range(SIZE)
    )


def get_hint_move(board, solution, fixed_positions=None):
    if solution is None:
        return None

    fixed = set() if fixed_positions is None else set(fixed_positions)
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY and (row, col) not in fixed:
                return row, col
    return None
