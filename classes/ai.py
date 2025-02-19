import random

class RandomAI:
    def __init__(self, board):
        """
        Initialize AI.
        :param board: Board object.
        """
        self.board = board

    def get_random_move(self):
        """
        Returns a random legal move for black.
        :return: A tuple ((start_row, start_col), (end_row, end_col)) representing the move.
        """
        valid_moves = self.get_all_valid_moves_for_black()
        if valid_moves:
            return random.choice(valid_moves)
        return None

    def get_all_valid_moves_for_black(self):
        """
        Returns all legal moves for black.
        :return: List of tuples ((start_row, start_col), (end_row, end_col)).
        """
        valid_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.colour == "black":
                    moves = piece.get_valid_moves(self.board.grid)
                    for move in moves:
                        valid_moves.append(((row, col), move))
        return valid_moves
