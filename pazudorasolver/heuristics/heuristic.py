from abc import ABCMeta, abstractmethod

import random


class Heuristic(metaclass=ABCMeta):
    def __init__(self, weights):
        self._weights = weights
        self._diagonals = False
        self._history = {}

    @property
    def diagonals(self):
        return self._diagonals

    @diagonals.setter
    def diagonals(self, diagonals):
        self._diagonals = diagonals

    def _reset(self):
        self._history = {}

    def _remember(self, board):
        s = board.hash()
        if s not in self._history:
            self._history[s] = True
            return self._history[s]
        else:
            return False

    def _score(self, board):
        """
        calculates a score for the current state of the board with given weights. optional row, column will calculate additional score based on localality
        :param board: current board
        :param weights: weights of pieces
        :param row: optional row
        :param column: optional column
        :return: score
        """
        matches = board.get_matches()
        chain_multiplier = len(matches)
        match_score = sum([self._weights[piece.symbol] * len(clusters) for piece, clusters in matches])
        chaos_score = random.random()

        return (chain_multiplier * match_score + chaos_score)

    def _swaps(self, board, row, column):
        """
        list of possible swaps
        :param board: current board
        :param row: current row position
        :param column: current column position
        :param previous_move: previous move (as a delta tuple)
        :return: list of possible swaps as delta tuples relative to current row, column
        """
        # consider previous move's direction so that we don't end up going back
        # get swaps in all directions (up, down, left, right)
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        if self._diagonals:
            directions += [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        return [
            (delta_r, delta_c)
            for delta_r, delta_c in directions
            if 0 <= row + delta_r < board.rows and 0 <= column + delta_c < board.columns
        ]

    @abstractmethod
    def solve(self, board, depth):
        pass
