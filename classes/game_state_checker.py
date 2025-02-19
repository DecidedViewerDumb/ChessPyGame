from classes.pieces.king import King

class GameStateChecker:
    def __init__(self, board):
        self.board = board

    def is_king_in_check(self, colour):
        """
        Checks if the king is in check.
        :param colour: The colour of the king ("black" or "white").
        :return: True if the king is in check, False otherwise.
        """
        king_pos = self.board.find_king_position(colour)
        if not king_pos:
            return False

        opponent_colourr = "black" if colour == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.colour == opponent_colour:
                    if king_pos in piece.get_valid_moves(self.board.grid):
                        return True
        return False

    def is_checkmate(self, colour):
        """
        Checks if the king is checkmated.
        :param colour: The colour of the king ("black" or "white").
        :return: True if the king is checkmated, otherwise False.
        """
        if not self.is_king_in_check(colour):
            return False

        king_pos = self.board.find_king_position(colour)
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

            if not self.is_king_in_check(colour):
                self.board.grid = temp_grid
                king.position = temp_position
                return False

            self.board.grid = temp_grid
            king.position = temp_position

        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.colour == colour and not isinstance(piece, King):
                    valid_moves = piece.get_valid_moves(self.board.grid)
                    for move in valid_moves:
                        temp_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
                        temp_position = piece.position

                        self.board.grid[row][col] = None
                        self.board.grid[move[0]][move[1]] = piece
                        piece.position = move

                        if not self.is_king_in_check(colour):
                            self.board.grid = temp_grid
                            piece.position = temp_position
                            return False

                        self.board.grid = temp_grid
                        piece.position = temp_position

        return True

    def is_stalemate(self, colour):
        """
        Checks if the king is stalemate.
        :param colour: The colour of the king ("black" or "white").
        :return: True if the king is stalemate, False otherwise.
        """
        if self.is_king_in_check(colour):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.colour == colour:
                    if piece.get_valid_moves(self.board.grid):
                        return False
        return True
