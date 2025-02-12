import random


class RandomAI:
    def __init__(self, board):
        """
        Инициализация AI.
        :param board: Объект доски (Board).
        """
        self.board = board

    def get_random_move(self):
        """
        Возвращает случайный допустимый ход для чёрных.
        :return: Кортеж ((start_row, start_col), (end_row, end_col)), представляющий ход.
        """
        valid_moves = self.get_all_valid_moves_for_black()
        if valid_moves:
            return random.choice(valid_moves)
        return None

    def get_all_valid_moves_for_black(self):
        """
        Возвращает все допустимые ходы для чёрных.
        :return: Список кортежей ((start_row, start_col), (end_row, end_col)).
        """
        valid_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece and piece.color == "black":
                    moves = piece.get_valid_moves(self.board.grid)
                    for move in moves:
                        valid_moves.append(((row, col), move))
        return valid_moves
