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
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def is_valid_move(board, row, col, value):
    if value == EMPTY:
        return True

    for x in range(SIZE):
        if x != col and board[row][x] == value:
            return False

    for y in range(SIZE):
        if y != row and board[y][col] == value:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r, c) != (row, col) and board[r][c] == value:
                return False

    return True


def get_invalid_positions(board, fixed_positions=None):
    fixed = set() if fixed_positions is None else set(fixed_positions)
    invalid = []

    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            if value == EMPTY:
                continue
            if (row, col) in fixed:
                continue
            if not is_valid_move(board, row, col, value):
                invalid.append([row, col])

    return invalid


def is_board_complete_and_correct(board, solution):
    if solution is None:
        return False

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return False
            if board[row][col] != solution[row][col]:
                return False

    return True


def get_hint_move(board, solution, fixed_positions=None):
    if solution is None:
        return None

    fixed = set() if fixed_positions is None else set(fixed_positions)
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY and (row, col) not in fixed:
                return row, col
    return None


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
                            if solutions >= limit:
                                working[row][col] = EMPTY
                                return
                            working[row][col] = EMPTY
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
                if sum(cell != EMPTY for row_values in board for cell in row_values) == clues:
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

        if count_solutions(puzzle, limit=2) == 1:
            if sum(cell != EMPTY for row in puzzle for cell in row) == clues:
                return puzzle, solution

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    puzzle = deep_copy(board)
    remove_cells(puzzle, min_clues)
    if count_solutions(puzzle, limit=2) != 1:
        raise ValueError('Unable to generate a uniquely solvable Sudoku puzzle.')
    return puzzle, solution


def update_leaderboard(existing_entries=None, new_entries=None, limit=10):
    all_entries = []
    if existing_entries is not None:
        all_entries.extend(existing_entries)
    if new_entries is not None:
        all_entries.extend(new_entries)

    seen_game_ids = set()
    valid_entries = []

    for entry in all_entries:
        if not isinstance(entry, dict):
            continue

        game_id = entry.get('game_id')
        player_name = str(entry.get('player_name', '')).strip()
        completion_time = entry.get('completion_time')
        difficulty = str(entry.get('difficulty', '')).strip().lower()
        hints_used = entry.get('hints_used')

        if game_id is not None:
            game_key = str(game_id)
            if game_key in seen_game_ids:
                continue
            seen_game_ids.add(game_key)

        if not player_name:
            continue

        try:
            completion_seconds = int(completion_time)
        except (TypeError, ValueError):
            continue
        if completion_seconds < 0:
            continue

        try:
            hint_count = int(hints_used)
        except (TypeError, ValueError):
            continue
        if hint_count < 0:
            continue

        if difficulty not in {'easy', 'medium', 'hard'}:
            continue

        valid_entries.append({
            'game_id': str(game_id) if game_id is not None else '',
            'player_name': player_name,
            'completion_time': completion_seconds,
            'difficulty': difficulty,
            'hints_used': hint_count,
        })

    sorted_entries = sorted(
        valid_entries,
        key=lambda item: (item['completion_time'], item['hints_used'], item['player_name'])
    )
    return sorted_entries[:limit]
