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
            fragment_score += len(board.get_cluster(row - 1, column)[1]) // 3
            fragment_score += len(board.get_cluster(row + 1, column)[1]) // 3
            fragment_score += len(board.get_cluster(row, column - 1)[1]) // 3
            fragment_score += len(board.get_cluster(row, column + 1)[1]) // 3

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
        swaps = []
        if row > 0 and (previous_move is None or previous_move != (1, 0)):
            swaps.append((-1, 0))
        if row < board.rows - 1 and (previous_move is None or previous_move != (-1, 0)):
            swaps.append((1, 0))
        if column > 0 and (previous_move is None or previous_move != (0, 1)):
            swaps.append((0, -1))
        if column < board.columns - 1 and (previous_move is None or previous_move != (0, -1)):
            swaps.append((0, 1))

        # get swaps for diagonals if they are enabled
        if self._diagonals:
            if row > 0 and column > 0 and (previous_move is None or previous_move != (1, 1)):
                swaps.append((-1, -1))
            if row > 0 and column < board.columns - 1 and (previous_move is None or previous_move != (1, -1)):
                swaps.append((-1, 1))
            if row < board.rows - 1 and column > 0 and (previous_move is None or previous_move != (-1, 1)):
                swaps.append((1, -1))
            if row < board.rows - 1 and column < board.columns - 1 and (previous_move is None or previous_move != (-1, -1)):
                swaps.append((1, 1))

        return swaps

    @abstractmethod
    def solve(self, board, depth):
        pass
