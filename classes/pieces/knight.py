from classes.pieces.piece import Piece


class Knight(Piece):
    def __init__(self, colour, position, cell_size, start_x, start_y):
        """
        Initialize the knight.
        :param colour: Knight colour ("black" or "white").
        :param position: Knight position on the board as a tuple (row, col).
        :param cell_size: Board cell size.
        :param start_x: Initial X coordinates.
        :param start_y: Initial Y coordinates.
        """
        image_name = "bN.png" if colour == "black" else "wN.png"
        super().__init__(colour, position, cell_size, image_name, start_x, start_y)

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the knight.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # All possible moves of the knight (in the shape of the letter "L")
        moves = [
            (row - 2, col - 1), (row - 2, col + 1),  # Up
            (row - 1, col - 2), (row - 1, col + 2),  # Up-sideways
            (row + 1, col - 2), (row + 1, col + 2),  # Down-sideways
            (row + 2, col - 1), (row + 2, col + 1),  # Down
        ]

        # Checking every move
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:  # Checking that the move is within the board
                target = board[r][c]
                if target is None or target.colour != self.colour:  # The cell is empty or occupied by an enemy piece
                    valid_moves.append((r, c))

        return valid_moves
