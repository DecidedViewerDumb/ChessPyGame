import pygame


class BoardRenderer:
    def __init__(self, board, start_x, start_y, cell_size, border_size):
        self.board = board
        self.start_x = start_x
        self.start_y = start_y
        self.cell_size = cell_size
        self.border_size = border_size
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """
        Отрисовка доски и фигур.
        :param screen: Экран, на котором отрисовывается доска.
        """
        pygame.draw.rect(
            screen,
            (200, 200, 200),  # Цвет рамки
            (
                self.start_x - self.border_size,
                self.start_y - self.border_size,
                self.cell_size * 8 + 2 * self.border_size,
                self.cell_size * 8 + 2 * self.border_size
            )
        )

        # Отрисовка клеток
        colors = [(235, 235, 208), (119, 149, 86)]
        for row in range(8):
            for col in range(8):
                x = self.start_x + col * self.cell_size
                y = self.start_y + row * self.cell_size
                color = colors[(row + col) % 2]
                pygame.draw.rect(screen, color, (x, y, self.cell_size, self.cell_size))

                # Подсветка допустимых ходов
                if (row, col) in self.board.valid_moves:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 3)

        # Подписи столбцов (a-h)
        for col in range(8):
            letter = chr(ord('a') + col)
            text = self.font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(
                    self.start_x + col * self.cell_size + self.cell_size//2,
                    self.start_y + 8 * self.cell_size + self.border_size//2
                )
            )
            screen.blit(text, text_rect)

        # Подписи строк (1-8)
        for row in range(8):
            number = str(8 - row)
            text = self.font.render(number, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(
                    self.start_x - self.border_size//2,
                    self.start_y + row * self.cell_size + self.cell_size//2
                )
            )
            screen.blit(text, text_rect)

        # Отрисовка фигур
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    piece.draw(screen)
