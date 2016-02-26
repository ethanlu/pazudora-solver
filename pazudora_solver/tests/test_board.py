from pazudora_solver.piece import *
from pazudora_solver.board import *

import pytest


@pytest.fixture(scope='module')
def board_with_3_chain():
    return Board([Fire,  Wood,  Water, Dark,  Light, Heart,
                  Fire,  Water, Dark,  Light, Heart, Fire,
                  Fire,  Water, Dark,  Heart, Heart, Wood,
                  Light, Water, Light, Fire,  Wood,  Wood,
                  Dark,  Water, Dark,  Light, Light, Light], 5, 6)

@pytest.fixture(scope='module')
def board_with_1_chain():
    return Board([Fire,  Wood,  Water, Dark,  Light, Heart,
                  Water, Water, Water, Light, Heart, Fire,
                  Fire,  Water, Dark,  Heart, Heart, Wood,
                  Light, Water, Light, Fire,  Wood,  Wood,
                  Dark,  Heart, Dark,  Light, Heart, Light], 5, 6)

@pytest.fixture(scope='module')
def board_with_0_chain():
    return Board([Unknown, Unknown, Unknown, Unknown, Unknown, Unknown,
                  Unknown, Unknown, Fire,    Unknown, Unknown, Unknown,
                  Unknown, Fire,    Unknown, Unknown, Unknown, Unknown,
                  Unknown, Fire,    Fire,    Unknown, Unknown, Unknown,
                  Unknown, Unknown, Unknown, Unknown, Unknown, Unknown], 5, 6)

@pytest.fixture(scope='module')
def weights():
    return {Fire.symbol: 1.0,
            Wood.symbol: 1.0,
            Water.symbol: 1.0,
            Dark.symbol: 1.0,
            Light.symbol: 1.0,
            Heart.symbol: 1.0,
            Poison.symbol: 1.0,
            Jammer.symbol: 1.0,
            Unknown.symbol: 1.0}


