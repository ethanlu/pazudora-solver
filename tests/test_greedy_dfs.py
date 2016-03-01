from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudorasolver.board import Board
from pazudorasolver.heuristics.greedy_dfs import GreedyDfs

import pytest


@pytest.fixture(scope='module')
def weights():
    return {Fire.symbol: 1.0,
            Wood.symbol: 1.0,
            Water.symbol: 1.0,
            Dark.symbol: 1.0,
            Light.symbol: 1.0,
            Heart.symbol: 1.0,
            Poison.symbol: .5,
            Jammer.symbol: .5,
            Unknown.symbol: 0.1}


def test_greedy_dfs(weights):
    def compare(original, final, moves, row, column, assert_error_message):
        for delta_r, delta_c in moves:
            original.swap(row, column, row + delta_r, column + delta_c)
            row += delta_r
            column += delta_c

        for r in range(original.rows):
            for c in range(original.columns):
                assert isinstance(original.cell(r, c), type(final.cell(r, c))), assert_error_message

    # solution should contain move list that gets you to the final board state starting from original board state
    original = Board.create_randomized_board(5, 6)
    _, moves, final_board = GreedyDfs(weights).solve(original, 20)
    compare(original, final_board, moves[1:], moves[0][0], moves[0][1], "Greedy DFS yielded an incorrect 4-way move list!")

    # same with diagonals enabled
    original = Board.create_randomized_board(5, 6)
    h = GreedyDfs(weights)
    h.diagonals = True
    _, moves, final_board = h.solve(original, 20)
    compare(original, final_board, moves[1:], moves[0][0], moves[0][1], "Greedy DFS yielded an incorrect 8-way move list!")
