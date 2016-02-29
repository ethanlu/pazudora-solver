from pazudorasolver.piece import PieceFactory, Piece, Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown

import pytest


@pytest.fixture(scope='module')
def pieces():
    return [Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown]


def test_abstract_piece_exception():
    # should not be able to instantiate base piece class
    with pytest.raises(TypeError) as exec_info:
        Piece(0, 0)
    assert 'abstract class Piece' in str(exec_info.value), "Piece class not abstract!"


def test_piece_uniqueness(pieces):
    # pieces should have unique symbol so that match finding can work properly
    symbols = [p.symbol for p in pieces]
    unique_symbols = set(symbols)
    assert len(symbols) == len(unique_symbols), "Pieces' symbols are not unique!"


def test_piece_properties():
    # instantiated pieces should have their initiated coordinate locations returned correctly
    fire = Fire(6, 8)
    assert fire.location == (6, 8), "Instantiated piece's location incorrect!"

    # the unknown piece should be unmatchable
    unknown = Unknown(1, 1)
    assert unknown.matchable is False, "Unknown piece must not be matchable!"


def test_piece_factory(pieces):
    # piece factory should raise exception on invalid symbols
    with pytest.raises(Exception) as exec_info:
        PieceFactory.read_symbol('%')
    assert 'Unrecognized symbol' in str(exec_info.value), "PieceFactory recognized invalid symbol!"

    # piece factory should raise exception on invalid elements
    with pytest.raises(Exception) as exec_info:
        PieceFactory.read_element('Hydrogen')
    assert 'Unrecognized element' in str(exec_info.value), "PieceFactory recognized invalid element!"

    # piece factory should be able to instantiate all known pieces by symbol
    for p in pieces:
        assert isinstance(PieceFactory.read_symbol(p.symbol)(0, 0), p), "PieceFactory did not return correct piece for symbol : {s}!".format(s=p.symbol)

    # piece factory should be able to instantiate piece even if symbol is lower cased
    assert isinstance(PieceFactory.read_symbol('p')(0, 0), Dark), "PieceFactory was not able to recognize lower-case symbols!"

    # piece factory should be able to instantiate all known pieces by element
    for p in pieces:
        assert isinstance(PieceFactory.read_element(p.__name__)(0, 0), p), "PieceFactory did not return correct piece for element : {s}!".format(s=p.__name__)
