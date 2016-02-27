from pazudora_solver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudora_solver.board import Board
from pazudora_solver.heuristics.heuristic import Heuristic
from pazudora_solver.heuristics.greedy_dfs import GreedyDfs

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


class TestHeuristic(object):
    def test_abstract_heuristic_exception(self):
        # should not be able to instantiate base piece class
        with pytest.raises(TypeError) as exec_info:
            Heuristic()
        assert 'abstract class Heuristic' in str(exec_info.value), "Heuristic class not abstract!"

    def test_scoring(self, weights, board):
        # basic scoring should yield just the number of matches multipled by the sum of type weights
        score = GreedyDfs(weights)._score(board)
        assert score == 9.0, "Scoring of board with just matches did not yield expected value of 9.0!"

        # scoring of board at specific locations should include fragment score
        score = GreedyDfs(weights)._score(board, 1, 4)
        assert score == 14.0, "Scoring of board @ 1, 4 did not yield expected value of 14.0!"

    def test_finding_swaps_4_way(self, board):
        # diagonal-disabled setup should return 4 possible swaps
        h = GreedyDfs(weights)
        swaps = h._swaps(board, 2, 2, None)
        assert len(swaps) == 4, "Swaps @ 2,2 did not yield expected swap count of 4!"
        assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (1, 0), (0, -1)]))) == 4, "Swaps @ 2,2 did not yield correct set of deltas!"

        # swapping at corners should yield 2
        swaps = h._swaps(board, 0, 0, None)
        assert len(swaps) == 2, "Corner swaps @ 0,0 did not yield expected swap count of 2!"
        assert len(set(swaps).intersection(set([(0, 1), (1, 0)]))) == 2, "Corner swaps @ 0,0 did not yield correct set of deltas!"
        swaps = h._swaps(board, 0, 5, None)
        assert len(swaps) == 2, "Corner swaps @ 0,5 did not yield expected swap count of 2!"
        assert len(set(swaps).intersection(set([(1, 0), (0, -1)]))) == 2, "Corner swaps @ 0,5 did not yield correct set of deltas!"
        swaps = h._swaps(board, 4, 5, None)
        assert len(swaps) == 2, "Corner swaps @ 4,5 did not yield expected swap count of 2!"
        assert len(set(swaps).intersection(set([(-1, 0), (0, -1)]))) == 2, "Corner swaps @ 4,5 did not yield correct set of deltas!"
        swaps = h._swaps(board, 4, 0, None)
        assert len(swaps) == 2, "Corner swaps @ 4,0 did not yield expected swap count of 2!"
        assert len(set(swaps).intersection(set([(-1, 0), (0, 1)]))) == 2, "Corner swaps @ 4,0 did not yield correct set of deltas!"

        # swapping at edges should yield 3
        swaps = h._swaps(board, 0, 3, None)
        assert len(swaps) == 3, "Edge swaps @ 0,3 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(0, 1), (1, 0), (0, -1)]))) == 3, "Edge swaps @ 0,3 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 5, None)
        assert len(swaps) == 3, "Edge swaps @ 2,5 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, 0), (1, 0), (0, -1)]))) == 3, "Edge swaps @ 2,5 did not yield correct set of deltas!"
        swaps = h._swaps(board, 4, 3, None)
        assert len(swaps) == 3, "Edge swaps @ 4,3 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (0, -1)]))) == 3, "Edge swaps @ 4,3 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 0, None)
        assert len(swaps) == 3, "Edge swaps @ 2,0 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (1, 0)]))) == 3, "Edge swaps @ 2,0 did not yield correct set of deltas!"

        # swapping with previous move should yield 3
        swaps = h._swaps(board, 2, 2, (-1, 0))
        assert len(swaps) == 3, "Swaps @ 2,2 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (0, -1)]))) == 3, "Swaps @ 2,2 and previous move -1,0 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (0, 1))
        assert len(swaps) == 3, "Swaps @ 2,2 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, 0), (0, 1), (1, 0)]))) == 3, "Swaps @ 2,2 and previous move 0,1 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (1, 0))
        assert len(swaps) == 3, "Swaps @ 2,2 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(0, 1), (1, 0), (0, -1)]))) == 3, "Swaps @ 2,2 and previous move 1,0 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (0, -1))
        assert len(swaps) == 3, "Swaps @ 2,2 did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, 0), (1, 0), (0, -1)]))) == 3, "Swaps @ 2,2 and previous move 0,-1 did not yield correct set of deltas!"

    def test_finding_swaps_8_way(self, board):
        # diagonal-enabled setup should return 8 possible swaps
        h = GreedyDfs(weights)
        h.diagonals = True
        swaps = h._swaps(board, 2, 2, None)
        assert len(swaps) == 8, "Swaps @ 2,2 (diagonals)did not yield expected swap count of 8!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 8, "Swaps @ 2,2  did not yield correct set of deltas!"

        # swapping at corners should yield 3
        swaps = h._swaps(board, 0, 0, None)
        assert len(swaps) == 3, "Corner swaps @ 0,0  did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(0, 1), (1, 1), (1, 0)]))) == 3, "Corner swaps @ 0,0  did not yield correct set of deltas!"
        swaps = h._swaps(board, 0, 5, None)
        assert len(swaps) == 3, "Corner swaps @ 0,5  did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(1, 0), (1, -1), (0, -1)]))) == 3, "Corner swaps @ 0,5  did not yield correct set of deltas!"
        swaps = h._swaps(board, 4, 5, None)
        assert len(swaps) == 3, "Corner swaps @ 4,5  did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (0, -1)]))) == 3, "Corner swaps @ 4,5  did not yield correct set of deltas!"
        swaps = h._swaps(board, 4, 0, None)
        assert len(swaps) == 3, "Corner swaps @ 4,0  did not yield expected swap count of 3!"
        assert len(set(swaps).intersection(set([(-1, 0), (-1, 1), (0, 1)]))) == 3, "Corner swaps @ 4,0  did not yield correct set of deltas!"

        # swapping at edges should yield 5
        swaps = h._swaps(board, 0, 3, None)
        assert len(swaps) == 5, "Edge swaps @ 0,3  did not yield expected swap count of 5!"
        assert len(set(swaps).intersection(set([(0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 5, "Edge swaps @ 0,3  did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 5, None)
        assert len(swaps) == 5, "Edge swaps @ 2,5  did not yield expected swap count of 5!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (1, 0), (1, -1), (0, -1)]))) == 5, "Edge swaps @ 2,5  did not yield correct set of deltas!"
        swaps = h._swaps(board, 4, 3, None)
        assert len(swaps) == 5, "Edge swaps @ 4,3  did not yield expected swap count of 5!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]))) == 5, "Edge swaps @ 4,3  did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 0, None)
        assert len(swaps) == 5, "Edge swaps @ 2,0  did not yield expected swap count of 5!"
        assert len(set(swaps).intersection(set([(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]))) == 5, "Edge swaps @ 2,0  did not yield correct set of deltas!"

        # swapping with previous move should yield 7
        swaps = h._swaps(board, 2, 2, (-1, -1))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1)]))) == 7, "Swaps @ 2,2 and previous move -1,-1 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (-1, 0))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, -1), (0, -1)]))) == 7, "Swaps @ 2,2 and previous move -1,0 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (-1, 1))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (0, -1)]))) == 7, "Swaps @ 2,2 and previous move -1,1 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (0, 1))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]))) == 7, "Swaps @ 2,2 and previous move 0,1 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (1, 1))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 7, "Swaps @ 2,2 and previous move 1,1 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (1, 0))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 7, "Swaps @ 2,2 and previous move 1,0 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (1, -1))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 7, "Swaps @ 2,2 and previous move -1,1 did not yield correct set of deltas!"
        swaps = h._swaps(board, 2, 2, (0, -1))
        assert len(swaps) == 7, "Swaps @ 2,2  did not yield expected swap count of 7!"
        assert len(set(swaps).intersection(set([(-1, -1), (-1, 0), (-1, 1), (1, 1), (1, 0), (1, -1), (0, -1)]))) == 7, "Swaps @ 2,2 and previous move 0,-1 did not yield correct set of deltas!"
