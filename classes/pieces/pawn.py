from classes.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Инициализация пешки.
        :param color: Цвет пешки ("black" или "white").
        :param position: Позиция пешки на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        :param start_x: Начальные координаты по X.
        :param start_y: Начальные координаты по Y.
        """
        image_name = "bp.png" if color == "black" else "wp.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)
        self.has_moved = False  # Флаг, указывающий, двигалась ли пешка

    def get_valid_moves(self, board):
        """
        Возвращает список допустимых ходов для пешки.
        :param board: Двумерный список, представляющий доску.
        :return: Список допустимых ходов в виде кортежей (row, col).
        """
        valid_moves = []
        row, col = self.position

        # Направление движения пешки (вперед для черных и белых)
        direction = 1 if self.color == "black" else -1

        # Ход на одну клетку вперед
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            valid_moves.append((row + direction, col))

            # Ход на две клетки вперед (если пешка еще не двигалась)
            if not self.has_moved and 0 <= row + 2 * direction < 8 and board[row + 2 * direction][col] is None:
                valid_moves.append((row + 2 * direction, col))

        # Взятие фигур по диагонали
        for dc in [-1, 1]:  # Проверяем обе диагонали
            if 0 <= col + dc < 8 and 0 <= row + direction < 8:
                target = board[row + direction][col + dc]
                if target and target.color != self.color:
                    valid_moves.append((row + direction, col + dc))

        # Взятие на проходе
        if self.board.en_passant_target:
            target_row, target_col = self.board.en_passant_target
            # Проверяем что цель находится на соседней колонке и правильном ряду
            if (row == target_row - direction and
                    abs(col - target_col) == 1 and
                    self.board.grid[target_row][target_col] is None):
                valid_moves.append((target_row, target_col))

        return valid_moves
