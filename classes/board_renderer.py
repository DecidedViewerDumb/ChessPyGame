import pygame

class BoardRenderer:
    def __init__(self, board, screen_width, screen_height):
        self.board = board
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = min(screen_width, screen_height) // 8
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """
        Drawing the board and pieces.
        :param screen: The screen on which the board is drawn.
        """
        colours = [(235, 235, 208), (119, 149, 86)]  # Cell colours (white and green)

        for row in range(8):
            for col in range(8):
                colour = colours[(row + col) % 2]
                x = col * self.cell_size
                y = row * self.cell_size
                pygame.draw.rect(screen, colour, (x, y, self.cell_size, self.cell_size))

                if (row, col) in self.board.valid_moves:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 3)

                if self.board.grid[row][col] is not None:
                    self.board.grid[row][col].draw(screen)

        text = self.font.render(f"Move: {self.board.current_player}", True, (255, 255, 255))
        screen.blit(text, (self.screen_width - 150, 275))

        if self.board.is_king_in_check("white"):
            king_pos = self.board.find_king_position("white")
            if king_pos:
                x = king_pos[1] * self.cell_size
                y = king_pos[0] * self.cell_size
                pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 5)
        if self.board.is_king_in_check("black"):
            king_pos = self.board.find_king_position("black")
            if king_pos:
                x = king_pos[1] * self.cell_size
                y = king_pos[0] * self.cell_size
                pygame.draw.rect(screen, (255, 0, 0), (x, y, self.cell_size, self.cell_size), 5)
