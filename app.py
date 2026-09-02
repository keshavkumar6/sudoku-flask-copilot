from flask import Flask, jsonify, render_template, request
from game_service import SudokuGameService
from sudoku_generator import SIZE

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
GAME = SudokuGameService()


def get_board_from_request():
    data = request.get_json(silent=True)
    board = data.get('board') if isinstance(data, dict) else None
    if not isinstance(board, list) or len(board) != SIZE:
        raise ValueError('Board must contain 9 rows.')
    if any(not isinstance(row, list) or len(row) != SIZE for row in board):
        raise ValueError('Each board row must contain 9 cells.')
    if any(not isinstance(value, int) or value < 0 or value > SIZE for row in board for value in row):
        raise ValueError('Board cells must be integers from 0 to 9.')
    return board

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium').lower()
    clues_value = request.args.get('clues')

    try:
        if clues_value is not None:
            clues = int(clues_value)
            puzzle, solution = GAME.new_game(clues=clues)
        else:
            puzzle, solution = GAME.new_game(difficulty=difficulty)
    except ValueError:
        return jsonify({'error': 'Invalid difficulty or clues value'}), 400

    return jsonify({'puzzle': puzzle, 'solution': solution, 'difficulty': difficulty, 'hints_used': GAME.hints_used})


@app.route('/hint', methods=['POST'])
def hint_solution():
    try:
        board = get_board_from_request()
        row, col, value, hints_used = GAME.get_hint(board)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    return jsonify({'row': row, 'col': col, 'value': value, 'hints_used': hints_used})


@app.route('/check', methods=['POST'])
def check_solution():
    try:
        board = get_board_from_request()
        incorrect, solved = GAME.check(board)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    return jsonify({'incorrect': incorrect, 'solved': solved})

if __name__ == '__main__':
    app.run(debug=True)