import pytest

from gridgame.model import Cell, Feedback, TicTacToeGameModel, TicTacToeGameModel, NoTakToGameModel, WildGameModel, Pick15GameModel


def test_invalid_symbols_exception():
    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=2, player_symbols=['O', 'O'])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=2, player_symbols=['X', 'X'])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=2, player_symbols=['*', '*'])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=2,
                      player_symbols=['X', 'O', 'X'])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=2,
                      player_symbols=['X', 'O', '*', 'X'])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=2,
                      player_symbols=['X', 'O', '*'])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=4,
                      player_symbols=['X', 'O', '*'])


def test_invalid_player_counts():
    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=0, player_symbols=['X', 'O'])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=0, player_symbols=[])

    with pytest.raises(ValueError):
        TicTacToeGameModel(grid_size=3, player_count=1, player_symbols=['O'])


def test_get_player_symbol_correct_2p():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])

    with pytest.raises(ValueError):
        model.get_symbol_choices(0)

    with pytest.raises(ValueError):
        model.get_symbol_choices(3)

    assert model.get_symbol_choices(1) == ['X']
    assert model.get_symbol_choices(2) == ['O']


def test_get_symbol_initial():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    occupied = model.occupied_cells

    for r in range(-10, 11):
        for c in range(-10, 11):
            assert Cell(r, c) not in occupied


def test_get_current_player_initial():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])

    assert model.current_player == 1


def test_place_symbol_out_of_bounds():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])

    assert model.place_symbol('X', Cell(0, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(1, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(0, 1)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(-1, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(0, -1)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(-1, -1)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(0, 4)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(4, 0)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(1, 4)) == Feedback.OUT_OF_BOUNDS
    assert model.place_symbol('X', Cell(4, 1)) == Feedback.OUT_OF_BOUNDS


def test_place_symbol_all_valid():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])

    assert model.place_symbol('X', Cell(1, 1)) == Feedback.VALID
    assert model.place_symbol('O', Cell(2, 2)) == Feedback.VALID
    assert model.place_symbol('X', Cell(3, 3)) == Feedback.VALID

    assert model.occupied_cells[Cell(1, 1)] == 'X'
    assert model.occupied_cells[Cell(2, 2)] == 'O'
    assert model.occupied_cells[Cell(3, 3)] == 'X'


def test_place_symbol_game_over():
    model = TicTacToeGameModel(grid_size=2, player_count=2,
                          player_symbols=['X', 'O'])
    model.place_symbol('X', Cell(1, 1))
    model.place_symbol('O', Cell(2, 2))
    model.place_symbol('X', Cell(1, 2))

    assert model.place_symbol('X', Cell(2, 1)) == Feedback.GAME_OVER
    assert model.place_symbol('O', Cell(2, 2)) == Feedback.GAME_OVER


def test_place_symbol_invalid_symbol():
    model = TicTacToeGameModel(grid_size=2, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.place_symbol('O', Cell(1, 1)) == Feedback.INVALID_SYMBOL
    assert model.place_symbol('?', Cell(1, 1)) == Feedback.INVALID_SYMBOL
    assert model.place_symbol('', Cell(1, 1)) == Feedback.INVALID_SYMBOL
    assert model.place_symbol('X ', Cell(1, 1)) == Feedback.INVALID_SYMBOL
    model.place_symbol('X', Cell(1, 1))
    assert model.place_symbol('X', Cell(2, 2)) == Feedback.INVALID_SYMBOL
    assert model.place_symbol('?', Cell(2, 2)) == Feedback.INVALID_SYMBOL
    assert model.place_symbol('', Cell(2, 2)) == Feedback.INVALID_SYMBOL
    assert model.place_symbol('O ', Cell(1, 1)) == Feedback.INVALID_SYMBOL
    model.place_symbol('O', Cell(2, 2))
    model.place_symbol('X', Cell(1, 2))


def test_get_player_count():
    assert TicTacToeGameModel(grid_size=3, player_count=2, player_symbols=[
        'X', 'O'
    ]).player_count == 2

    assert TicTacToeGameModel(grid_size=3, player_count=3, player_symbols=[
                         'X', '*', 'O']).player_count == 3


def test_get_next_player_initial():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['O', 'X'])

    assert model.next_player == 2


def test_get_next_player_multiple_2_all_valid():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['O', 'X'])

    assert model.next_player == 2
    model.place_symbol('O', Cell(1, 1))
    assert model.next_player == 1
    model.place_symbol('X', Cell(2, 2))
    assert model.next_player == 2
    model.place_symbol('O', Cell(2, 1))
    assert model.next_player == 1


def test_get_next_player_multiple_2_with_errors():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['O', 'X'])

    assert model.next_player == 2
    model.place_symbol('O', Cell(1, 1))
    assert model.next_player == 1
    model.place_symbol('X', Cell(1, 1))
    assert model.next_player == 1
    model.place_symbol('X', Cell(2, 2))
    assert model.next_player == 2
    model.place_symbol('O', Cell(-1, -1))
    model.place_symbol('O', Cell(-1, -1))
    model.place_symbol('O', Cell(0, 0))
    model.place_symbol('O', Cell(4, 1))
    assert model.next_player == 2
    model.place_symbol('O', Cell(1, 3))
    assert model.next_player == 1
    model.place_symbol('X', Cell(1, 3))
    model.place_symbol('X', Cell(1, 3))
    model.place_symbol('X', Cell(1, 3))
    assert model.next_player == 1


