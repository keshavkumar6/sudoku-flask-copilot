import pytest

from sudoku_logic import (
    DIFFICULTY_LEVELS,
    EMPTY,
    SIZE,
    count_solutions,
    create_empty_board,
    deep_copy,
    fill_board,
    generate_puzzle,
    get_difficulty_clues,
    get_hint_move,
    get_invalid_positions,
    is_board_complete_and_correct,
    is_safe,
    is_valid_move,
    update_leaderboard,
)


def test_deep_copy_creates_independent_board():
    board = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    copied = deep_copy(board)

    copied[0][0] = 9

    assert board[0][0] == 1
    assert copied[0][0] == 9


def test_create_empty_board_has_9x9_zero_grid():
    board = create_empty_board()

    assert len(board) == SIZE
    assert all(len(row) == SIZE for row in board)
    assert all(cell == EMPTY for row in board for cell in row)


def test_is_safe_detects_conflicts_in_row_column_and_box():
    board = create_empty_board()
    board[0][0] = 5
    board[0][1] = 1
    board[1][0] = 1
    board[1][1] = 5

    assert is_safe(board, 0, 2, 5) is False
    assert is_safe(board, 2, 2, 5) is False
    assert is_safe(board, 2, 2, 7) is True


def test_fill_board_solves_a_blank_board():
    board = create_empty_board()

    assert fill_board(board) is True
    assert all(1 <= value <= SIZE for row in board for value in row)
    assert all(sorted(row) == list(range(1, SIZE + 1)) for row in board)
    assert all(sorted(column) == list(range(1, SIZE + 1)) for column in zip(*board))

    for row_start in range(0, SIZE, 3):
        for col_start in range(0, SIZE, 3):
            values = [
                board[row_start + r][col_start + c]
                for r in range(3)
                for c in range(3)
            ]
            assert sorted(values) == list(range(1, SIZE + 1))


def test_generate_puzzle_returns_valid_puzzle_and_solution():
    clues = 35
    puzzle, solution = generate_puzzle(clues)

    assert len(puzzle) == SIZE
    assert len(solution) == SIZE
    assert all(len(row) == SIZE for row in puzzle)
    assert all(len(row) == SIZE for row in solution)
    assert sum(cell != EMPTY for row in puzzle for cell in row) == clues
    assert all(cell in range(0, SIZE + 1) for row in puzzle for cell in row)
    assert all(cell in range(1, SIZE + 1) for row in solution for cell in row)

    for row in range(SIZE):
        for col in range(SIZE):
            if puzzle[row][col] != EMPTY:
                assert puzzle[row][col] == solution[row][col]


def test_count_solutions_detects_multiple_and_unique_cases():
    empty_board = create_empty_board()
    assert count_solutions(empty_board, limit=2) == 2

    solved_board = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    assert count_solutions(solved_board, limit=2) == 1


def test_generate_puzzle_has_exactly_one_unique_solution():
    for clues in (30, 35, 40):
        puzzle, solution = generate_puzzle(clues)

        assert count_solutions(puzzle, limit=2) == 1
        assert solution is not None
        assert all(cell in range(1, SIZE + 1) for row in solution for cell in row)


def test_is_valid_move_detects_row_column_and_box_conflicts():
    board = create_empty_board()
    board[0][0] = 5
    board[0][1] = 1
    board[1][0] = 1
    board[1][1] = 5

    assert is_valid_move(board, 0, 2, 5) is False
    assert is_valid_move(board, 2, 2, 5) is False
    assert is_valid_move(board, 2, 2, 7) is True


def test_get_hint_move_returns_one_correct_empty_cell():
    puzzle, solution = generate_puzzle(clues=35)
    fixed_positions = {
        (row, col)
        for row in range(SIZE)
        for col in range(SIZE)
        if puzzle[row][col] != EMPTY
    }

    hint = get_hint_move(puzzle, solution, fixed_positions=fixed_positions)

    assert hint is not None
    row, col = hint
    assert puzzle[row][col] == EMPTY
    assert solution[row][col] != EMPTY
    assert (row, col) not in fixed_positions


