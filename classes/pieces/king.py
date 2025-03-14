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

        if not self.has_moved:
            # Короткая рокировка (правая ладья)
            if self.can_castle(board, row, col, 7):
                valid_moves.append((row, col + 2))
            # Длинная рокировка (левая ладья)
            if self.can_castle(board, row, col, 0):
                valid_moves.append((row, col - 2))

        # Найдем позицию вражеского короля
        enemy_king_pos = None
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if isinstance(piece, King) and piece.color != self.color:
                    enemy_king_pos = (r, c)
                    break
            if enemy_king_pos:
                break

        # Проверка обычных ходов
        for r, c in moves:
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]

                # Пропускаем свои фигуры
                if target and target.color == self.color:
                    continue

                # Проверка безопасности клетки
                if not self.is_square_attacked(board, r, c):

                    # Проверка расстояния до вражеского короля
                    if enemy_king_pos:
                        enemy_row, enemy_col = enemy_king_pos
                        if abs(r - enemy_row) <= 1 and abs(c - enemy_col) <= 1:
                            continue  # Пропускаем ход, если короли будут рядом

                    valid_moves.append((r, c))

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
        # Проверяем, что король не двигался
        if self.has_moved:
            return False

        # Проверяем, что ладья существует и не двигалась
        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Определяем направление и проверяем пустые клетки между
        step = 1 if rook_col > col else -1
        for c in range(col + step, rook_col, step):
            if board[row][c] is not None:
                return False

        # Проверяем, что король не находится под шахом
        if self.is_square_attacked(board, row, col):
            return False

        # Проверяем, что король не проходит через атакованные клетки
        for c in range(col, rook_col + step, step):
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
