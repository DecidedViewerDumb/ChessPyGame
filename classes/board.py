import pygame

from classes.pieces.king import King
from classes.pieces.pawn import Pawn
from classes.pieces.rook import Rook
from classes.pieces.knight import Knight
from classes.pieces.bishop import Bishop
from classes.pieces.queen import Queen


class Board:
    def __init__(self, screen_width, screen_height):
        """
        Инициализация доски.
        :param screen_width: Ширина экрана.
        :param screen_height: Высота экрана.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = min(screen_width, screen_height) // 8  # Размер клетки доски

        # Инициализация двумерного списка для хранения фигур
        self.grid = [[None for _ in range(8)] for _ in range(8)]  # 8x8, изначально все клетки пусты

        # Добавляем фигуры на доску
        self.add_pieces()

        # Текущий выделенный фигура и допустимые ходы
        self.selected_piece = None
        self.valid_moves = []

        # Текущий игрок ("white" или "black")
        self.current_player = "white"

        # Шрифт для отображения информации о текущем игроке
        self.font = pygame.font.Font(None, 36)

    def is_king_in_check(self, color):
        """
        Проверяет, находится ли король под шахом.
        :param color: Цвет короля ("black" или "white").
        :return: True, если король под шахом, иначе False.
        """
        # Находим позицию короля
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            return False  # Король не найден (невозможная ситуация)

        # Проверяем, атакована ли клетка короля фигурами противника
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == opponent_color:
                    if king_pos in piece.get_valid_moves(self.grid):
                        return True
        return False

    def is_checkmate(self, color):
        """
        Проверяет, находится ли король под матом.
        :param color: Цвет короля ("black" или "white").
        :return: True, если король под матом, иначе False.
        """
        if not self.is_king_in_check(color):
            return False  # Король не под шахом

        # Проверяем, есть ли допустимые ходы для короля
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    if piece.get_valid_moves(self.grid):
                        return False  # Есть допустимые ходы
        return True

    def is_stalemate(self, color):
        """
        Проверяет, находится ли король под патом.
        :param color: Цвет короля ("black" или "white").
        :return: True, если король под патом, иначе False.
        """
        if self.is_king_in_check(color):
            return False  # Король под шахом, это не пат

        # Проверяем, есть ли допустимые ходы для короля
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    if piece.get_valid_moves(self.grid):
                        return False  # Есть допустимые ходы
        return True

    def add_pieces(self):
        """
        Добавляет фигуры на доску.
        """
        # Добавляем черные пешки
        for col in range(8):
            self.grid[1][col] = Pawn("black", (1, col), self.cell_size)

        # Добавляем белые пешки
        for col in range(8):
            self.grid[6][col] = Pawn("white", (6, col), self.cell_size)

        # Добавляем черные ладьи
        self.grid[0][0] = Rook("black", (0, 0), self.cell_size)
        self.grid[0][7] = Rook("black", (0, 7), self.cell_size)

        # Добавляем белые ладьи
        self.grid[7][0] = Rook("white", (7, 0), self.cell_size)
        self.grid[7][7] = Rook("white", (7, 7), self.cell_size)

        # Добавляем черных коней
        self.grid[0][1] = Knight("black", (0, 1), self.cell_size)
        self.grid[0][6] = Knight("black", (0, 6), self.cell_size)

        # Добавляем белых коней
        self.grid[7][1] = Knight("white", (7, 1), self.cell_size)
        self.grid[7][6] = Knight("white", (7, 6), self.cell_size)

        # Добавляем черных слонов
        self.grid[0][2] = Bishop("black", (0, 2), self.cell_size)
        self.grid[0][5] = Bishop("black", (0, 5), self.cell_size)

        # Добавляем белых слонов
        self.grid[7][2] = Bishop("white", (7, 2), self.cell_size)
        self.grid[7][5] = Bishop("white", (7, 5), self.cell_size)

        # Добавляем черную королеву
        self.grid[0][3] = Queen("black", (0, 3), self.cell_size)

        # Добавляем белую королеву
        self.grid[7][3] = Queen("white", (7, 3), self.cell_size)

        # Добавляем черного короля
        self.grid[0][4] = King("black", (0, 4), self.cell_size)

        # Добавляем белого короля
        self.grid[7][4] = King("white", (7, 4), self.cell_size)

    def draw(self, screen):
        """
        Отрисовка доски и фигур.
        :param screen: Экран, на котором отрисовывается доска.
        """
        colors = [(235, 235, 208), (119, 149, 86)]  # Цвета клеток (белый и зеленый)

        for row in range(8):
            for col in range(8):
                # Определяем цвет клетки
                color = colors[(row + col) % 2]
                # Вычисляем координаты клетки
                x = col * self.cell_size
                y = row * self.cell_size
                # Отрисовываем клетку
                pygame.draw.rect(screen, color, (x, y, self.cell_size, self.cell_size))

                # Если клетка выделена, отрисовываем её с другим цветом
                if (row, col) in self.valid_moves:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 3)

                # Если в клетке есть фигура, отрисовываем её
                if self.grid[row][col] is not None:
                    self.grid[row][col].draw(screen)

        # Отрисовка информации о текущем игроке
        text = self.font.render(f"Ход: {self.current_player}", True, (255, 255, 255))
        screen.blit(text, (self.screen_width - 150, 275))

        # Проверка на шах и отрисовка клетки короля, если он под шахом
        if self.is_king_in_check("white"):
            king_pos = self.find_king_position("white")
            if king_pos:
                x = king_pos[1] * self.cell_size
                y = king_pos[0] * self.cell_size
                pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 5)
        if self.is_king_in_check("black"):
            king_pos = self.find_king_position("black")
            if king_pos:
                x = king_pos[1] * self.cell_size
                y = king_pos[0] * self.cell_size
                pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 5)

    def find_king_position(self, color):
        """
        Находит позицию короля на доске.
        :param color: Цвет короля ("black" или "white").
        :return: Позиция короля в виде кортежа (row, col).
        """
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        return None

    def handle_click(self, row, col):
        """
        Обрабатывает клик на клетку доски.
        :param row: Строка клетки.
        :param col: Столбец клетки.
        """
        if self.selected_piece is None:
            # Выделяем фигуру, если она принадлежит текущему игроку
            piece = self.grid[row][col]
            if piece is not None and piece.color == self.current_player:
                self.selected_piece = piece
                self.valid_moves = piece.get_valid_moves(self.grid)

                # Фильтруем допустимые ходы: оставляем только те, которые убирают короля из-под шаха
                if self.is_king_in_check(self.current_player):
                    self.valid_moves = self.filter_moves_in_check(self.selected_piece, self.valid_moves)
        else:
            # Перемещаем фигуру, если ход допустим
            if (row, col) in self.valid_moves:
                # Сохраняем текущее состояние доски
                original_grid = [[self.grid[row][col] for col in range(8)] for row in range(8)]
                original_position = self.selected_piece.position

                # Перемещаем фигуру
                self.grid[self.selected_piece.position[0]][self.selected_piece.position[1]] = None
                self.grid[row][col] = self.selected_piece
                self.selected_piece.position = (row, col)

                # Проверяем, остался ли король под шахом после хода
                if self.is_king_in_check(self.current_player):
                    # Если король все еще под шахом, отменяем ход
                    self.grid = original_grid
                    self.selected_piece.position = original_position
                else:
                    # Удаляем фигуру противника, если она есть
                    if self.grid[row][col] is not None and self.grid[row][col].color != self.current_player:
                        self.grid[row][col] = None

                    # Устанавливаем флаг has_moved в True после первого хода (для пешек)
                    if isinstance(self.selected_piece, Pawn):
                        self.selected_piece.has_moved = True

                    # Переход хода к другому игроку
                    self.current_player = "black" if self.current_player == "white" else "white"

            # Сбрасываем выделение
            self.selected_piece = None
            self.valid_moves = []

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
            temp_grid = [[self.grid[row][col] for col in range(8)] for row in range(8)]
            temp_position = piece.position

            # Выполняем ход
            self.grid[piece.position[0]][piece.position[1]] = None
            self.grid[move[0]][move[1]] = piece
            piece.position = move

            # Проверяем, остался ли король под шахом
            if not self.is_king_in_check(self.current_player):
                filtered_moves.append(move)

            # Восстанавливаем исходное состояние доски
            self.grid = [[temp_grid[row][col] for col in range(8)] for row in range(8)]
            piece.position = temp_position

        return filtered_moves

    def run(self):
        """
        Основной игровой цикл для шахматной доски.
        """
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")

        running = True
        while running:
            # Отрисовка доски
            screen.fill((0, 0, 0))
            self.draw(screen)

            # Проверка на мат или пат
            if self.is_checkmate("white"):
                self.show_message(screen, "Мат! Черные победили.")
                running = False
            elif self.is_checkmate("black"):
                self.show_message(screen, "Мат! Белые победили.")
                running = False
            elif self.is_stalemate("white") or self.is_stalemate("black"):
                self.show_message(screen, "Пат! Ничья.")
                running = False

            # Обновление экрана
            pygame.display.flip()

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Обработка кликов на доске
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // self.cell_size
                    col = mouse_pos[0] // self.cell_size
                    self.handle_click(row, col)

        # Возврат в главное меню
        self.return_to_main_menu()

    def show_message(self, screen, message):
        """
        Отображает сообщение о результате игры.
        :param screen: Экран, на котором отрисовывается сообщение.
        :param message: Текст сообщения.
        """
        font = pygame.font.Font(None, 50)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Ждем 3 секунды перед возвратом в меню

    def return_to_main_menu(self):
        """
        Возвращает игру в главное меню.
        """
        # Здесь можно добавить логику для возврата в главное меню
        pass
