from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'hints_used': 0,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium')
    clues_value = request.args.get('clues')

    try:
        if clues_value is not None:
            clues = int(clues_value)
            puzzle, solution = sudoku_logic.generate_puzzle(clues=clues)
        else:
            puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)
    except ValueError:
        return jsonify({'error': 'Invalid difficulty'}), 400

    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['hints_used'] = 0
    return jsonify({'puzzle': puzzle, 'solution': solution, 'difficulty': difficulty, 'hints_used': CURRENT['hints_used']})


@app.route('/hint', methods=['POST'])
def hint_solution():
    data = request.json
    board = data.get('board') if data else None
    if board is None:
        return jsonify({'error': 'Board is required'}), 400

    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    fixed_positions = {
        (row, col)
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
        if puzzle[row][col] != sudoku_logic.EMPTY
    }

    hint_move = sudoku_logic.get_hint_move(board, solution, fixed_positions=fixed_positions)
    if hint_move is None:
        return jsonify({'error': 'No available hint'}), 400

    row, col = hint_move
    CURRENT['hints_used'] = CURRENT.get('hints_used', 0) + 1
    board[row][col] = solution[row][col]
    return jsonify({'row': row, 'col': col, 'value': solution[row][col], 'hints_used': CURRENT['hints_used']})


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    if board is None:
        return jsonify({'error': 'Board is required'}), 400

    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400

    fixed_positions = {
        (row, col)
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
        if puzzle[row][col] != sudoku_logic.EMPTY
    }

    incorrect = sudoku_logic.get_invalid_positions(board, fixed_positions=fixed_positions)
    solved = sudoku_logic.is_board_complete_and_correct(board, solution)
    return jsonify({'incorrect': incorrect, 'solved': solved})

if __name__ == '__main__':
    app.run(debug=True)