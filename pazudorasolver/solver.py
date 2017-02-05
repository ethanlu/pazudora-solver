from pazudorasolver.board import Board
from pazudorasolver.heuristics.greedy_dfs import GreedyDfs
from pazudorasolver.heuristics.pruned_bfs import PrunedBfs
from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown

import time


class Solver(object):
    def __init__(self):
        pass

    @staticmethod
    def run(rows, columns, depth, weights):
        def update_board_with_matches(board, matches):
            for piece, clusters in matches:
                for r, c in clusters:
                    board.update(r, c, type(piece))

        b = Board.create_randomized_board(5, 6)
        # b = Board([Fire,  Wood,  Water, Dark,  Light, Light,
        #           Water, Fire, Water, Light, Heart, Light,
        #           Fire,  Water, Dark,  Heart, Heart, Wood,
        #           Light, Water, Light, Fire,  Wood,  Wood,
        #           Dark,  Heart, Dark,  Light, Heart, Light], 5, 6)

        m = Board.create_empty_board(rows, columns)
        update_board_with_matches(m, b.get_matches())

        h = GreedyDfs(weights) if False else PrunedBfs(weights)
        h.diagonals = True
        start = time.time()
        moves = h.solve(b, depth)
        performance = time.time() - start

        print('---------------------------------------------')
        print(b)
        print(m)
        print('run time : ' + str(performance))
        print('best move score : ' + str(moves[0]))
        print('start : ' + str(moves[1][0]))
        print('moves : ' + str(moves[1][1:]))
        print(moves[2])

        m = Board.create_empty_board(rows, columns)
        update_board_with_matches(m, moves[2].get_matches())

        print(m)


if __name__ == "__main__":
    Solver.run(5,
               6,
               100,
               {Fire.symbol: 2.0,
                Wood.symbol: 2.0,
                Water.symbol: 2.0,
                Dark.symbol: 2.0,
                Light.symbol: 2.0,
                Heart.symbol: 1.0,
                Poison.symbol: 0.5,
                Jammer.symbol: 0.5,
                Unknown.symbol: 0.0})
