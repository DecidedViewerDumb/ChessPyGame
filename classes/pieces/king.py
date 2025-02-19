from classes.pieces.bishop import Bishop
from classes.pieces.knight import Knight
from classes.pieces.pawn import Pawn
from classes.pieces.piece import Piece
from classes.pieces.queen import Queen
from classes.pieces.rook import Rook

class King(Piece):
    def __init__(self, colour, position, cell_size):
        """
        Initialize the king.
        :param colour: The colour of the king ("black" or "white").
        :param position: The position of the king on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
            """
        image_name = "bK.png" if colour == "black" else "wK.png"
        super().__init__(colour, position, cell_size, image_name)
        self.has_moved = False  # Flag indicating whether the king has moved

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the king.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # All possible moves of the king (all adjacent cells)
        moves = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),  # Upper cells
            (row, col - 1), (row, col + 1),  # Side cells
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),  # Bottom cells
        ]

        # Check every move
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:  # Check that the move is within the board
                target = board[r][c]
                if target is None or target.colour != self.colour:  # The cell is empty or occupied by an enemy piece
                    valid_moves.append((r, c))

        # Add castling if the king and rook have not moved
        if not self.has_moved:
            # Kingside castling
            if self.can_castle(board, row, col, 7):
                valid_moves.append((row, col + 2))

            # Queenside castling
            if self.can_castle(board, row, col, 0):
                valid_moves.append((row, col - 2))

        return valid_moves

    def can_castle(self, board, row, col, rook_col):
        """
        Checks if castling is possible.
        :param board: A two-dimensional list representing the board.
        :param row: The king's row.
        :param col: The king's column.
        :param rook_col: The rook's column (0 for long castling, 7 for short castling).
        :return: True if castling is possible, otherwise False.
        """
        # Check that the rook exists and has not moved
        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Check that the squares between the king and the rook are empty
        if rook_col == 0:  # Queenside  castling
            for c in range(col - 1, rook_col, -1):
                if board[row][c] is not None:
                    return False
        else:  # Kingside castling
            for c in range(col + 1, rook_col):
                if board[row][c] is not None:
                    return False

        # Check that the king is not in check
        if self.is_square_attacked(board, row, col):
            return False

        # Check that the cells the king passes through are not attacked
        if rook_col == 0:  # Queenside castling
            for c in range(col - 1, rook_col, -1):
                if self.is_square_attacked(board, row, c):
                    return False
        else:  # Kingside castling
            for c in range(col + 1, rook_col):
                if self.is_square_attacked(board, row, c):
                    return False

        return True

    def is_square_attacked(self, board, row, col):
        """
        Checks if the cell is attacked.
        :param board: A two-dimensional list representing the board.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :return: True if the cell is attacked, otherwise False.
                """
        opponent_colour = "black" if self.colour == "white" else "white"

        # Checking pawn attacks
        direction = 1 if opponent_colour == "black" else -1
        for dc in [-1, 1]:
            r = row + direction
            c = col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if isinstance(piece, Pawn) and piece.colour == opponent_colour:
                    return True

        # Checking the knight attacks
        knight_moves = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1),
        ]
        for r, c in knight_moves:
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if isinstance(piece, Knight) and piece.colour == opponent_colour:
                    return True

        # # Checking the bishop, rook and queen attacks
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece is not None:
                    if piece.colour == opponent_colour:
                        if isinstance(piece, Bishop) and abs(dr) == abs(dc):
                            return True
                        if isinstance(piece, Rook) and (dr == 0 or dc == 0):
                            return True
                        if isinstance(piece, Queen):
                            return True
                    break
                r += dr
                c += dc

        return False
