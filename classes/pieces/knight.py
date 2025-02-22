from classes.pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Инициализация коня.
        :param color: Цвет коня ("black" или "white").
        :param position: Позиция коня на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        :param start_x: Начальные координаты по X.
        :param start_y: Начальные координаты по Y.
        """
        image_name = "bN.png" if color == "black" else "wN.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)

    def get_valid_moves(self, board):
        """
        Возвращает список допустимых ходов для коня.
        :param board: Двумерный список, представляющий доску.
        :return: Список допустимых ходов в виде кортежей (row, col).
        """
        valid_moves = []
        row, col = self.position

        # Все возможные ходы коня (в форме буквы "Г")
        moves = [
            (row - 2, col - 1), (row - 2, col + 1),  # Вверх
            (row - 1, col - 2), (row - 1, col + 2),  # Вверх-вбок
            (row + 1, col - 2), (row + 1, col + 2),  # Вниз-вбок
            (row + 2, col - 1), (row + 2, col + 1),  # Вниз
        ]

        # Проверяем каждый ход
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:  # Проверяем, что ход находится в пределах доски
                target = board[r][c]
                if target is None or target.color != self.color:  # Клетка пуста или занята фигурой противника
                    valid_moves.append((r, c))

        return valid_moves
