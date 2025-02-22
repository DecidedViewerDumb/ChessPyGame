from classes.pieces.piece import Piece


class Queen(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Инициализация королевы.
        :param color: Цвет королевы ("black" или "white").
        :param position: Позиция королевы на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        :param start_x: Начальные координаты по X.
        :param start_y: Начальные координаты по Y.
        """
        image_name = "bQ.png" if color == "black" else "wQ.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)

    def get_valid_moves(self, board):
        """
        Возвращает список допустимых ходов для королевы.
        :param board: Двумерный список, представляющий доску.
        :return: Список допустимых ходов в виде кортежей (row, col).
        """
        valid_moves = []
        row, col = self.position

        # Движение по горизонтали и вертикали (как у ладьи)
        # Вверх
        r = row - 1
        while r >= 0:
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].color != self.color:
                    valid_moves.append((r, col))
                break  # Прерываем цикл, если на пути стоит фигура
            r -= 1

        # Вниз
        r = row + 1
        while r < 8:
            if board[r][col] is None:
                valid_moves.append((r, col))
            else:
                if board[r][col].color != self.color:
                    valid_moves.append((r, col))
                break  # Прерываем цикл, если на пути стоит фигура
            r += 1

        # Влево
        c = col - 1
        while c >= 0:
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].color != self.color:
                    valid_moves.append((row, c))
                break  # Прерываем цикл, если на пути стоит фигура
            c -= 1

        # Вправо
        c = col + 1
        while c < 8:
            if board[row][c] is None:
                valid_moves.append((row, c))
            else:
                if board[row][c].color != self.color:
                    valid_moves.append((row, c))
                break  # Прерываем цикл, если на пути стоит фигура
            c += 1

        # Движение по диагонали (как у слона)
        # Вверх-влево
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

        # Вверх-вправо
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

        # Вниз-влево
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

        # Вниз-вправо
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
