from classes.pieces.piece import Piece


class Rook(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Инициализация ладьи.
        :param color: Цвет ладьи ("black" или "white").
        :param position: Позиция ладьи на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        :param start_x: Начальные координаты по X.
        :param start_y: Начальные координаты по Y.
        """
        image_name = "bR.png" if color == "black" else "wR.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)
        self.has_moved = False  # Флаг, указывающий, двигался ли король

    def get_valid_moves(self, board):
        """
        Возвращает список допустимых ходов для ладьи.
        :param board: Двумерный список, представляющий доску.
        :return: Список допустимых ходов в виде кортежей (row, col).
        """
        valid_moves = []
        row, col = self.position

        # Движение вверх
        for r in range(row - 1, -1, -1):
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].color != self.color:
                    valid_moves.append((r, col))
                break  # Прерываем цикл, если на пути стоит фигура

        # Движение вниз
        for r in range(row + 1, 8):
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].color != self.color:
                    valid_moves.append((r, col))
                break  # Прерываем цикл, если на пути стоит фигура

        # Движение влево
        for c in range(col - 1, -1, -1):
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].color != self.color:
                    valid_moves.append((row, c))
                break  # Прерываем цикл, если на пути стоит фигура

        # Движение вправо
        for c in range(col + 1, 8):
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].color != self.color:
                    valid_moves.append((row, c))
                break  # Прерываем цикл, если на пути стоит фигура

        return valid_moves
