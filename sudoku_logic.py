"""Compatibility exports for the modular Sudoku implementation."""

from leaderboard import update_leaderboard
from sudoku_generator import (
    DIFFICULTY_LEVELS,
    EMPTY,
    SIZE,
    count_solutions,
    create_empty_board,
    deep_copy,
    fill_board,
    generate_puzzle,
    get_difficulty_clues,
    is_safe,
)
from sudoku_validator import (
    get_hint_move,
    get_incorrect_positions,
    get_invalid_positions,
    is_board_complete_and_correct,
    is_valid_move,
)

__all__ = [
    'DIFFICULTY_LEVELS', 'EMPTY', 'SIZE', 'count_solutions',
    'create_empty_board', 'deep_copy', 'fill_board', 'generate_puzzle',
    'get_difficulty_clues', 'get_hint_move', 'get_incorrect_positions',
    'get_invalid_positions', 'is_board_complete_and_correct', 'is_safe',
    'is_valid_move', 'update_leaderboard',
]
