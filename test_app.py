import app


def test_check_marks_empty_and_wrong_editable_cells_but_not_fixed_cells():
    app.GAME.puzzle = [[0 for _ in range(9)] for _ in range(9)]
    app.GAME.solution = [[1 for _ in range(9)] for _ in range(9)]

    board = [[1 for _ in range(9)] for _ in range(9)]
    board[0][0] = 0
    board[0][1] = 2
    app.GAME.puzzle[0][2] = 1

    client = app.app.test_client()
    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {
        'incorrect': [[0, 0], [0, 1]],
        'solved': False,
    }


def test_board_requests_reject_invalid_shape_and_values():
    client = app.app.test_client()

    missing_board = client.post('/check', json={})
    invalid_value = client.post('/check', json={'board': [[10] * 9 for _ in range(9)]})

    assert missing_board.status_code == 400
    assert missing_board.get_json()['error'] == 'Board must contain 9 rows.'
    assert invalid_value.status_code == 400
    assert invalid_value.get_json()['error'] == 'Board cells must be integers from 0 to 9.'