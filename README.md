[![PyPI version](https://badge.fury.io/py/pazudorasolver.svg)](https://badge.fury.io/py/pazudorasolver)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pazudorasolver.svg)](https://pypi.python.org/pypi/pazudorasolver/)
[![Build Status](https://travis-ci.org/ethanlu/pazudora-solver.svg?branch=master)](https://travis-ci.org/ethanlu/pazudora-solver)
[![Requirements Status](https://requires.io/github/ethanlu/pazudora-solver/requirements.svg?branch=master)](https://requires.io/github/ethanlu/pazudora-solver/requirements/?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/78cdfdafa28f4475a3dea086c3dd006d)](https://www.codacy.com/app/ethanoks/pazudora-solver)
[![Coverage Status](https://coveralls.io/repos/github/ethanlu/pazudora-solver/badge.svg?branch=master)](https://coveralls.io/github/ethanlu/pazudora-solver?branch=master)

Pazudora Solver
=====

Python-based solver library for the [Puzzles and Dragons mobile game](http://www.gunghoonline.com/games/puzzle-dragons/).
Inspired by the [Javascript version](https://github.com/alexknutson/Combo.Tips) on [Combo.tips](http://combo.tips/). This project is primarily a library that can be used to build a board and solve it using the provided heuristics.

# Table of Contents
* [Setup](#setup)
* [Example](#example)
* [TODO](#todo)

## Setup
Install this library in your Python virtual environment
```commandline
pip install pazudorasolver
```

Import these modules into your Python project
```python
# the puzzle board
from pazudorasolver.board import Board
 
# the pieces that can be in the board
from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
 
# the various heuristics that can be used to solve the board layout
from pazudorasolver.heuristics.greedy_dfs import GreedyDfs
from pazudorasolver.heuristics.pruned_bfs import PrunedBfs
```

Construct a board
```python
# a 5x6 board with some pieces
piece_list = [Fire,  Wood,  Water, Dark,  Light, Heart,
              Fire,  Water, Dark,  Light, Heart, Fire,
              Fire,  Water, Dark,  Heart, Heart, Wood,
              Light, Water, Light, Fire,  Wood,  Wood,
              Dark,  Water, Dark,  Light, Light, Light]
number_of_rows = 5
number_of_columns = 6
board = Board(piece_list, number_of_rows, number_of_columns)
```

Heuristics need to be given a configuration that defines the weight values for all of the types of pieces on the board. Weight configuration is a dictionary of pieces. increase a piece's weight to give it higher preference for heuristic.
```python
# in this configuration, emphasis is placed on getting fire, wood, water, dark, and light
# matches due to their weights being 2.0
weight_configuration1 = {Fire.symbol: 2.0,
                         Wood.symbol: 2.0,
                         Water.symbol: 2.0,
                         Dark.symbol: 2.0,
                         Light.symbol: 2.0,
                         Heart.symbol: 1.0,
                         Poison.symbol: 0.5,
                         Jammer.symbol: 0.5,
                         Unknown.symbol: 0.0}
           
# in this configuration, emphasis is placed on matching fire and dark (ronia team) 
weight_configuration2 = {Fire.symbol: 2.0,
                         Wood.symbol: 1.0,
                         Water.symbol: 1.0,
                         Dark.symbol: 2.0,
                         Light.symbol: 1.0,
                         Heart.symbol: 1.0,
                         Poison.symbol: 0.5,
                         Jammer.symbol: 0.5,
                         Unknown.symbol: 0.0}
```

Solve a constructed board by using one of the available heuristics
```python
heuristic = GreedyDfs(weight_configuration1)
keep_top_n_solutions = 25
solution = heuristic.solve(board, keep_top_n_solutions)
```

## Example
```python
from pazudorasolver.board import Board
from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudorasolver.heuristics.greedy_dfs import GreedyDfs
from pazudorasolver.heuristics.pruned_bfs import PrunedBfs
 
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
 
print(board)
print(matches)
 
# try GreedyDfs heuristic
solver1 = GreedyDfs(weights)
solution = solver1.solve(board, 50)
 
print(solution)
 
# try PrunedBfs heuristic
solver2 = PrunedBfs(weights)
solution = solver2.solve(board, 50)
 
print(solution)
```

## TODO
- Improve score calculation (TPA, Row-clear, N-match, etc.)
- Additional heuristics for solving board
