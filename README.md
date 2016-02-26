Pazudora Solver
=====

Python-based solver for the [Puzzles and Dragons mobile game](http://www.gunghoonline.com/games/puzzle-dragons/).
Inspired by the [Javascript version](https://github.com/alexknutson/Combo.Tips) on [Combo.tips](http://combo.tips/)

### Example
```python
from pazudora.board import Board
from pazudora.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudora.heuristics.greedy_dfs import GreedyDfs
from pazudora.heuristics.pruned_bfs import PrunedBfs

weights = {Fire.symbol: 2.0,
           Wood.symbol: 2.0,
           Water.symbol: 2.0,
           Dark.symbol: 2.0,
           Light.symbol: 2.0,
           Heart.symbol: 1.0,
           Poison.symbol: 0.5,
           Jammer.symbol: 0.5,
           Unknown.symbol: 0.0}

board = Board.create_randomized_board(5, 6)
matches = board.get_matches()

print board
print matches

solver1 = GreedyDfs(weights)
solution = solver1.solve(board, 50)

print solution

solver2 = PrunedBfs(weights)
solution = solver2.solve(board, 50)

print solution
```

### TODO
- Improve fragment score calculation
- Add new heuristics ()