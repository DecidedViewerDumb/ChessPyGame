from classes.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Initialize the pawn.
        :param colour: The colour of the pawn ("black" or "white").
        :param position: The position of the pawn on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
        :param start_x: Initial X coordinates.
        :param start_y: Initial Y coordinates.
        """
        image_name = "bp.png" if colour == "black" else "wp.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)
        self.has_moved = False  # Flag indicating whether the pawn has moved

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for a pawn.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        valid_moves = []
        row, col = self.position

        # Direction of pawn movement (forward for black and white)
        direction = 1 if self.colour == "black" else -1

        # Move one cell forward
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            valid_moves.append((row + direction, col))

            # Move two squares forward (if the pawn has not moved yet)
            if not self.has_moved and 0 <= row + 2 * direction < 8 and board[row + 2 * direction][col] is None:
                valid_moves.append((row + 2 * direction, col))

        # Taking pieces diagonally
        for dc in [-1, 1]:  # Checking both diagonals
            if 0 <= col + dc < 8 and 0 <= row + direction < 8:
                target = board[row + direction][col + dc]
                if target and target.color != self.color:
                    valid_moves.append((row + direction, col + dc))

        # Взятие на проходе
        if self.board.en_passant_target:
            target_row, target_col = self.board.en_passant_target
            # Проверяем что цель находится на соседней колонке и правильном ряду
            if (row == target_row - direction and
                    abs(col - target_col) == 1 and
                    self.board.grid[target_row][target_col] is None):
                valid_moves.append((target_row, target_col))

        return valid_moves