def test_get_next_player_multiple_3_all_valid():
    model = TicTacToeGameModel(grid_size=3, player_count=3,
                          player_symbols=['O', 'X', '*'])

    assert model.next_player == 2
    model.place_symbol('O', Cell(1, 1))
    assert model.next_player == 3
    model.place_symbol('X', Cell(2, 2))
    assert model.next_player == 1
    model.place_symbol('*', Cell(2, 1))
    assert model.next_player == 2
    model.place_symbol('O', Cell(3, 3))
    assert model.next_player == 3
    model.place_symbol('X', Cell(3, 2))
    assert model.next_player == 1


def test_get_next_player_multiple_3_with_errors():
    model = TicTacToeGameModel(grid_size=3, player_count=3,
                          player_symbols=['O', 'X', '*'])

    assert model.next_player == 2
    model.place_symbol('O', Cell(1, 1))
    assert model.next_player == 3
    model.place_symbol('X', Cell(1, 2))
    assert model.next_player == 1
    model.place_symbol('*', Cell(2, 2))
    assert model.next_player == 2
    model.place_symbol('O', Cell(-1, -1))
    model.place_symbol('O', Cell(-1, -1))
    model.place_symbol('O', Cell(0, 0))
    model.place_symbol('O', Cell(4, 1))
    assert model.next_player == 2
    model.place_symbol('O', Cell(1, 3))
    assert model.next_player == 3
    model.place_symbol('X', Cell(1, 3))
    model.place_symbol('X', Cell(1, 3))
    model.place_symbol('X', Cell(1, 3))
    assert model.next_player == 3


def test_is_game_over_2():
    model = TicTacToeGameModel(grid_size=2, player_count=2,
                          player_symbols=['O', 'X'])
    assert not model.is_game_over

    model.place_symbol('O', Cell(1, 1))
    assert not model.is_game_over
    model.place_symbol('X', Cell(2, 2))
    assert not model.is_game_over
    model.place_symbol('O', Cell(1, 2))
    assert model.is_game_over


def test_get_winner_2():
    model = TicTacToeGameModel(grid_size=2, player_count=2,
                          player_symbols=['O', 'X'])
    assert model.winner is None

    model.place_symbol('O', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 2))
    assert model.winner == 1

    # Invalid move
    model.place_symbol('X', Cell(2, 1))
    assert model.winner == 1


def test_get_winner_3_backslash():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 3))
    assert model.winner == 1


def test_get_winner_3_forward_slash():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 3))
    assert model.winner is None
    model.place_symbol('X', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(3, 1))
    assert model.winner == 2


def test_get_winner_3_row_1():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(1, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(1, 3))
    assert model.winner == 1


def test_get_winner_3_row_2():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(2, 3))
    assert model.winner == 1


def test_get_winner_3_row_3():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(3, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 3))
    assert model.winner == 1


def test_get_winner_3_col_1():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 3))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(1, 3))
    assert model.winner is None
    model.place_symbol('O', Cell(3, 1))
    assert model.winner == 2


def test_get_winner_3_col_2():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 3))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(1, 3))
    assert model.winner is None
    model.place_symbol('O', Cell(3, 2))
    assert model.winner == 2


def test_get_winner_3_col_3():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 3))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 3))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(3, 3))
    assert model.winner == 2


def test_get_winner_draw_3():
    model = TicTacToeGameModel(grid_size=3, player_count=2,
                          player_symbols=['X', 'O'])
    assert model.winner is None

    model.place_symbol('X', Cell(2, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(1, 2))
    assert model.winner is None
    model.place_symbol('O', Cell(3, 2))
    assert model.winner is None
    model.place_symbol('X', Cell(2, 3))
    assert model.winner is None
    model.place_symbol('O', Cell(2, 1))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 1))
    assert model.winner is None
    model.place_symbol('O', Cell(1, 3))
    assert model.winner is None
    model.place_symbol('X', Cell(3, 3))
    assert model.winner is None


def test_grid_size():
    assert TicTacToeGameModel(grid_size=2, player_count=2,
                         player_symbols=['O', 'X']).grid_size == 2
    assert TicTacToeGameModel(grid_size=3, player_count=2,
                         player_symbols=['O', 'X']).grid_size == 3
    assert TicTacToeGameModel(grid_size=4, player_count=2,
                         player_symbols=['O', 'X']).grid_size == 4
    assert TicTacToeGameModel(grid_size=5, player_count=2,
                         player_symbols=['O', 'X']).grid_size == 5
    assert TicTacToeGameModel(grid_size=10, player_count=2,
                         player_symbols=['O', 'X']).grid_size == 10
