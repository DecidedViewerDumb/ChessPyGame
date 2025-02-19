from classes.pieces.piece import Piece

class Bishop(Piece):
    def __init__(self, colour, position, cell_size):
        """
        Initialize the bishop.
    :param colour: The colour of the bishop ("black" or "white").
    :param position: The position of the bishop on the board as a tuple (row, col).
    :param cell_size: The size of the board cell.
        """
        image_name = "bB.png" if colour == "black" else "wB.png"
        super().__init__(colour, position, cell_size, image_name)

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the bishop.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # Diagonal move up-left
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].colour != self.colour:
                    valid_moves.append((r, c))
                break  # Break the loop if there is a chess  piece in the way
            r -= 1
            c -= 1

        # Diagonal move up-right
        r, c = row - 1, col + 1
        while r >= 0 and c < 8:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].colour != self.colour:
                    valid_moves.append((r, c))
                break  # Break the loop if there is a chess piece in the way
            r -= 1
            c += 1

        # Diagonal move down-left
        r, c = row + 1, col - 1
        while r < 8 and c >= 0:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].colour != self.colour:
                    valid_moves.append((r, c))
                break  # Break the loop if there is a chess piece in the way
            r += 1
            c -= 1

        # Diagonal move down-right
        r, c = row + 1, col + 1
        while r < 8 and c < 8:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].colour != self.colour:
                    valid_moves.append((r, c))
                break  # Break the loop if there is a chess piece in the way
            r += 1
            c += 1

        return valid_moves
