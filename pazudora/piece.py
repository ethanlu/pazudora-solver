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

    @abstractproperty
    def piece(self):
        pass

class Fire(Piece):
    def __init__(self, r, c):
        super(Fire, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'red')

    @property
    def piece(self):
        return 'R'

    def is_matchable(self):
        return True

class Wood(Piece):
    def __init__(self, r, c):
        super(Wood, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'green')

    @property
    def piece(self):
        return 'G'

    def is_matchable(self):
        return True

class Water(Piece):
    def __init__(self, r, c):
        super(Water, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'blue')

    @property
    def piece(self):
        return 'B'

    def is_matchable(self):
        return True

class Dark(Piece):
    def __init__(self, r, c):
        super(Dark, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'magenta')

    @property
    def piece(self):
        return 'P'

    def is_matchable(self):
        return True

class Light(Piece):
    def __init__(self, r, c):
        super(Light, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'yellow')

    @property
    def piece(self):
        return 'Y'

    def is_matchable(self):
        return True

class Heart(Piece):
    def __init__(self, r, c):
        super(Heart, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'white')

    @property
    def piece(self):
        return 'M'

    def is_matchable(self):
        return True

class Poison(Piece):
    def __init__(self, r, c):
        super(Poison, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'cyan')

    @property
    def piece(self):
        return 'X'

    def is_matchable(self):
        return True

class Jammer(Piece):
    def __init__(self, r, c):
        super(Jammer, self).__init__(r, c)

    def __repr__(self):
        return colored(self.piece, 'grey')

    @property
    def piece(self):
        return 'J'

    def is_matchable(self):
        return True

class Unknown(Piece):
    def __init__(self, r, c):
        super(Unknown, self).__init__(r, c)

    def __repr__(self):
        return self.piece

    @property
    def piece(self):
        return '?'

    def is_matchable(self):
        return False
