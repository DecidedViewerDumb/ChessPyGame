import datetime
import os
from classes.pieces.king import King
from classes.pieces.pawn import Pawn


class MoveHandler:
    def __init__(self, board):
        self.board = board
        self.start_time = datetime.datetime.now()  # Время начала партии
        self.log_file = self.create_log_file()  # Создаем файл для записи ходов

    def __del__(self):
        """
        Закрываем файл при уничтожении объекта.
        """
        if hasattr(self, 'log_file'):
            self.log_file.close()

    def create_log_file(self):
        """
        Создает файл для записи ходов.
        :return: Файловый объект.
        """
        if not os.path.exists("data"):
            os.makedirs("data")
        filename = f"data/Партия от {self.start_time.strftime('%Y-%m-%d %H-%M-%S')}.txt"
        return open(filename, "w", encoding="utf-8")

    def convert_to_chess_notation(self, position):
        """
        Преобразует координаты из числового формата (строка, столбец) в шахматный формат (буква столбца и номер строки).
        :param position: Кортеж (строка, столбец).
        :return: Строка в шахматной нотации (например, "a1").
        """
        row, col = position
        # Преобразуем столбец в букву (0 -> 'a', 1 -> 'b', ..., 7 -> 'h')
        col_char = chr(ord('a') + col)
        # Преобразуем строку в номер (0 -> 8, 1 -> 7, ..., 7 -> 1)
        row_num = 8 - row
        return f"{col_char}{row_num}"

    def log_move(self, move):
        """
        Записывает ход в файл в шахматной нотации.
        :param move: Ход в формате ((start_row, start_col), (end_row, end_col)).
        """
        start_pos, end_pos = move
        start_chess = self.convert_to_chess_notation(start_pos)
        end_chess = self.convert_to_chess_notation(end_pos)
        move_str = f"{self.board.current_player} {start_chess} -> {end_chess}\n"
        self.log_file.write(move_str)
        self.log_file.flush()  # Сбрасываем буфер, чтобы данные сразу записывались в файл

    def handle_click(self, row, col):
        """
        Обрабатывает клик на клетку доски.
        :param row: Строка клетки.
        :param col: Столбец клетки.
        """
        if self.board.selected_piece is None:
            # Если фигура не выбрана, выбираем фигуру текущего игрока
            piece = self.board.grid[row][col]
            if piece is not None and piece.color == self.board.current_player:
                self.board.selected_piece = piece
                self.board.valid_moves = piece.get_valid_moves(self.board.grid)

                # Фильтруем допустимые ходы, если король под шахом
                if self.board.is_king_in_check(self.board.current_player):
                    self.board.valid_moves = self.filter_moves_in_check(self.board.selected_piece, self.board.valid_moves)
        else:
            # Если фигура уже выбрана, проверяем, куда кликнул игрок
            if (row, col) == self.board.selected_piece.position:
                # Если кликнули на ту же фигуру, отменяем выбор
                self.board.selected_piece = None
                self.board.valid_moves = []
            elif (row, col) in self.board.valid_moves:
                # Если кликнули на допустимый ход, выполняем его
                self.make_move(row, col)
            else:
                # Если кликнули на другую фигуру, выбираем её (если она принадлежит текущему игроку)
                piece = self.board.grid[row][col]
                if piece is not None and piece.color == self.board.current_player:
                    self.board.selected_piece = piece
                    self.board.valid_moves = piece.get_valid_moves(self.board.grid)

                    # Фильтруем допустимые ходы, если король под шахом
                    if self.board.is_king_in_check(self.board.current_player):
                        self.board.valid_moves = self.filter_moves_in_check(self.board.selected_piece, self.board.valid_moves)

    def filter_moves_in_check(self, piece, valid_moves):
        """
        Фильтрует допустимые ходы, оставляя только те, которые убирают короля из-под шаха.
        :param piece: Фигура, которая ходит.
        :param valid_moves: Список допустимых ходов.
        :return: Отфильтрованный список допустимых ходов.
        """
        filtered_moves = []

        for move in valid_moves:
            # Сохраняем текущее состояние доски
            temp_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
            temp_position = piece.position

            # Выполняем ход
            self.board.grid[piece.position[0]][piece.position[1]] = None
            self.board.grid[move[0]][move[1]] = piece
            piece.position = move

            # Проверяем, остался ли король под шахом
            if not self.board.is_king_in_check(self.board.current_player):
                filtered_moves.append(move)

            # Восстанавливаем исходное состояние доски
            self.board.grid = [[temp_grid[row][col] for col in range(8)] for row in range(8)]
            piece.position = temp_position

        return filtered_moves

    def make_move(self, row, col):
        """
        Выполняет ход фигуры.
        :param row: Строка клетки.
        :param col: Столбец клетки.
        """
        original_grid = [[self.board.grid[row][col] for col in range(8)] for row in range(8)]
        original_position = self.board.selected_piece.position
        start_row, start_col = original_position
        piece = self.board.selected_piece

        # Сброс флага взятия на проходе
        self.board.en_passant_target = None

        # Обработка взятия на проходе
        if isinstance(piece, Pawn):
            # Ход на две клетки - устанавливаем правильную целевую позицию
            if abs(row - start_row) == 2:
                direction = 1 if piece.color == "black" else -1
                self.board.en_passant_target = (start_row + direction, start_col)  # Позиция ПРОМЕЖУТОЧНОЙ клетки

            # Выполнение взятия на проходе
            if col != start_col and self.board.grid[row][col] is None:
                # Удаляем пешку противника
                captured_row = start_row  # Ряд где стояла атакующая пешка
                captured_col = col  # Колонка куда пошла цель
                self.board.grid[captured_row][captured_col] = None

        # Логируем ход
        start_pos = self.board.selected_piece.position
        end_pos = (row, col)
        self.log_move((start_pos, end_pos))

        # Проверяем, является ли ход рокировкой
        if isinstance(self.board.selected_piece, King) and abs(col - original_position[1]) == 2:
            self.handle_castle(row, col)
        else:
            # Обычный ход
            self.board.grid[self.board.selected_piece.position[0]][self.board.selected_piece.position[1]] = None
            self.board.grid[row][col] = self.board.selected_piece
            self.board.selected_piece.position = (row, col)

            # Проверяем, остался ли король под шахом после хода
            if self.board.is_king_in_check(self.board.current_player):
                # Если король под шахом, отменяем ход
                self.board.grid = original_grid
                self.board.selected_piece.position = original_position
            else:
                # Если ход допустим, завершаем его
                if self.board.grid[row][col] is not None and self.board.grid[row][col].color != self.board.current_player:
                    self.board.grid[row][col] = None

                # Устанавливаем флаг has_moved для пешки
                if isinstance(self.board.selected_piece, Pawn):
                    self.board.selected_piece.has_moved = True

                # Меняем игрока
                self.board.current_player = "black" if self.board.current_player == "white" else "white"

        # Обновление флага has_moved для пешки
        if isinstance(piece, Pawn):
            piece.has_moved = True

        # Сбрасываем выбор фигуры
        self.board.selected_piece = None
        self.board.valid_moves = []

    def handle_castle(self, row, col):
        """
        Выполняет рокировку.
        :param row: Строка короля.
        :param col: Столбец короля после рокировки.
        """
        king = self.board.selected_piece
        king_row, king_col = king.position

        # Определяем направление рокировки
        if col > king_col:  # Короткая рокировка
            rook_col = 7
            new_rook_col = col - 1
        else:  # Длинная рокировка
            rook_col = 0
            new_rook_col = col + 1

        # Перемещаем короля
        self.board.grid[king_row][king_col] = None
        self.board.grid[row][col] = king
        king.position = (row, col)
        king.has_moved = True

        # Перемещаем ладью
        rook = self.board.grid[king_row][rook_col]
        self.board.grid[king_row][rook_col] = None
        self.board.grid[king_row][new_rook_col] = rook
        rook.position = (king_row, new_rook_col)
        rook.has_moved = True

        # Меняем игрока
        self.board.current_player = "black" if self.board.current_player == "white" else "white"
