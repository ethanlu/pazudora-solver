from pazudora.board import Board

class Solver(object):
    def __init__(self, piece_weights):
        self._piece_weights = piece_weights

    def solve(self, board, search_depth):
        moves = []
        for s in range(0, search_depth):

        return return []


if __name__ == "__main__":
    rows = 10
    columns = 10
    search_depth = 30

    s = Solver()
    moves = s.solve(Board.create_randomized_board(rows, columns), search_depth)

    print moves