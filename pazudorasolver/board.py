from itertools import chain
from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Unknown

import random


class Board(object):
    def __init__(self, pieces, rows, columns):
        """
        initializes board with list of pieces starting from upper left and going horizontally and then vertically down
        to the lower right. throws exception if length of pieces do not match row and column dimensions
        :param pieces: list of pieces from upper left down to lower right
        :param rows: the number of rows
        :param columns: the number of columns
        :return: initialized board
        """
        if len(pieces) != (rows * columns):
            raise Exception('Given pieces do not fit specified board dimensions!')

        self._rows = rows
        self._columns = columns

        self._board = [[pieces[((r % rows) * columns) + (c % columns)](r, c) for c in range(columns)] for r in range(rows)]

    def __repr__(self):
        output = '  | ' + ' '.join([str(c) for c in range(self._columns)]) + '\n'
        output += '---' + ('--' * self._columns) + '\n'

        for r in range(self._rows):
            output += str(r) + ' | ' + ' '.join([str(self._board[r][c]) for c in range(self._columns)]) + '\n'

        return output

    def hash(self):
        return "".join([self._board[r][c].symbol for r in range(self._rows) for c in range(self._columns)])

    @classmethod
    def create_randomized_board(cls, rows, columns):
        pieces = [Fire, Wood, Water, Dark, Light, Heart]
        return cls([random.choice(pieces) for i in range(rows * columns)], rows, columns)

    @classmethod
    def create_empty_board(cls, rows, columns):
        return cls([Unknown for i in range(rows * columns)], rows, columns)

    @classmethod
    def copy_board(cls, board):
        return cls([type(p) for p in chain(*board.board)], board.rows, board.columns)

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    @property
    def board(self):
        return self._board

    def cell(self, row, column):
        return self._board[row][column]

    def swap(self, source_row, source_column, target_row, target_column):
        tmp = type(self._board[source_row][source_column])(target_row, target_column)
        self._board[source_row][source_column] = type(self._board[target_row][target_column])(source_row, source_column)
        self._board[target_row][target_column] = tmp
        return self

    def update(self, row, column, piece):
        self._board[row][column] = piece(row, column)
        return self

    def get_cluster(self, row, column):
        cluster = set([])
        search_stack = [(row, column)]
        while search_stack:
            r, c = search_stack.pop()
            if 0 <= r < self._rows and 0 <= c < self._columns and (r, c) not in cluster and \
               self._board[r][c] and self._board[r][c].symbol == self._board[row][column].symbol:
                # candidate cell is a valid cell and it matches the starting cell, add it to cluster
                cluster.update(((r, c), ))

                # add up, down, left, and right cells
                search_stack.append((r - 1, c))
                search_stack.append((r + 1, c))
                search_stack.append((r, c - 1))
                search_stack.append((r, c + 1))

        return (self._board[row][column], cluster)

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
                    if first and second and third and (first.symbol == second.symbol == third.symbol) and first.matchable:
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
        vertical_chains = find_chains(self._columns, self._rows, list(zip(*self._board)))  # swap row with column and transpose board to get verticals

        clusters = []
        if horizontal_chains or vertical_chains:
            # there is at least one chain, overlay them onto an empty board
            chain_locations = set(chain(*(horizontal_chains + vertical_chains)))
            memoized = set([])
            for r, c in chain_locations:
                if (r, c) not in memoized:
                    # cell is part of a chain, but has not been clustered yet, so start cluster search
                    cluster_piece, cluster = self.get_cluster(r, c)
                    # need to do intersection because cluster search will return all adjacent cells of same symbol...including non-chain cells
                    clusters.append((cluster_piece, cluster.intersection(chain_locations)))
                    memoized = memoized.union(cluster)

        return clusters
