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
        b = Board.create_randomized_board(rows, columns)

        m = Board.create_empty_board(rows, columns)
        for cluster in b.get_matches():
            for r, c in cluster[1]:
                m.update(r, c, type(cluster[0]))

        s = GreedyDfs(weights) if False else PrunedBfs(weights)
        s.diagonals = True
        start = time.time()
        moves = s.solve(b, depth)
        performance = time.time() - start

        print '---------------------------------------------'
        print b
        print m
        print 'run time : ' + str(performance)
        print 'best move score : ' + str(moves[0])
        print 'start : ' + str(moves[1][0])
        print 'moves : ' + str(moves[1][1:])
        print moves[2]

        m = Board.create_empty_board(rows, columns)
        for cluster in moves[2].get_matches():
            for r, c in cluster[1]:
                m.update(r, c, type(cluster[0]))
        print m


if __name__ == "__main__":
    Solver.run(5,
               6,
               50,
               {Fire.symbol: 2.0,
                Wood.symbol: 2.0,
                Water.symbol: 2.0,
                Dark.symbol: 2.0,
                Light.symbol: 2.0,
                Heart.symbol: 1.0,
                Poison.symbol: 0.5,
                Jammer.symbol: 0.5,
                Unknown.symbol: 0.0})
