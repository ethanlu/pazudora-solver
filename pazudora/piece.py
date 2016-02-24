from abc import ABCMeta, abstractmethod, abstractproperty
from termcolor import colored

class Piece(object):
    __metaclass__ = ABCMeta

    def __init__(self, r, c):
        self._row = r
        self._column = c

    @abstractmethod
    def is_matchable(self):
        pass

    @property
    def location(self):
        return (self._row, self._column)

class Fire(Piece):
    symbol = 'R'

    def __init__(self, r, c):
        super(Fire, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'red')

    def is_matchable(self):
        return True

class Wood(Piece):
    symbol = 'G'

    def __init__(self, r, c):
        super(Wood, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'green')

    def is_matchable(self):
        return True

class Water(Piece):
    symbol = 'B'

    def __init__(self, r, c):
        super(Water, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'blue')

    def is_matchable(self):
        return True

class Dark(Piece):
    symbol = 'P'

    def __init__(self, r, c):
        super(Dark, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'magenta')

    def is_matchable(self):
        return True

class Light(Piece):
    symbol = 'Y'

    def __init__(self, r, c):
        super(Light, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'yellow')

    def is_matchable(self):
        return True

class Heart(Piece):
    symbol = 'H'

    def __init__(self, r, c):
        super(Heart, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'cyan')

    def is_matchable(self):
        return True

class Poison(Piece):
    symbol = '@'

    def __init__(self, r, c):
        super(Poison, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'white')

    def is_matchable(self):
        return True

class Jammer(Piece):
    symbol = '#'

    def __init__(self, r, c):
        super(Jammer, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'white')

    def is_matchable(self):
        return True

class Unknown(Piece):
    symbol = '?'

    def __init__(self, r, c):
        super(Unknown, self).__init__(r, c)

    def __repr__(self):
        return colored(self.symbol, 'grey')

    def is_matchable(self):
        return False
