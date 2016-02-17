Pazudora Solver
=====

Python-based solver for the [Puzzles and Dragons mobile game](http://www.gunghoonline.com/games/puzzle-dragons/).
Inspired by the [Javascript version](https://github.com/alexknutson/Combo.Tips) on [Combo.tips](http://combo.tips/)

### Example
```
from pazudora import *

board = Board.create_randomized_board(5, 6)
matches = board.get_matche()

print board
print matches
```

### TODO
- Finish get_matches()
- Initial solver implementation (greedy algorithm)