def test_get_invalid_positions_ignores_prefilled_cells():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    board[0][2] = 5
    fixed_positions = {(0, 0), (0, 1), (0, 4), (1, 0), (1, 3), (1, 4), (1, 5)}

    invalid = get_invalid_positions(board, fixed_positions=fixed_positions)

    assert [0, 2] in invalid
    assert [0, 1] not in invalid
    assert [1, 0] not in invalid
    assert [4, 8] not in invalid


def test_difficulty_levels_are_ordered_and_unique():
    easy_clues = get_difficulty_clues('easy')
    medium_clues = get_difficulty_clues('medium')
    hard_clues = get_difficulty_clues('hard')

    assert easy_clues > medium_clues > hard_clues
    assert DIFFICULTY_LEVELS == {
        'easy': easy_clues,
        'medium': medium_clues,
        'hard': hard_clues,
    }

    for difficulty, clues in DIFFICULTY_LEVELS.items():
        puzzle, solution = generate_puzzle(difficulty=difficulty)

        assert sum(cell != EMPTY for row in puzzle for cell in row) == clues
        assert count_solutions(puzzle, limit=2) == 1
        assert all(cell in range(1, SIZE + 1) for row in solution for cell in row)


def test_is_board_complete_and_correct_only_returns_true_for_fully_solved_board():
    solution = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

    assert is_board_complete_and_correct(solution, solution) is True

    incomplete = deep_copy(solution)
    incomplete[0][0] = EMPTY
    assert is_board_complete_and_correct(incomplete, solution) is False

    incorrect = deep_copy(solution)
    incorrect[0][0] = 1
    assert is_board_complete_and_correct(incorrect, solution) is False


def test_update_leaderboard_keeps_fastest_top_ten_and_removes_invalid_entries():
    existing = [
        {'game_id': 'g1', 'player_name': 'Anna', 'completion_time': 180, 'difficulty': 'easy', 'hints_used': 0},
        {'game_id': 'g2', 'player_name': 'Ben', 'completion_time': 300, 'difficulty': 'medium', 'hints_used': 1},
        {'game_id': 'g3', 'player_name': 'Cara', 'completion_time': 240, 'difficulty': 'hard', 'hints_used': 2},
    ]

    new_entries = [
        {'game_id': 'g4', 'player_name': 'Dana', 'completion_time': 120, 'difficulty': 'easy', 'hints_used': 0},
        {'game_id': 'g5', 'player_name': 'Eli', 'completion_time': 90, 'difficulty': 'medium', 'hints_used': 1},
        {'game_id': 'g6', 'player_name': 'Fran', 'completion_time': 200, 'difficulty': 'hard', 'hints_used': 2},
        {'game_id': 'g5', 'player_name': 'Eli duplicate', 'completion_time': 40, 'difficulty': 'easy', 'hints_used': 0},
        {'game_id': 'g7', 'player_name': '', 'completion_time': 50, 'difficulty': 'easy', 'hints_used': 2},
        {'game_id': 'g8', 'player_name': 'Gio', 'completion_time': -5, 'difficulty': 'easy', 'hints_used': 0},
    ]

    leaderboard = update_leaderboard(existing, new_entries, limit=10)

    assert [entry['player_name'] for entry in leaderboard] == ['Eli', 'Dana', 'Anna', 'Fran', 'Cara', 'Ben']
    assert all(entry['completion_time'] >= 0 for entry in leaderboard)
    assert len(leaderboard) == 6


def test_update_leaderboard_keeps_only_ten_fastest_scores():
    entries = [
        {'game_id': f'g{i}', 'player_name': f'P{i}', 'completion_time': 10 + i * 30, 'difficulty': 'easy', 'hints_used': i % 3}
        for i in range(1, 15)
    ]

    leaderboard = update_leaderboard([], entries, limit=10)

    assert len(leaderboard) == 10
    assert leaderboard[0]['completion_time'] == 40
    assert leaderboard[-1]['completion_time'] == 310
    assert leaderboard == sorted(leaderboard, key=lambda entry: entry['completion_time'])
