from itertools import chain
from pazudora.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown

import random

class Board(object):
    def __init__(self, cells):
        # assumes layout is ROWxCOLUMN list
        self._rows = len(cells)
        self._columns = len(cells[0])

        self._board = cells

    def __repr__(self):
        output =  '  | ' + ' '.join([str(c) for c in range(self._columns)]) + '\n'
        output += '---' + ('--' * self._columns) + '\n'

        for r in range(self._rows):
            output += str(r) + ' | ' + ' '.join([str(self._board[r][c]) for c in range(self._columns)]) + '\n'

        return output

    @classmethod
    def create_randomized_board(cls, rows, columns):
        pieces = [Fire, Wood, Water, Dark, Light, Heart]
        return cls([[random.choice(pieces)(r, c) for c in range(columns)] for r in range(rows)])

    @classmethod
    def create_empty_board(cls, rows, columns):
        return cls([[Unknown(r, c) for c in range(columns)] for r in range(rows)])

    @classmethod
    def copy_board(cls, board):
        return cls([[board.cell(r, c).__class__(r, c) for c in range(board.columns)] for r in range(board.rows)])

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    def cell(self, row, column):
        return self._board[row][column]

    def swap(self, source_row, source_column, target_row, target_column):
        tmp = self._board[source_row][source_column].__class__(target_row, target_column)
        self._board[source_row][source_column] = self._board[target_row][target_column].__class__(source_row, source_column)
        self._board[target_row][target_column] = tmp
        return self

    def update(self, row, column, piece):
        self._board[row][column] = piece
        return self

    def get_cluster(self, row, column):
        cluster = set([])
        search_stack = [(row, column)]
        while search_stack:
            r, c = search_stack.pop()
            if 0 <= r < self._rows and 0 <= c < self._columns and (r, c) not in cluster and self._board[r][c] and self._board[r][c].symbol == self._board[row][column].symbol:
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
        vertical_chains = find_chains(self._columns, self._rows, zip(*self._board))  # swap row with column and transpose board to get verticals

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
                    memoized.union(cluster)

        return clusters
