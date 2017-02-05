from pazudorasolver.heuristics.heuristic import Heuristic
from pazudorasolver.board import Board


class PrunedBfs(Heuristic):
    def __init__(self, weights):
        super(PrunedBfs, self).__init__(weights)
        self._prune_limit = 25

    def _prune(self, solutions):
        return sorted(solutions, key=lambda x: x[0], reverse=True)[0:self._prune_limit]

    def _step(self, solutions, depth):
        if depth == 0:
            return solutions
        else:
            next_solutions = []
            for score, moves, board, row, column in solutions:
                for delta_r, delta_c in self._swaps(board, row, column):
                    swapped_board = Board.copy_board(board).swap(row, column, row + delta_r, column + delta_c)
                    if self._remember(swapped_board):
                        # only add move to solutions if it is a board layout that has not been seen before
                        next_solutions.append((score + self._score(swapped_board), (moves + ((delta_r, delta_c),)), swapped_board, row + delta_r, column + delta_c))

            if next_solutions:
                # prune solutions down before recursing to next depth
                return self._step(self._prune(next_solutions), depth - 1)
            else:
                return solutions

    def solve(self, board, depth):
        solutions = []
        for r in range(board.rows):
            for c in range(board.columns):
                solutions.append((self._score(board), ((r, c), ), board, r, c))

        best = self._step(solutions, depth)[0]
        return (best[0], best[1], best[2])
