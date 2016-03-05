from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudorasolver.board import Board
from pazudorasolver.heuristics.heuristic import Heuristic
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


@pytest.fixture(scope='module')
def board():
    return Board([Fire,    Unknown, Unknown, Unknown, Dark,    Dark,
                  Fire,    Water,   Unknown, Heart,   Unknown, Dark,
                  Fire,    Water,   Heart,   Heart,   Unknown, Unknown,
                  Unknown, Water,   Unknown, Unknown, Unknown, Unknown,
                  Unknown, Water,   Unknown, Light,   Light,   Light], 5, 6)


def test_abstract_heuristic_exception(weights):
    # should not be able to instantiate base piece class
    with pytest.raises(TypeError) as exec_info:
        Heuristic(weights)
    assert 'abstract class Heuristic' in str(exec_info.value), "Heuristic class not abstract!"


def test_scoring(weights, board):
    # scoring should yield a score using the number of matches found and 10% of a random number
    score = GreedyDfs(weights)._score(board)
    assert 30.0 <= score <= 31.0, "Scoring of board with just matches did not yield expected value between 9.0 and 19.0!"


def test_finding_swaps_4_way(board):
    # diagonal-disabled setup should return 4 possible swaps
    h = GreedyDfs(weights)
    swaps = h._swaps(board, 2, 2)
    assert len(swaps) == 4, "Swaps @ 2,2 did not yield expected swap count of 4!"
    assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (1, 0), (0, -1)]))) == 4, "Swaps @ 2,2 did not yield correct set of deltas!"

    # swapping at corners should yield 2
    swaps = h._swaps(board, 0, 0)
    assert len(swaps) == 2, "Corner swaps @ 0,0 did not yield expected swap count of 2!"
    assert len(set(swaps).intersection(set([(0, 1), (1, 0)]))) == 2, "Corner swaps @ 0,0 did not yield correct set of deltas!"
    swaps = h._swaps(board, 0, 5)
    assert len(swaps) == 2, "Corner swaps @ 0,5 did not yield expected swap count of 2!"
    assert len(set(swaps).intersection(set([(1, 0), (0, -1)]))) == 2, "Corner swaps @ 0,5 did not yield correct set of deltas!"
    swaps = h._swaps(board, 4, 5)
    assert len(swaps) == 2, "Corner swaps @ 4,5 did not yield expected swap count of 2!"
    assert len(set(swaps).intersection(set([(-1, 0), (0, -1)]))) == 2, "Corner swaps @ 4,5 did not yield correct set of deltas!"
    swaps = h._swaps(board, 4, 0)
    assert len(swaps) == 2, "Corner swaps @ 4,0 did not yield expected swap count of 2!"
    assert len(set(swaps).intersection(set([(-1, 0), (0, 1)]))) == 2, "Corner swaps @ 4,0 did not yield correct set of deltas!"

    # swapping at edges should yield 3
    swaps = h._swaps(board, 0, 3)
    assert len(swaps) == 3, "Edge swaps @ 0,3 did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(0, 1), (1, 0), (0, -1)]))) == 3, "Edge swaps @ 0,3 did not yield correct set of deltas!"
    swaps = h._swaps(board, 2, 5)
    assert len(swaps) == 3, "Edge swaps @ 2,5 did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(-1, 0), (1, 0), (0, -1)]))) == 3, "Edge swaps @ 2,5 did not yield correct set of deltas!"
    swaps = h._swaps(board, 4, 3)
    assert len(swaps) == 3, "Edge swaps @ 4,3 did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (0, -1)]))) == 3, "Edge swaps @ 4,3 did not yield correct set of deltas!"
    swaps = h._swaps(board, 2, 0)
    assert len(swaps) == 3, "Edge swaps @ 2,0 did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (1, 0)]))) == 3, "Edge swaps @ 2,0 did not yield correct set of deltas!"


def test_finding_swaps_8_way(board):
    # diagonal-enabled setup should return 8 possible swaps
    h = GreedyDfs(weights)
    h.diagonals = True
    swaps = h._swaps(board, 2, 2)
    assert len(swaps) == 8, "Swaps @ 2,2 (diagonals)did not yield expected swap count of 8!"
    assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 8, \
        "Swaps @ 2,2  did not yield correct set of deltas!"

    # swapping at corners should yield 3
    swaps = h._swaps(board, 0, 0)
    assert len(swaps) == 3, "Corner swaps @ 0,0  did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(0, 1), (1, 1), (1, 0)]))) == 3, "Corner swaps @ 0,0  did not yield correct set of deltas!"
    swaps = h._swaps(board, 0, 5)
    assert len(swaps) == 3, "Corner swaps @ 0,5  did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(1, 0), (1, -1), (0, -1)]))) == 3, "Corner swaps @ 0,5  did not yield correct set of deltas!"
    swaps = h._swaps(board, 4, 5)
    assert len(swaps) == 3, "Corner swaps @ 4,5  did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (0, -1)]))) == 3, "Corner swaps @ 4,5  did not yield correct set of deltas!"
    swaps = h._swaps(board, 4, 0)
    assert len(swaps) == 3, "Corner swaps @ 4,0  did not yield expected swap count of 3!"
    assert len(set(swaps).intersection(set([(-1, 0), (-1, 1), (0, 1)]))) == 3, "Corner swaps @ 4,0  did not yield correct set of deltas!"

    # swapping at edges should yield 5
    swaps = h._swaps(board, 0, 3)
    assert len(swaps) == 5, "Edge swaps @ 0,3  did not yield expected swap count of 5!"
    assert len(set(swaps).intersection(set([(0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 5, "Edge swaps @ 0,3  did not yield correct set of deltas!"
    swaps = h._swaps(board, 2, 5)
    assert len(swaps) == 5, "Edge swaps @ 2,5  did not yield expected swap count of 5!"
    assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (1, 0), (1, -1), (0, -1)]))) == 5, "Edge swaps @ 2,5  did not yield correct set of deltas!"
    swaps = h._swaps(board, 4, 3)
    assert len(swaps) == 5, "Edge swaps @ 4,3  did not yield expected swap count of 5!"
    assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]))) == 5, "Edge swaps @ 4,3  did not yield correct set of deltas!"
    swaps = h._swaps(board, 2, 0)
    assert len(swaps) == 5, "Edge swaps @ 2,0  did not yield expected swap count of 5!"
    assert len(set(swaps).intersection(set([(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]))) == 5, "Edge swaps @ 2,0  did not yield correct set of deltas!"
