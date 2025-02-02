from classes.pieces.piece import Piece


class King(Piece):
    def __init__(self, color, position, cell_size):
        """
        Инициализация короля.
        :param color: Цвет короля ("black" или "white").
        :param position: Позиция короля на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        """
        image_name = "bK.png" if color == "black" else "wK.png"
        super().__init__(color, position, cell_size, image_name)

    def get_valid_moves(self, board):
        """
        Возвращает список допустимых ходов для короля.
        :param board: Двумерный список, представляющий доску.
        :return: Список допустимых ходов в виде кортежей (row, col).
        """
        valid_moves = []
        row, col = self.position

        # Все возможные ходы короля (все соседние клетки)
        moves = [
            (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),  # Верхние клетки
            (row, col - 1), (row, col + 1),  # Боковые клетки
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1),  # Нижние клетки
        ]

        # Проверяем каждый ход
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:  # Проверяем, что ход находится в пределах доски
                target = board[r][c]
                if target is None or target.color != self.color:  # Клетка пуста или занята фигурой противника
                    valid_moves.append((r, c))

        return valid_moves
