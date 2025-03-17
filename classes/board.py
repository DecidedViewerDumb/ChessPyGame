import os

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
        Initializing the board.
        :param screen_width: Screen width.
        :param screen_height: Screen height.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Area sizes
        self.board_width = int(screen_width * 0.7)  # 70% под доску
        self.info_panel_width = screen_width - self.board_width

        # Calculation of board parameters
        self.border_size = 20
        self.cell_size = (self.board_width - 2 * self.border_size) // 8

        # Board position
        self.board_start_x = self.border_size
        self.board_start_y = (screen_height - (self.cell_size * 8)) // 2

            # Position of the information panel
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

        self.mode = mode  # Game mode
        if self.mode == "human_vs_ai":
            self.ai = RandomAI(self)  # Initialize AI

        # Timers for players
        self.timer_minutes = timer_minutes
        self.white_time = timer_minutes * 60  # Time in seconds
        self.black_time = timer_minutes * 60  # Time in seconds
        self.last_time_update = pygame.time.get_ticks()  # Time of last timer update
        self.promotion_pawn = None
        self.promotion_active = False
        self.promotion_piece = None
        self.promotion_buttons = []

    def draw_promotion_menu(self, screen, pawn):
        colors = [(235, 235, 208), (119, 149, 86)]
        menu_width = 4 * self.cell_size

        col = pawn.position[1]
        if col < 2:
            menu_x = self.board_start_x
        elif col > 5:
            menu_x = self.board_start_x + (8 - 4) * self.cell_size
        else:
            menu_x = self.board_start_x + (col - 1) * self.cell_size
        menu_y = self.board_start_y + pawn.position[0] * self.cell_size

        # Adjusting the position for black pawns
        if pawn.color == "black":
            menu_y -= 3 * self.cell_size

        # Selection window frame
        pygame.draw.rect(screen, (0, 0, 0), (menu_x - 2, menu_y - 2, menu_width + 4, self.cell_size + 4), 3)

        pieces = [Queen, Rook, Bishop, Knight]

        self.promotion_buttons = []
        for i, piece_class in enumerate(pieces):
            x = menu_x + i * self.cell_size
            rect = pygame.Rect(x, menu_y, self.cell_size, self.cell_size)
            self.promotion_buttons.append((rect, piece_class))

            # Drawing a button with a frame
            pygame.draw.rect(screen, colors[i % 2], rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            name_piece = piece_class.__name__[0] if not piece_class == Knight else 'N'
            image_name = f"{'b' if pawn.color == 'black' else 'w'}{name_piece}.png"
            image = pygame.image.load(os.path.join("images", image_name))
            image = pygame.transform.scale(image, (self.cell_size, self.cell_size))
            screen.blit(image, (x, menu_y))

    def handle_promotion_click(self, mouse_pos):
        for rect, piece_class in self.promotion_buttons:
            if rect.collidepoint(mouse_pos):
                self.promotion_piece = piece_class
                return True
        return False

    def update_timers(self, screen):
        """
        Updates players timers.
        """
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_time_update) / 1000  # Time in seconds

        if self.current_player == "white":
            self.white_time -= elapsed_time
        else:
            self.black_time -= elapsed_time

        self.last_time_update = current_time

        # Checking if one of the players has run out of time
        if self.white_time <= 0:
            self.white_time = 0
            self.show_message(screen, "Time's up! Black wins.")
            return True  # Game over
        elif self.black_time <= 0:
            self.black_time = 0
            self.show_message(screen, "Time's up! White wins.")
            return True  # Game over

        return False  # The game continues

    def draw_timers(self, screen):
        """
        Draws player timers on the screen.
        :param screen: The screen on which the timers are drawn.
        """
        font = pygame.font.Font(None, 36)

        pygame.draw.rect(screen, (50, 50, 50), (self.info_panel_x, 0, self.info_panel_width, self.screen_height))

        # Positioning in the right panel
        panel_center_x = self.info_panel_x + self.info_panel_width//2

        # Current player
        text = font.render(f"Turn: {self.current_player}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(panel_center_x, self.screen_height // 2))
        screen.blit(text, text_rect)

        # Timers
        white_time_str = f"White: {int(self.white_time // 60):02}:{int(self.white_time % 60):02}"
        black_time_str = f"Black: {int(self.black_time // 60):02}:{int(self.black_time % 60):02}"

        white_text = font.render(white_time_str, True, (255, 255, 255))
        black_text = font.render(black_time_str, True, (255, 255, 255))

        # Timers location
        screen.blit(white_text, (panel_center_x - white_text.get_width() // 2, self.screen_height - 50))
        screen.blit(black_text, (panel_center_x - black_text.get_width() // 2, self.info_panel_y))

    def add_pieces(self):
        """
        Adds pieces to the board.
        """
        # Add black pawns
        for col in range(8):
            pawn = Pawn("black", (1, col), self.cell_size, self.board_start_x, self.board_start_y)
            pawn.board = self  # Add a link to the board
            self.grid[1][col] = pawn

        # Add white pawns
        for col in range(8):
            pawn = Pawn("white", (6, col), self.cell_size, self.board_start_x, self.board_start_y)
            pawn.board = self
            self.grid[6][col] = pawn

        # Add black rooks
        self.grid[0][0] = Rook("black", (0, 0), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[0][7] = Rook("black", (0, 7), self.cell_size, self.board_start_x, self.board_start_y)

        # Add white rooks
        self.grid[7][0] = Rook("white", (7, 0), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[7][7] = Rook("white", (7, 7), self.cell_size, self.board_start_x, self.board_start_y)

        # Add black knights
        self.grid[0][1] = Knight("black", (0, 1), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[0][6] = Knight("black", (0, 6), self.cell_size, self.board_start_x, self.board_start_y)

        # Add white knights
        self.grid[7][1] = Knight("white", (7, 1), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[7][6] = Knight("white", (7, 6), self.cell_size, self.board_start_x, self.board_start_y)

        # Adding black bishops
        self.grid[0][2] = Bishop("black", (0, 2), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[0][5] = Bishop("black", (0, 5), self.cell_size, self.board_start_x, self.board_start_y)

        # Adding black bishops
        self.grid[7][2] = Bishop("white", (7, 2), self.cell_size, self.board_start_x, self.board_start_y)
        self.grid[7][5] = Bishop("white", (7, 5), self.cell_size, self.board_start_x, self.board_start_y)

        # Adding the black queen
        self.grid[0][3] = Queen("black", (0, 3), self.cell_size, self.board_start_x, self.board_start_y)

        # Adding the white queen
        self.grid[7][3] = Queen("white", (7, 3), self.cell_size, self.board_start_x, self.board_start_y)

        # Adding the black king
        self.grid[0][4] = King("black", (0, 4), self.cell_size, self.board_start_x, self.board_start_y)

        # Adding the white king
        self.grid[7][4] = King("white", (7, 4), self.cell_size, self.board_start_x, self.board_start_y)

    def find_king_position(self, color):
        """
        Finds the king's position on the board.
        :param color: The king's color ("black" or "white").
        :return: The king's position as a tuple (row, col).
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

    def get_king_position(self, color):
        return self.state_checker.find_king_position(color)

    def draw(self, screen):
        self.renderer.draw(screen)

    def handle_click(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:  # Checking board boundaries
            self.move_handler.handle_click(row, col)
        else:
            self.selected_piece = None
            self.valid_moves = []
            return

    def run(self):
        """
        The basic game cycle for a chessboard.
        """
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game")

        running = True
        game_over = False

        while running and not game_over:
            screen.fill((0, 0, 0))
            self.draw(screen)

            # Drawing timers
            self.draw_timers(screen)

            # Updating timers
            if self.update_timers(screen):
                game_over = True  # One of the players time has expired.

            if not game_over:
                if self.is_checkmate("white"):
                    self.show_message(screen, "Checkmate! Black wins.")
                    game_over = True
                elif self.is_checkmate("black"):
                    self.show_message(screen, "Checkmate! White wins.")
                    game_over = True
                elif self.is_stalemate("white") or self.is_stalemate("black"):
                    self.show_message(screen, "Stalemate! Draw.")
                    game_over = True

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check that the click was within the board
                    if (self.board_start_x <= mouse_pos[0] < self.board_start_x + 8 * self.cell_size and
                            self.board_start_y <= mouse_pos[1] < self.board_start_y + 8 * self.cell_size):
                        # Convert coordinates only for clicks inside the board
                        row = (mouse_pos[1] - self.board_start_y) // self.cell_size
                        col = (mouse_pos[0] - self.board_start_x) // self.cell_size
                        self.handle_click(row, col)

            # Computer move (if "human_vs_ai" mode and current player are black)
            if self.mode == "human_vs_ai" and self.current_player == "black" and not game_over:
                self.make_ai_move()

        self.return_to_main_menu()

    def show_message(self, screen, message):
        """
        Displays a message about the game result.
        :param screen: The screen on which the message is drawn.
        :param message: The text of the message.
        """
        font = pygame.font.Font(None, 50)
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def return_to_main_menu(self):
        """
        Returns the game to the main menu.
        """
        from main import main
        main()

    def make_ai_move(self):
        """
        Performs the computers move.
        """
        move = self.ai.get_random_move()
        if move:
            (start_row, start_col), (end_row, end_col) = move
            self.move_handler.handle_click(start_row, start_col)  # Select a figure
            self.move_handler.handle_click(end_row, end_col)  # Making the move
