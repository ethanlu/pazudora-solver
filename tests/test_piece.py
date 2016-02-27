from pazudora_solver.piece import Piece, Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown

import pytest


class TestPiece(object):
    def test_abstract_piece_exception(self):
        # should not be able to instantiate base piece class
        with pytest.raises(TypeError) as exec_info:
            Piece(0, 0)
        assert 'abstract class Piece' in str(exec_info.value), "Piece class not abstract!"

    def test_piece_uniqueness(self):
        # pieces should have unique symbol so that match finding can work properly
        symbols = [Fire.symbol, Wood.symbol, Water.symbol, Dark.symbol, Light.symbol, Heart.symbol, Poison.symbol, Jammer.symbol, Unknown.symbol]
        unique_symbols = set(symbols)
        assert len(symbols) == len(unique_symbols), "Pieces' symbols are not unique!"

    def test_piece_properties(self):
        # instantiated pieces should have their initiated coordinate locations returned correctly
        fire = Fire(6, 8)
        assert fire.location == (6, 8), "Instantiated piece's location incorrect!"

        # the unknown piece should be unmatchable
        unknown = Unknown(1, 1)
        assert unknown.matchable is False, "Unknown piece must not be matchable!"
