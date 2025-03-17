from classes.pieces.king import King


class GameStateChecker:
    def __init__(self, board):
        self.board = board

    def is_king_in_check(self, color):
        """
        Checks if the king is in check.
        :param color: The color of the king ("black" or "white").
        :return: True if the king is in check, False otherwise.
        """
        king_pos = self.board.find_king_position(color)
        if not king_pos:
            return False

        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == opponent_color:
                    if king_pos in piece.get_valid_moves(self.board.grid):
                        return True
        return False

    def is_checkmate(self, color):
        """
        Checks if the king is checkmated.
        :param color: The color of the king ("black" or "white").
        :return: True if the king is checkmated, otherwise False.
        """
        if not self.is_king_in_check(color):
            return False

        king_pos = self.board.find_king_position(color)
        if not king_pos:
            return False

        king = self.board.grid[king_pos[0]][king_pos[1]]
        king_moves = king.get_valid_moves(self.board.grid)
        for move in king_moves:
            temp_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
            temp_position = king.position

            self.board.grid[king_pos[0]][king_pos[1]] = None
            self.board.grid[move[0]][move[1]] = king
            king.position = move

            if not self.is_king_in_check(color):
                self.board.grid = temp_grid
                king.position = temp_position
                return False

            self.board.grid = temp_grid
            king.position = temp_position

        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color and not isinstance(piece, King):
                    valid_moves = piece.get_valid_moves(self.board.grid)
                    for move in valid_moves:
                        temp_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
                        temp_position = piece.position

                        self.board.grid[row][col] = None
                        self.board.grid[move[0]][move[1]] = piece
                        piece.position = move

                        if not self.is_king_in_check(color):
                            self.board.grid = temp_grid
                            piece.position = temp_position
                            return False

                        self.board.grid = temp_grid
                        piece.position = temp_position

        return True

    def is_stalemate(self, color):
        """
        Checks if the king is stalemate.
        :param color: The color of the king ("black" or "white").
        :return: True if the king is stalemate, False otherwise.
        """
        if self.is_king_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == color:
                    if piece.get_valid_moves(self.board.grid):
                        return False
        return True

    def find_king_position(self, color):
        """
        Finds the position of the king of the specified color
        """
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        return None