class TestBoard(object):
    def test_invalid_board(self):
        # length of list must be equal to row x column for the board to be valid
        with pytest.raises(Exception) as exec_info:
            b = Board([Fire, Water, Wood, Dark, Light, Heart, Poison, Jammer, Unknown], 10, 10)
        assert 'Given pieces do not fit specified board dimensions!' in str(exec_info.value), "Board's pieces list was smaller than dimensions, but did not fail initialization!"

        with pytest.raises(Exception) as exec_info:
            b = Board([Fire, Water, Wood, Dark, Light, Heart, Poison, Jammer, Unknown], 2, 2)
        assert 'Given pieces do not fit specified board dimensions!' in str(exec_info.value), "Board's pieces list was bigger than dimensions, but did not fail initialization!"

        with pytest.raises(Exception) as exec_info:
            b = Board([Fire, Water, Wood, Dark, Light, Heart, Poison, Jammer, Unknown], 0, 3)
        assert 'Given pieces do not fit specified board dimensions!' in str(exec_info.value), "Board's row was invalid, but did not fail initialization!"

    def test_board_setup(self):
        # as long as length of piece list is equal to row x column, the board yields no error and loads from top left down to bottom right
        b = Board([Fire, Water, Wood, Dark, Light, Heart], 2, 3)
        assert b.__class__ == Board, "Board valid 2x3, but was not instantiated!"
        assert b.cell(0, 0).__class__ == Fire, "Unexpected piece @ 0,0 on 2x3 Board!"
        assert b.cell(0, 1).__class__ == Water, "Unexpected piece @ 0,1 on 2x3 Board!"
        assert b.cell(0, 2).__class__ == Wood, "Unexpected piece @ 0,2 on 2x3 Board!"
        assert b.cell(1, 0).__class__ == Dark, "Unexpected piece @ 1,0 on 2x3 Board!"
        assert b.cell(1, 1).__class__ == Light, "Unexpected piece @ 1,1 on 2x3 Board!"
        assert b.cell(1, 2).__class__ == Heart, "Unexpected piece @ 1,2 on 2x3 Board!"
        assert b.rows == 2, "2x3 board has incorrect rows property!"
        assert b.columns == 3, "2x3 board has incorrect columns property!"
        assert len(b.board) == 2 and len(b.board[0]) == 3, "2x3 board has incorrect board dimensions!"

        b = Board([Fire, Water, Wood, Dark, Light, Heart], 3, 2)
        assert b.__class__ == Board, "Board valid 3x2, but was not instantiated!"
        assert b.cell(0, 0).__class__ == Fire, "Unexpected piece @ 0,0 on 3x2 Board!"
        assert b.cell(0, 1).__class__ == Water, "Unexpected piece @ 0,1 on 3x2 Board!"
        assert b.cell(1, 0).__class__ == Wood, "Unexpected piece @ 1,0 on 3x2 Board!"
        assert b.cell(1, 1).__class__ == Dark, "Unexpected piece @ 1,1 on 3x2 Board!"
        assert b.cell(2, 0).__class__ == Light, "Unexpected piece @ 2,0 on 3x2 Board!"
        assert b.cell(2, 1).__class__ == Heart, "Unexpected piece @ 2,1 on 3x2 Board!"
        assert b.rows == 3, "3x2 board has incorrect rows property!"
        assert b.columns == 2, "3x2 board has incorrect columns property!"
        assert len(b.board) == 3 and len(b.board[0]) == 2, "3x2 board has incorrect board dimensions!"

    def test_empty_board(self):
        # empty board should contain only Unknown pieces
        b = Board.create_empty_board(5, 6)
        unknown_pieces = [b.cell(r, c) for c in range(b.columns) for r in range(b.rows) if b.cell(r, c).__class__ == Unknown]
        assert len(unknown_pieces) == 30, "Creating empty board does not contain only Unknown pieces!"

    def test_randomized_board(self):
        # randomized board should contain only Fire, Water, Wood, Dark, Light, and Heart pieces
        allowed_pieces = set([Fire, Water, Wood, Dark, Light, Heart])
        b = Board.create_randomized_board(5, 6)
        pieces = [b.cell(r, c) for c in range(b.columns) for r in range(b.rows) if b.cell(r, c).__class__ in allowed_pieces]
        assert len(pieces) == 30, "Creating randomized board contains invalid pieces!"

    def test_copy_board(self):
        # copying a board produces another board with same setup as original
        original = Board.create_randomized_board(5, 6)
        copy = Board.copy_board(original)

        assert original.rows == copy.rows, "Copied board's rows do not match original!"
        assert original.columns == copy.columns, "Copied board's columns do not match original!"
        matching = [copy.cell(r, c)
                    for c in range(original.columns) for r in range(original.rows)
                    if original.cell(r, c).__class__ == copy.cell(r, c).__class__ and original.cell(r, c).location == copy.cell(r, c).location]
        assert len(matching) == 30, "Copied board's board does not match original!"

    def test_match_finding(self, board_with_3_chain, board_with_1_chain, board_with_0_chain):
        m = {m[0].symbol: m[1] for m in board_with_3_chain.get_matches()}

        assert len(m.keys()) == 3, "Board with 3 chains did not yield correct match count of 3!"
        assert len(m[Fire.symbol]) == 3, "Board's Fire match is not expected 3!"
        assert (0, 0) in m[Fire.symbol], "Piece @ 0,0 is issing from 3-chain Board's Fire match list!"
        assert (1, 0) in m[Fire.symbol], "Piece @ 1,0 is issing from 3-chain Board's Fire match list!"
        assert (2, 0) in m[Fire.symbol], "Piece @ 2,0 is issing from 3-chain Board's Fire match list!"
        assert len(m[Light.symbol]) == 3, "Board's Light match is not expected 3!"
        assert (4, 3) in m[Light.symbol], "Piece @ 4,3 is issing from 3-chain Board's Light match list!"
        assert (4, 4) in m[Light.symbol], "Piece @ 4,4 is issing from 3-chain Board's Light match list!"
        assert (4, 5) in m[Light.symbol], "Piece @ 4,5 is issing from 3-chain Board's Light match list!"
        assert len(m[Water.symbol]) == 4, "Board's Water match is not expected 4!"
        assert (1, 1) in m[Water.symbol], "Piece @ 1,1 is issing from 3-chain Board's Water match list!"
        assert (2, 1) in m[Water.symbol], "Piece @ 2,1 is issing from 3-chain Board's Water match list!"
        assert (3, 1) in m[Water.symbol], "Piece @ 3,1 is issing from 3-chain Board's Water match list!"
        assert (4, 1) in m[Water.symbol], "Piece @ 4,1 is issing from 3-chain Board's Water match list!"

        m = {m[0].symbol: m[1] for m in board_with_1_chain.get_matches()}
        assert len(m.keys()) == 1, "Board with 1 chain did not yield correct match count of 1!"
        assert len(m[Water.symbol]) == 5, "Board's Water match is not expected 5!"
        assert (1, 1) in m[Water.symbol], "Piece @ 1,1 is issing from 1-chain Board's Water match list!"
        assert (2, 1) in m[Water.symbol], "Piece @ 2,1 is issing from 1-chain Board's Water match list!"
        assert (3, 1) in m[Water.symbol], "Piece @ 3,1 is issing from 1-chain Board's Water match list!"
        assert (1, 0) in m[Water.symbol], "Piece @ 1,0 is issing from 1-chain Board's Water match list!"
        assert (1, 2) in m[Water.symbol], "Piece @ 1,2 is issing from 1-chain Board's Water match list!"

        m = {m[0].symbol: m[1] for m in board_with_0_chain.get_matches()}
        assert len(m.keys()) == 0, "Board with 0 chain did not yield correct match count of 0!"

    def test_cluster_finding(self, board_with_0_chain):
        c = board_with_0_chain.get_cluster(2, 1)
        assert c[0].__class__ == Fire, "Cluster @ 2,1 is not the expected Fire piece!"
        assert len(c[1]) == 3, "Cluster @ 2,1 does not have expected count of 3!"

        c = board_with_0_chain.get_cluster(1, 2)
        assert c[0].__class__ == Fire, "Cluster @ 1,2 is not the expected Fire piece!"
        assert len(c[1]) == 1, "Cluster @ 1,2 does not have expected count of 1!"

        c = board_with_0_chain.get_cluster(0, 0)
        assert c[0].__class__ == Unknown, "Cluster @ 0,0 is not the expected Fire piece!"
        assert len(c[1]) == 26, "Cluster @ 0,0 does not have expected count of 26!"
