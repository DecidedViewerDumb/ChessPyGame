import pygame
from classes.game_state_checker import GameStateChecker
from classes.board_renderer import BoardRenderer
from classes.move_handler import MoveHandler
from classes.ai import RandomAI
from classes.pieces.king import King
from classes.pieces.pawn import Pawn
from classes.pieces.rook import Rook
from classes.pieces.knight import Knight
from classes.pieces.bishop import Bishop
from classes.pieces.queen import Queen


class Board:
    def __init__(self, screen_width, screen_height, mode="human_vs_human", timer_minutes=5):
        """
        Инициализация доски.
        :param screen_width: Ширина экрана.
        :param screen_height: Высота экрана.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Размеры областей
        self.board_width = int(screen_width * 0.7)  # 70% под доску
        self.info_panel_width = screen_width - self.board_width

        # Расчет параметров доски
        self.border_size = 20
        self.cell_size = (self.board_width - 2 * self.border_size) // 8

        # Позиция доски
        self.board_start_x = self.border_size
        self.board_start_y = (screen_height - (self.cell_size * 8)) // 2

        # Позиция информационной панели
        self.info_panel_x = self.board_width
        self.info_panel_y = 50

        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.add_pieces()

        self.selected_piece = None
        self.valid_moves = []
        self.current_player = "white"
        self.en_passant_target = None

        self.state_checker = GameStateChecker(self)
        self.renderer = BoardRenderer(
            self,
            self.board_start_x,
            self.board_start_y,
            self.cell_size,
            self.border_size
        )
        self.move_handler = MoveHandler(self)

        self.mode = mode  # Режим игры
        if self.mode == "human_vs_ai":
            self.ai = RandomAI(self)  # Инициализируем AI

        # Таймеры для игроков
        self.timer_minutes = timer_minutes
        self.white_time = timer_minutes * 60  # Время в секундах
        self.black_time = timer_minutes * 60  # Время в секундах
        self.last_time_update = pygame.time.get_ticks()  # Время последнего обновления таймера

    def update_timers(self, screen):
        """
        Обновляет таймеры игроков.
        """
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_time_update) / 1000  # Время в секундах

        if self.current_player == "white":
            self.white_time -= elapsed_time
        else:
            self.black_time -= elapsed_time

        self.last_time_update = current_time

        # Проверяем, не истекло ли время у одного из игроков
        if self.white_time <= 0:
            self.white_time = 0
            self.show_message(screen, "Время вышло! Черные победили.")
            return True  # Игра завершена
        elif self.black_time <= 0:
            self.black_time = 0
            self.show_message(screen, "Время вышло! Белые победили.")
            return True  # Игра завершена

        return False  # Игра продолжается

    def draw_timers(self, screen):
        """
        Отрисовывает таймеры игроков на экране.
        :param screen: Экран, на котором отрисовываются таймеры.
        """
        font = pygame.font.Font(None, 36)

        pygame.draw.rect(screen, (50, 50, 50), (self.info_panel_x, 0, self.info_panel_width, self.screen_height))

        # Позиционирование в правой панели
        panel_center_x = self.info_panel_x + self.info_panel_width//2

        # Текущий игрок
        text = font.render(f"Ход: {self.current_player}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(panel_center_x, self.screen_height // 2))
        screen.blit(text, text_rect)

        # Таймеры
        white_time_str = f"Белые: {int(self.white_time // 60):02}:{int(self.white_time % 60):02}"
        black_time_str = f"Черные: {int(self.black_time // 60):02}:{int(self.black_time % 60):02}"

        white_text = font.render(white_time_str, True, (255, 255, 255))
        black_text = font.render(black_time_str, True, (255, 255, 255))

        # Расположение таймеров
        screen.blit(white_text, (panel_center_x - white_text.get_width() // 2, self.screen_height - 50))
        screen.blit(black_text, (panel_center_x - black_text.get_width() // 2, self.info_panel_y))

    def add_pieces(self):
        """
        Добавляет фигуры на доску.
        """
        # Добавляем черные пешки
        for col in range(8):
            pawn = Pawn("black", (1, col), self.cell_size, self.board_start_x, self.board_start_y)
            pawn.board = self  # Добавляем ссылку на доску
            self.grid[1][col] = pawn

        # Добавляем белые пешки
        for col in range(8):
            pawn = Pawn("white", (6, col), self.cell_size, self.board_start_x, self.board_start_y)
            pawn.board = self
            self.grid[6][col] = pawn

        # Добавляем черные ладьи
        self.grid[0][0] = Rook("black", (0, 0), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[0][7] = Rook("black", (0, 7), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем белые ладьи
        self.grid[7][0] = Rook("white", (7, 0), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[7][7] = Rook("white", (7, 7), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем черных коней
        self.grid[0][1] = Knight("black", (0, 1), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[0][6] = Knight("black", (0, 6), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем белых коней
        self.grid[7][1] = Knight("white", (7, 1), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[7][6] = Knight("white", (7, 6), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем черных слонов
        self.grid[0][2] = Bishop("black", (0, 2), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[0][5] = Bishop("black", (0, 5), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем белых слонов
        self.grid[7][2] = Bishop("white", (7, 2), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[7][5] = Bishop("white", (7, 5), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем черную королеву
        self.grid[0][3] = Queen("black", (0, 3), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем белую королеву
        self.grid[7][3] = Queen("white", (7, 3), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем черного короля
        self.grid[0][4] = King("black", (0, 4), self.cell_size, self.board_start_x, self.board_start_y)

        # Добавляем белого короля
        self.grid[7][4] = King("white", (7, 4), self.cell_size, self.board_start_x, self.board_start_y)

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

    def is_king_in_check(self, color):
        return self.state_checker.is_king_in_check(color)

    def is_checkmate(self, color):
        return self.state_checker.is_checkmate(color)

    def is_stalemate(self, color):
        return self.state_checker.is_stalemate(color)

    def draw(self, screen):
        self.renderer.draw(screen)

    def handle_click(self, row, col):
        self.move_handler.handle_click(row, col)

    def run(self):
        """
        Основной игровой цикл для шахматной доски.
        """
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")

        running = True
        game_over = False

        while running and not game_over:
            screen.fill((0, 0, 0))
            self.draw(screen)

            # Отрисовываем таймеры
            self.draw_timers(screen)

            # Обновляем таймеры
            if self.update_timers(screen):
                game_over = True  # Время одного из игроков истекло

            if not game_over:
                if self.is_checkmate("white"):
                    self.show_message(screen, "Мат! Черные победили.")
                    game_over = True
                elif self.is_checkmate("black"):
                    self.show_message(screen, "Мат! Белые победили.")
                    game_over = True
                elif self.is_stalemate("white") or self.is_stalemate("black"):
                    self.show_message(screen, "Пат! Ничья.")
                    game_over = True

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // self.cell_size
                    col = mouse_pos[0] // self.cell_size
                    self.handle_click(row, col)

            # Ход компьютера (если режим "human_vs_ai" и текущий игрок — чёрные)
            if self.mode == "human_vs_ai" and self.current_player == "black" and not game_over:
                self.make_ai_move()

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
        pygame.time.wait(3000)

    def return_to_main_menu(self):
        """
        Возвращает игру в главное меню.
        """
        from main import main
        main()

    def make_ai_move(self):
        """
        Выполняет ход компьютера.
        """
        move = self.ai.get_random_move()
        if move:
            (start_row, start_col), (end_row, end_col) = move
            self.move_handler.handle_click(start_row, start_col)  # Выбираем фигуру
            self.move_handler.handle_click(end_row, end_col)  # Выполняем ход
