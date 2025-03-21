from classes.pieces.piece import Piece


class Rook(Piece):
    def __init__(self, colour, position, cell_size, start_x, start_y):
        """
        Initialize the rook.
        :param colour: The colour of the rook ("black" or "white").
        :param position: The position of the rook on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
        :param start_x: The initial X coordinates.
        :param start_y: The initial Y coordinates.
        """
        image_name = "bR.png" if colour == "black" else "wR.png"
        super().__init__(colour, position, cell_size, image_name, start_x, start_y)
        self.has_moved = False  # A flag indicating whether the king has moved
    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the rook.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # Moving up
        for r in range(row - 1, -1, -1):
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].colour != self.colour:
                    valid_moves.append((r, col))
                break  # Breaking the loop if there is a chess piece in the way

        # Moving down
        for r in range(row + 1, 8):
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].colour != self.colour:
                    valid_moves.append((r, col))
                break  # Breaking the loop if there is a chess piece in the way

        # Moving left
        for c in range(col - 1, -1, -1):
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].colour != self.colour:
                    valid_moves.append((row, c))
                break  # Breaking the loop if there is a chess piece in the way

        # Moving right
        for c in range(col + 1, 8):
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].colour != self.colour:
                    valid_moves.append((row, c))
                break  # Breaking the loop if there is a chess piece in the way

        return valid_moves
