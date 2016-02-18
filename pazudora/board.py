from itertools import chain
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

    def update(self, cells):
        for cell in cells:
            (r, c) = cell.location
            self._board[r][c] = cell

    def get_matches(self):
        def find_chains(row, column, board):
            chains = []
            for r in range(row):
                first, second, third = (None, None, None)
                current_chain = set([])
                for c in range(column):
                    third = second
                    second = first
                    first = board[r][c]
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
                    # add final chain if there is one
                    chains.append(current_chain)

            return chains

        # get horizontal and vertical chains
        horizontal_chains = find_chains(self._rows, self._columns, self._board)
        vertical_chains = find_chains(self._columns, self._rows, zip(*self._board))  # swap row with column and transpose board to get verticals

        clusters = []
        if horizontal_chains or vertical_chains:
            # there is at least one chain, overlay them onto an empty board
            chains_board = [[None for c in range(self._columns)] for r in range(self._rows)]
            for (r, c) in chain(*(horizontal_chains + vertical_chains)):
                chains_board[r][c] = self._board[r][c]

            # find the clusters by doing a floodfill on any cell that is not unknown
            for r in range(self._rows):
                for c in range(self._rows):
                    if chains_board[r][c] is not None:
                        # cell is not unknown, so it is the start of a cluster
                        cluster = []
                        cluster_piece = chains_board[r][c].piece
                        search_stack = [(r, c)]
                        while search_stack:
                            r1, c1 = search_stack.pop()
                            if 0 <= r1 < self._rows and 0 <= c1 < self._columns and chains_board[r1][c1] and cluster_piece == chains_board[r1][c1].piece:
                                # candidate cell is a valid cell and it matches the cell that started the cluster search
                                # add it to cluster and remove it from the chains board (memoize)
                                cluster.append((r1, c1))
                                chains_board[r1][c1] = None

                                # add up, down, left, and right cells
                                search_stack.append((r1 - 1, c1))
                                search_stack.append((r1 + 1, c1))
                                search_stack.append((r1, c1 - 1))
                                search_stack.append((r1, c1 + 1))

                        clusters.append((cluster_piece, tuple(cluster)))

        return clusters


if __name__ == "__main__":
    rows = 9
    columns = 10

    b = Board.create_randomized_board(rows, columns)
    print b

    m = Board.create_empty_board(rows, columns)
    m.update((Cell(r, c, cluster[0]) for cluster in b.get_matches() for r, c in cluster[1]))
    print m


