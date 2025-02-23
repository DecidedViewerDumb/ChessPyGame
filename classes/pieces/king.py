from classes.pieces.bishop import Bishop
from classes.pieces.knight import Knight
from classes.pieces.pawn import Pawn
from classes.pieces.piece import Piece
from classes.pieces.queen import Queen
from classes.pieces.rook import Rook


class King(Piece):
    def __init__(self, color, position, cell_size, start_x, start_y):
        """
        Инициализация короля.
        :param color: Цвет короля ("black" или "white").
        :param position: Позиция короля на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        :param start_x: Начальные координаты по X.
        :param start_y: Начальные координаты по Y.
        """
        image_name = "bK.png" if color == "black" else "wK.png"
        super().__init__(color, position, cell_size, image_name, start_x, start_y)
        self.has_moved = False  # Флаг, указывающий, двигался ли король

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

        # Проверка обычных ходов
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]

                # Пропускаем свои фигуры
                if target and target.color == self.color:
                    continue

                # Временное перемещение короля
                original = board[row][col]
                temp = board[r][c]
                board[row][col] = None
                board[r][c] = self
                self.position = (r, c)

                # Проверка безопасности клетки
                if not self.is_square_attacked(board, r, c):
                    valid_moves.append((r, c))

                # Восстановление доски
                board[row][col] = original
                board[r][c] = temp
                self.position = (row, col)

        return valid_moves

    def can_castle(self, board, row, col, rook_col):
        """
        Проверяет, возможна ли рокировка.
        :param board: Двумерный список, представляющий доску.
        :param row: Строка короля.
        :param col: Столбец короля.
        :param rook_col: Столбец ладьи (0 для длинной рокировки, 7 для короткой).
        :return: True, если рокировка возможна, иначе False.
        """
        # Проверяем, что ладья существует и не двигалась
        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Проверяем, что клетки между королем и ладьей пусты
        if rook_col == 0:  # Длинная рокировка
            for c in range(col - 1, rook_col, -1):
                if board[row][c] is not None:
                    return False
        else:  # Короткая рокировка
            for c in range(col + 1, rook_col):
                if board[row][c] is not None:
                    return False

        # Проверяем, что король не находится под шахом
        if self.is_square_attacked(board, row, col):
            return False

        # Проверяем, что клетки, через которые проходит король, не атакованы
        if rook_col == 0:  # Длинная рокировка
            for c in range(col - 1, rook_col, -1):
                if self.is_square_attacked(board, row, c):
                    return False
        else:  # Короткая рокировка
            for c in range(col + 1, rook_col):
                if self.is_square_attacked(board, row, c):
                    return False

        return True

    def is_square_attacked(self, board, row, col):
        """
        Проверяет, атакована ли клетка.
        :param board: Двумерный список, представляющий доску.
        :param row: Строка клетки.
        :param col: Столбец клетки.
        :return: True, если клетка атакована, иначе False.
        """
        opponent_color = "black" if self.color == "white" else "white"

        # Проверка атак пешек
        pawn_direction = 1 if opponent_color == "black" else -1  # Черные пешки двигаются вниз (увеличение row)

        # Проверяем диагональные клетки для взятия пешкой
        attack_squares = [
            (row - pawn_direction, col - 1),
            (row - pawn_direction, col + 1)
        ]

        for r, c in attack_squares:
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if isinstance(piece, Pawn) and piece.color == opponent_color:
                    return True

        # Проверяем атаки коней
        knight_moves = [
            (row - 2, col - 1), (row - 2, col + 1),
            (row - 1, col - 2), (row - 1, col + 2),
            (row + 1, col - 2), (row + 1, col + 2),
            (row + 2, col - 1), (row + 2, col + 1),
        ]
        for r, c in knight_moves:
            if 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if isinstance(piece, Knight) and piece.color == opponent_color:
                    return True

        # Проверяем атаки слонов, ладей и ферзей
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = board[r][c]
                if piece is not None:
                    if piece.color == opponent_color:
                        if isinstance(piece, Bishop) and abs(dr) == abs(dc):
                            return True
                        if isinstance(piece, Rook) and (dr == 0 or dc == 0):
                            return True
                        if isinstance(piece, Queen):
                            return True
                    break
                r += dr
                c += dc

        return False
