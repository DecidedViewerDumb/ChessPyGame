from classes.pieces.bishop import Bishop
from classes.pieces.knight import Knight
from classes.pieces.pawn import Pawn
from classes.pieces.piece import Piece
from classes.pieces.queen import Queen
from classes.pieces.rook import Rook


class King(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Initialize the king.
        :param color: The color of the king ("black" or "white").
        :param position: The position of the king on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
        :param start_x: The initial X coordinates.
        :param start_y: The initial Y coordinates.
        """
        image_name = "bK.png" if color == "black" else "wK.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)
        self.has_moved = False  # A flag indicating whether the king has moved

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
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),  # Lower cells
        ]

        if not self.has_moved:
            # Kingside castling
            if self.can_castle(board, row, col, 7):
                valid_moves.append((row, col + 2))
            # Queenside castling
            if self.can_castle(board, row, col, 0):
                valid_moves.append((row, col - 2))

        # Finding the enemy kings position
        enemy_king_pos = None
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if isinstance(piece, King) and piece.color != self.color:
                    enemy_king_pos = (r, c)
                    break
            if enemy_king_pos:
                break

        # Checking the normal moves
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]

                # Skipping our chess pieces
                if target and target.color == self.color:
                    continue

                # Checking safety of squares
                if not self.is_square_attacked(board, r, c):

                    # Checking the distance to the enemy king
                    if enemy_king_pos:
                        enemy_row, enemy_col = enemy_king_pos
                        if abs(r - enemy_row) <= 1 and abs(c - enemy_col) <= 1:
                            continue  # Skip a move if the kings are nearby

                    valid_moves.append((r, c))

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
        # Checking that the king has not moved.
        if self.has_moved:
            return False

        # Checking that the rook exists and has not moved.
        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Determining the direction and check the empty cells between
        step = 1 if rook_col > col else -1
        for c in range(col + step, rook_col, step):
            if board[row][c] is not None:
                return False

        # Checking that the king is not in check
        if self.is_square_attacked(board, row, col):
            return False

        # Checking that the king does not pass through the attacked cells
        for c in range(col, rook_col + step, step):
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
        opponent_color = "black" if self.color == "white" else "white"

        # Checking pawn attacks
        pawn_direction = 1 if opponent_color == "black" else -1  # Black pawns move down (increase row)

        # Checking diagonal squares for pawn capture
        attack_squares = [
            (row - pawn_direction, col - 1),
            (row - pawn_direction, col + 1)
        ]

        for r, c in attack_squares:
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if isinstance(piece, Pawn) and piece.color == opponent_color:
                    return True

        # Checking the attacks of the knights
        knight_moves = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1),
        ]
        for r, c in knight_moves:
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if isinstance(piece, Knight) and piece.color == opponent_color:
                    return True

        # Checking the attacks of bishops, rooks and queens
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece is not None:
                    if piece.color == opponent_color:
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
