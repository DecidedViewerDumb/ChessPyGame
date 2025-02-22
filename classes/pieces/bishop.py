from classes.pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Инициализация слона.
        :param color: Цвет слона ("black" или "white").
        :param position: Позиция слона на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        :param start_x: Начальные координаты по X.
        :param start_y: Начальные координаты по Y.
        """
        image_name = "bB.png" if color == "black" else "wB.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)

    def get_valid_moves(self, board):
        """
        Возвращает список допустимых ходов для слона.
        :param board: Двумерный список, представляющий доску.
        :return: Список допустимых ходов в виде кортежей (row, col).
        """
        valid_moves = []
        row, col = self.position

        # Движение по диагонали вверх-влево
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Прерываем цикл, если на пути стоит фигура
            r -= 1
            c -= 1

        # Движение по диагонали вверх-вправо
        r, c = row - 1, col + 1
        while r >= 0 and c < 8:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Прерываем цикл, если на пути стоит фигура
            r -= 1
            c += 1

        # Движение по диагонали вниз-влево
        r, c = row + 1, col - 1
        while r < 8 and c >= 0:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Прерываем цикл, если на пути стоит фигура
            r += 1
            c -= 1

        # Движение по диагонали вниз-вправо
        r, c = row + 1, col + 1
        while r < 8 and c < 8:
            if board[r][c] is None:
                valid_moves.append((r, c))
            else:
                if board[r][c].color != self.color:
                    valid_moves.append((r, c))
                break  # Прерываем цикл, если на пути стоит фигура
            r += 1
            c += 1

        return valid_moves
