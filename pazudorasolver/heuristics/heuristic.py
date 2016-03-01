from abc import ABCMeta, abstractmethod


class Heuristic(object):
    __metaclass__ = ABCMeta

    def __init__(self, weights):
        self._weights = weights
        self._diagonals = False

    @property
    def diagonals(self):
        return self._diagonals

    @diagonals.setter
    def diagonals(self, diagonals):
        self._diagonals = diagonals

    def _score(self, board, row=None, column=None):
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
        match_score = sum([self._weights[piece.symbol] for piece, clusters in matches])
        fragment_score = 0.0
        if row is not None and column is not None:
            # fragment score is the number of clusters around the target cell that is more than length 3 (potential chain)
            fragment_score += len(board.get_cluster(row - 1, column)[1]) // 3 \
                              + len(board.get_cluster(row + 1, column)[1]) // 3 \
                              + len(board.get_cluster(row, column - 1)[1]) // 3 \
                              + len(board.get_cluster(row, column + 1)[1]) // 3

        return (chain_multiplier * match_score + fragment_score)

    def _swaps(self, board, row, column, previous_move):
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
            if 0 <= row + delta_r < board.rows and 0 <= column + delta_c < board.columns and (-delta_r, -delta_c) != previous_move
        ]

    @abstractmethod
    def solve(self, board, depth):
        pass
