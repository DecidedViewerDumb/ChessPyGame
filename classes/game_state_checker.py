from classes.pieces.king import King


class GameStateChecker:
    def __init__(self, board):
        self.board = board

    def is_king_in_check(self, color):
        """
        Проверяет, находится ли король под шахом.
        :param color: Цвет короля ("black" или "white").
        :return: True, если король под шахом, иначе False.
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
        Проверяет, находится ли король под матом.
        :param color: Цвет короля ("black" или "white").
        :return: True, если король под матом, иначе False.
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
        Проверяет, находится ли король под патом.
        :param color: Цвет короля ("black" или "white").
        :return: True, если король под патом, иначе False.
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
