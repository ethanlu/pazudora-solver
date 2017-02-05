from pazudorasolver.heuristics.heuristic import Heuristic
from pazudorasolver.board import Board


class GreedyDfs(Heuristic):
    def __init__(self, weights):
        super(GreedyDfs, self).__init__(weights)

    def _step(self, score, moves, board, row, column, depth):
        if depth == 0:
            return (score, moves, board)
        else:
            # get possible swaps from current row, column position
            swaps = self._swaps(board, row, column)

            solutions = []
            for delta_r, delta_c in swaps:
                swapped_board = Board.copy_board(board).swap(row, column, row + delta_r, column + delta_c)
                if self._remember(swapped_board):
                    # only add move to solutions if it is a board layout that has not been seen before
                    solutions.append((self._score(swapped_board), swapped_board, (delta_r, delta_c)))

            if solutions:
                # calculate score on all possible swaps and order them from highest to lowest. recurse into the highest one
                best = max(solutions, key=lambda x: x[0])
                return self._step(score + best[0], (moves + (best[2],)), best[1], row + best[2][0], column + best[2][1], depth - 1)
            else:
                return (score, moves, board)

    def solve(self, board, depth):
        best = None
        score = self._score(board)
        for r in range(board.rows):
            for c in range(board.columns):
                solution = self._step(score, ((r, c),), board, r, c, depth)

                if best is None or best[0] < solution[0]:
                    best = solution

        return best
