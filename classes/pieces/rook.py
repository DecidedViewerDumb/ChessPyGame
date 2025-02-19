from classes.pieces.piece import Piece

class Rook(Piece):
    def __init__(self, colour, position, cell_size):
        """
        Initialize the rook.
        :param colour: The colour of the rook ("black" or "white").
        :param position: The position of the rook on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
        """
        image_name = "bR.png" if colour == "black" else "wR.png"
        super().__init__(colour, position, cell_size, image_name)
        self.has_moved = False  # Flag indicating whether the king has moved

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the rook.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # Upward movement
        for r in range(row - 1, -1, -1):
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].colour != self.colour:
                    valid_moves.append((r, col))
                break  # Break the loop if there is a figure in the way

        # Downward movement
        for r in range(row + 1, 8):
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].colour != self.colour:
                    valid_moves.append((r, col))
                break  # Break the loop if there is a figure in the way

        # Move to the left
        for c in range(col - 1, -1, -1):
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].colour != self.colour:
                    valid_moves.append((row, c))
                break  # Break the loop if there is a figure in the way

        # Move to the right
        for c in range(col + 1, 8):
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].colour != self.colour:
                    valid_moves.append((row, c))
                break  # Break the loop if there is a figure in the way

        return valid_moves
