from termcolor import colored

import random

FIRE = 'R'
WOOD = 'G'
WATER = 'B'
DARK = 'P'
LIGHT = 'Y'
RECOVER = 'H'
POISON = 'Q'
JAMMER = 'X'
UNKNOWN = '?'

class Cell(object):
    def __init__(self, row, column, piece):
        self._row = row
        self._column = column
        self._piece = piece

    def __repr__(self):
        return self._piece

    @property
    def location(self):
        return (self._row, self._column)

    @property
    def piece(self):
        return self._piece

class Board(object):
    def __init__(self, cells):
        # assumes layout is ROWxCOLUMN list
        self._rows = len(cells)
        self._columns = len(cells[0])

        self._board = cells

    def __repr__(self):
        def colorize(piece):
            if piece == FIRE:
                return colored(piece, 'red')
            elif piece == WOOD:
                return colored(piece, 'green')
            elif piece == WATER:
                return colored(piece, 'blue')
            elif piece == DARK:
                return colored(piece, 'magenta')
            elif piece == LIGHT:
                return colored(piece, 'yellow')
            elif piece == RECOVER:
                return colored(piece, 'cyan')
            else:
                return colored(piece, 'grey')

        output =  '  | ' + ' '.join([str(c) for c in range(self._columns)]) + '\n'
        output += '---' + ('--' * self._columns) + '\n'

        for r in range(self._rows):
            output += str(r) + ' | ' + ' '.join([colorize(self._board[r][c].piece) for c in range(self._columns)]) + '\n'

        return output

    @classmethod
    def create_randomized_board(cls, rows, columns):
        tiles = [FIRE, WOOD, WATER, DARK, LIGHT, RECOVER]
        return cls([[Cell(r, c, random.choice(tiles)) for c in range(columns)] for r in range(rows)])

    @classmethod
    def create_empty_board(cls, rows, columns):
        return cls([[Cell(r, c, UNKNOWN) for c in range(columns)] for r in range(rows)])

    @classmethod
    def copy_board(cls, board):
        return cls(board._board)

    def get_matches(self):
        """
        based off :
        https://github.com/alexknutson/Combo.Tips/blob/post-merge-master/ext/optimizer.js
        :return:
        """
        def find_horizontal_chains():
            chains = []
            for r in range(self._rows):
                first, second, third = (None, None, None)
                current_chain = set([])
                for c in range(self._columns):
                    third = second
                    second = first
                    first = self._board[r][c]
                    if first and second and third and (first.piece == second.piece == third.piece):
                        # keep adding the last three matching pieces to current chain
                        current_chain.update([first.location, second.location, third.location])
                    else:
                        # last three pieces do not match
                        if current_chain:
                            # add completed chain to list of chains before resetting
                            chains.append(current_chain)
                        current_chain = set([])

                if current_chain:
                    chains.append(current_chain)

            return chains

        def find_vertical_chains():
            chains = []
            for c in range(self._columns):
                first, second, third = (None, None, None)
                current_chain = set([])
                for r in range(self._rows):
                    third = second
                    second = first
                    first = self._board[r][c]
                    if first and second and third and first.piece == second.piece == third.piece:
                        # keep adding the last three matching pieces to current chain
                        current_chain.update([first.location, second.location, third.location])
                    else:
                        # last three pieces do not match
                        if current_chain:
                            # add completed chain to list of chains before resetting
                            chains.append(current_chain)
                        current_chain = set([])

                if current_chain:
                    chains.append(current_chain)

            return chains

        # get horizontal and vertical chains
        horizontal_chains = find_horizontal_chains()
        vertical_chains = find_vertical_chains()

        return horizontal_chains, vertical_chains


if __name__ == "__main__":
    b = Board.create_randomized_board(5, 6)
    h,v = b.get_matches()

    print b
    print h
    print v

