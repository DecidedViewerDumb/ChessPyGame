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
        Drawing the board and pieces.
        :param screen: The screen on which the board is drawn.
        """
        pygame.draw.rect(
            screen,
            (200, 200, 200),  # Frame colour
            (
                self.start_x - self.border_size,
                self.start_y - self.border_size,
                self.cell_size * 8 + 2 * self.border_size,
                self.cell_size * 8 + 2 * self.border_size
            )
        )

        # Drawing cells
        colours = [(235, 235, 208), (119, 149, 86)]
        for row in range(8):
            for col in range(8):
                x = self.start_x + col * self.cell_size
                y = self.start_y + row * self.cell_size
                colour = colours[(row + col) % 2]
                pygame.draw.rect(screen, colour, (x, y, self.cell_size, self.cell_size))

                # Highlighting of permissible moves
                if (row, col) in self.board.valid_moves:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 3)

        # File labels (a-h)
        for col in range(8):
            letter = chr(ord('A') + col)
            text = self.font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(
                    self.start_x + col * self.cell_size + self.cell_size//2,
                    self.start_y + 8 * self.cell_size + self.border_size//2
                )
            )
            screen.blit(text, text_rect)

        # Rank labels (1-8)
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

        # Drawing the chess pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    piece.draw(screen)

        # Highlighting the king under check
        current_player_king_pos = self.board.get_king_position(self.board.current_player)
        if self.board.state_checker.is_king_in_check(self.board.current_player):
            x = self.start_x + current_player_king_pos[1] * self.cell_size
            y = self.start_y + current_player_king_pos[0] * self.cell_size
            pygame.draw.rect(screen, (255, 0, 0, 100), (x, y, self.cell_size, self.cell_size), 5)
