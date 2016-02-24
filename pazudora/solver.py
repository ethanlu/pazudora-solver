from itertools import islice
from board import Board
from piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown

import time

class Solver(object):
    def __init__(self):
        pass

    def calculate_score(self, board, weights, row=None, column=None):
        matches = board.get_matches()
        chain_multiplier = len(matches)
        match_score = sum([weights[piece.symbol] for piece, clusters in matches])
        fragment_score = 0.0
        if row is not None and column is not None:
            # fragment score is the number of clusters around the target cell that is more than length 3 (potential chain)
            fragment_score += len(board.get_cluster(row - 1, column)[1]) // 3
            fragment_score += len(board.get_cluster(row + 1, column)[1]) // 3
            fragment_score += len(board.get_cluster(row, column - 1)[1]) // 3
            fragment_score += len(board.get_cluster(row, column + 1)[1]) // 3

        return (chain_multiplier * match_score + fragment_score)

    def solve(self, score, moves, board, row, column, weights, depth):
        if depth == 0:
            return (score, moves, board)
        else:
            # consider previous move's direction so that we don't end up going back
            previous_move = moves[-1] if len(moves) > 1 else None
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

            # calculate score on all possible swaps and order them from highest to lowest. recurse into the highest one
            best = max(
                (
                    (self.calculate_score(swapped_board, weights, *move), swapped_board, move)
                    for swapped_board, move in (
                        (Board.copy_board(board).swap(row, column, row + delta_r, column + delta_c), (delta_r, delta_c))
                        for delta_r, delta_c in swaps
                    )
                )
            )
            return self.solve(score + best[0], (moves + (best[2],)), best[1], row + best[2][0], column + best[2][1], weights, depth - 1)

    def get_solutions(self, board, weights, depth):
        solutions = []
        # get best solution for each cell on the board
        score = self.calculate_score(board, weights)
        for r in range(board.rows):
            for c in range(board.columns):
                solutions.append(self.solve(score, ((r, c),), board, r, c, weights, depth))

        # return top 10 best solutions
        return list(islice(sorted(solutions, cmp=lambda x, y: cmp(x[0], y[0]), reverse=True), 0, 9))


if __name__ == "__main__":
    rows = 5
    columns = 6
    depth = 50

    weights = {Fire.symbol: 2.0,
               Wood.symbol: 2.0,
               Water.symbol: 2.0,
               Dark.symbol: 2.0,
               Light.symbol: 2.0,
               Heart.symbol: 1.0,
               Poison.symbol: 0.5,
               Jammer.symbol: 0.5,
               Unknown.symbol: 0.0}

    b = Board.create_randomized_board(rows, columns)

    m = Board.create_empty_board(rows, columns)
    for cluster in b.get_matches():
        for r, c in cluster[1]:
            m.update(r, c, cluster[0].__class__(r, c))

    s = Solver()
    start = time.time()
    moves = s.get_solutions(b, weights, depth)
    performance = time.time() - start

    print '---------------------------------------------'
    print b
    print m
    print 'run time : ' + str(performance)
    print 'best move score : ' + str(moves[0][0])
    print 'start : ' + str(moves[0][1][0])
    print 'moves : ' + str(moves[0][1][1:])
    print moves[0][2]

    m = Board.create_empty_board(rows, columns)
    for cluster in moves[0][2].get_matches():
        for r, c in cluster[1]:
            m.update(r, c, cluster[0].__class__(r, c))
    print m