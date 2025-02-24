from classes.pieces.piece import Piece

class Queen(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Initialize the queen.
        :param colour: The queen's colour ("black" or "white").
        :param position: The queen's position on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
        :param start_x: Initial X coordinates.
        :param start_y: Initial Y coordinates.
        """
        image_name = "bQ.png" if colour == "black" else "wQ.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the queen.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # Move horizontally and vertically (like a rook)
        # Up
        r = row - 1
        while r >= 0:
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].colour != self.colour:
                    valid_moves.append((r, col))
                break  # Break the loop if there is a figure in the way
            r -= 1

        # Down
        r = row + 1
        while r < 8:
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].colour != self.colour:
                    valid_moves.append((r, col))
                break  # Break the loop if there is a chess piece in the way
            r += 1

        # Left
        c = col - 1
        while c >= 0:
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].colour != self.colour:
                    valid_moves.append((row, c))
                break  # Break the loop if there is a chess piece in the way
            c -= 1

        # Right
        c = col + 1
        while c < 8:
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].colour != self.colour:
                    valid_moves.append((row, c))
                break  # Break the loop if there is a chess piece in the way
            c += 1

        # Diagonal movement (like an elephant)
        # Up-left
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].colour != self.colour:
                    valid_moves.append((r, c))
                break  # Break the loop if there is a chess piece in the way
            r -= 1
            c -= 1

        # Up-right
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

        # Down-left
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

        # Вниз-вправо
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
