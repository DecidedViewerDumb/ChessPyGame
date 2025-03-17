from classes.pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Initialize the bishop.
        :param color: The color of the bishop ("black" or "white").
        :param position: The position of the bishop on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
        :param start_x: The initial X coordinates.
        :param start_y: The initial Y coordinates.
        """
        image_name = "bB.png" if color == "black" else "wB.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the bishop.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # Diagonal movement up-left
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Breaking the loop if there is a chess piece in the way
            r -= 1
            c -= 1

        # Move diagonally up-right
        r, c = row - 1, col + 1
        while r >= 0 and c < 8:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Breaking the loop if there is a chess piece in the way
            r -= 1
            c += 1

        # Diagonal movement down-left
        r, c = row + 1, col - 1
        while r < 8 and c >= 0:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Break the loop if there is a chess piece in the way
            r += 1
            c -= 1

        # Move diagonally down-right
        r, c = row + 1, col + 1
        while r < 8 and c < 8:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Break the loop if there is a chess piece in the way
            r += 1
            c += 1

        return valid_moves
