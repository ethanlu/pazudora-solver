from pazudora_solver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudora_solver.board import Board

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
    return Board([Fire,  Wood,  Water, Dark,  Light, Poison,
                  Water, Water, Water, Light, Heart, Jammer,
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


def test_invalid_board():
    # length of list must be equal to row x column for the board to be valid
    with pytest.raises(Exception) as exec_info:
        Board([Fire, Water, Wood, Dark, Light, Heart, Poison, Jammer, Unknown], 10, 10)
    assert 'Given pieces do not fit specified board dimensions!' in str(exec_info.value), \
        "Board's pieces list was smaller than dimensions, but did not fail initialization!"

    with pytest.raises(Exception) as exec_info:
        Board([Fire, Water, Wood, Dark, Light, Heart, Poison, Jammer, Unknown], 2, 2)
    assert 'Given pieces do not fit specified board dimensions!' in str(exec_info.value), \
        "Board's pieces list was bigger than dimensions, but did not fail initialization!"

    with pytest.raises(Exception) as exec_info:
        Board([Fire, Water, Wood, Dark, Light, Heart, Poison, Jammer, Unknown], 0, 3)
    assert 'Given pieces do not fit specified board dimensions!' in str(exec_info.value), "Board's row was invalid, but did not fail initialization!"


def test_board_setup():
    # as long as length of piece list is equal to row x column, the board yields no error and loads from top left down to bottom right
    b = Board([Fire, Water, Wood, Dark, Light, Heart], 2, 3)
    assert type(b) == Board, "Board valid 2x3, but was not instantiated!"
    assert type(b.cell(0, 0)) == Fire, "Unexpected piece @ 0,0 on 2x3 Board!"
    assert type(b.cell(0, 1)) == Water, "Unexpected piece @ 0,1 on 2x3 Board!"
    assert type(b.cell(0, 2)) == Wood, "Unexpected piece @ 0,2 on 2x3 Board!"
    assert type(b.cell(1, 0)) == Dark, "Unexpected piece @ 1,0 on 2x3 Board!"
    assert type(b.cell(1, 1)) == Light, "Unexpected piece @ 1,1 on 2x3 Board!"
    assert type(b.cell(1, 2)) == Heart, "Unexpected piece @ 1,2 on 2x3 Board!"
    assert b.rows == 2, "2x3 board has incorrect rows property!"
    assert b.columns == 3, "2x3 board has incorrect columns property!"
    assert len(b.board) == 2 and len(b.board[0]) == 3, "2x3 board has incorrect board dimensions!"

    b = Board([Fire, Water, Wood, Dark, Light, Heart], 3, 2)
    assert type(b) == Board, "Board valid 3x2, but was not instantiated!"
    assert type(b.cell(0, 0)) == Fire, "Unexpected piece @ 0,0 on 3x2 Board!"
    assert type(b.cell(0, 1)) == Water, "Unexpected piece @ 0,1 on 3x2 Board!"
    assert type(b.cell(1, 0)) == Wood, "Unexpected piece @ 1,0 on 3x2 Board!"
    assert type(b.cell(1, 1)) == Dark, "Unexpected piece @ 1,1 on 3x2 Board!"
    assert type(b.cell(2, 0)) == Light, "Unexpected piece @ 2,0 on 3x2 Board!"
    assert type(b.cell(2, 1)) == Heart, "Unexpected piece @ 2,1 on 3x2 Board!"
    assert b.rows == 3, "3x2 board has incorrect rows property!"
    assert b.columns == 2, "3x2 board has incorrect columns property!"
    assert len(b.board) == 3 and len(b.board[0]) == 2, "3x2 board has incorrect board dimensions!"


def test_empty_board():
    # empty board should contain only Unknown pieces
    b = Board.create_empty_board(5, 6)
    unknown_pieces = [b.cell(r, c) for c in range(b.columns) for r in range(b.rows) if type(b.cell(r, c)) == Unknown]
    assert len(unknown_pieces) == 30, "Creating empty board does not contain only Unknown pieces!"


def test_randomized_board():
    # randomized board should contain only Fire, Water, Wood, Dark, Light, and Heart pieces
    allowed_pieces = set([Fire, Water, Wood, Dark, Light, Heart])
    b = Board.create_randomized_board(5, 6)
    pieces = [b.cell(r, c) for c in range(b.columns) for r in range(b.rows) if type(b.cell(r, c)) in allowed_pieces]
    assert len(pieces) == 30, "Creating randomized board contains invalid pieces!"


def test_copy_board():
    # copying a board produces another board with same setup as original
    original = Board.create_randomized_board(5, 6)
    copy = Board.copy_board(original)

    assert original.rows == copy.rows, "Copied board's rows do not match original!"
    assert original.columns == copy.columns, "Copied board's columns do not match original!"
    matching = [copy.cell(r, c)
                for c in range(original.columns) for r in range(original.rows)
                if isinstance(original.cell(r, c), type(copy.cell(r, c))) and original.cell(r, c).location == copy.cell(r, c).location]
    assert len(matching) == 30, "Copied board's board does not match original!"


def test_match_finding(board_with_3_chain, board_with_1_chain, board_with_0_chain):
    # getting matches should find all chains on the board and their correct sizes
    m = dict((piece.symbol, clusters) for piece, clusters in board_with_3_chain.get_matches())

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

    m = dict((piece.symbol, clusters) for piece, clusters in board_with_1_chain.get_matches())
    assert len(m.keys()) == 1, "Board with 1 chain did not yield correct match count of 1!"
    assert len(m[Water.symbol]) == 5, "Board's Water match is not expected 5!"
    assert (1, 1) in m[Water.symbol], "Piece @ 1,1 is issing from 1-chain Board's Water match list!"
    assert (2, 1) in m[Water.symbol], "Piece @ 2,1 is issing from 1-chain Board's Water match list!"
    assert (3, 1) in m[Water.symbol], "Piece @ 3,1 is issing from 1-chain Board's Water match list!"
    assert (1, 0) in m[Water.symbol], "Piece @ 1,0 is issing from 1-chain Board's Water match list!"
    assert (1, 2) in m[Water.symbol], "Piece @ 1,2 is issing from 1-chain Board's Water match list!"

    m = dict((piece.symbol, clusters) for piece, clusters in board_with_0_chain.get_matches())
    assert len(m.keys()) == 0, "Board with 0 chain did not yield correct match count of 0!"


def test_cluster_finding(board_with_0_chain):
    # clusters on a cell should return all adjacent neighbors of the same piece
    c = board_with_0_chain.get_cluster(2, 1)
    assert type(c[0]) == Fire, "Cluster @ 2,1 is not the expected Fire piece!"
    assert len(c[1]) == 3, "Cluster @ 2,1 does not have expected count of 3!"

    c = board_with_0_chain.get_cluster(1, 2)
    assert type(c[0]) == Fire, "Cluster @ 1,2 is not the expected Fire piece!"
    assert len(c[1]) == 1, "Cluster @ 1,2 does not have expected count of 1!"

    c = board_with_0_chain.get_cluster(0, 0)
    assert type(c[0]) == Unknown, "Cluster @ 0,0 is not the expected Fire piece!"
    assert len(c[1]) == 26, "Cluster @ 0,0 does not have expected count of 26!"


def test_cell_update():
    # updating a board's cell should update that cell only
    original = Board.create_randomized_board(5, 6)
    updated_board = Board.copy_board(original).update(3, 4, Jammer)
    matching = [
        updated_board.cell(r, c)
        for c in range(original.columns) for r in range(original.rows)
        if isinstance(original.cell(r, c), type(updated_board.cell(r, c))) and original.cell(r, c).location == updated_board.cell(r, c).location
    ]
    assert len(matching) == 29, "Updating board did not yield expected matching cells with original board!"
    assert type(updated_board.cell(3, 4)) == Jammer, "Piece @ 3,4 was not updated to correct piece!"


def test_cell_swap(board_with_1_chain):
    # swapping a board's cell with another should only affect the source and target cells
    original = board_with_1_chain
    swapped_board = Board.copy_board(original)
    # swap corners where the two pieces are different
    swapped_board.swap(0, 0, 4, 5)

    matching = [
        swapped_board.cell(r, c)
        for c in range(original.columns) for r in range(original.rows)
        if isinstance(original.cell(r, c), type(swapped_board.cell(r, c))) and original.cell(r, c).location == swapped_board.cell(r, c).location
    ]
    assert len(matching) == 28, "Swapping upper left corner with lower right corner of board yielded match counts!"
    assert swapped_board.cell(0, 0).location == (0, 0), "Swapped piece @ 0,0 has invalid location!"
    assert swapped_board.cell(4, 5).location == (4, 5), "Swapped piece @ 4,5 has invalid location!"
    assert isinstance(swapped_board.cell(0, 0), type(original.cell(4, 5))), "Swapped piece @ 0,0 does not match original piece @ 4,5!"
    assert isinstance(swapped_board.cell(4, 5), type(original.cell(0, 0))), "Swapped piece @ 4,5 does not match original piece @ 0,0!"

    # swap multiple times should yield expected results
    original = Board.create_randomized_board(5, 6)
    swapped_board = Board.copy_board(original)
    swapped_board.swap(0, 0, 1, 1)
    swapped_board.swap(1, 1, 2, 2)
    swapped_board.swap(2, 2, 3, 3)
    swapped_board.swap(3, 3, 4, 4)
    assert isinstance(swapped_board.cell(0, 0), type(original.cell(1, 1))), "Swapped piece @ 0,0 does not match original @ 1,1"
    assert isinstance(swapped_board.cell(1, 1), type(original.cell(2, 2))), "Swapped piece @ 1,1 does not match original @ 2,2"
    assert isinstance(swapped_board.cell(2, 2), type(original.cell(3, 3))), "Swapped piece @ 2,2 does not match original @ 3,3"
    assert isinstance(swapped_board.cell(3, 3), type(original.cell(4, 4))), "Swapped piece @ 3,3 does not match original @ 4,4"
    assert isinstance(swapped_board.cell(4, 4), type(original.cell(0, 0))), "Swapped piece @ 4,4 does not match original @ 0,0"
