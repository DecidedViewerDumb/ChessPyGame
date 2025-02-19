import pygame
import os

class Piece:
    def __init__(self, colour, position, cell_size, image_name):
        """
        Base class for all pieces.
        :param colour: The colour of the piece ("black" or "white").
        :param position: The position of the piece on the board as a tuple (row, col).
        :param cell_size: The size of the board cell.
        :param image_name: The name of the image file of the piece.
        """
        self.colour = colour
        self.position = position  # Position as (row, col)
        self.cell_size = cell_size

        # Loading figure image
        image_path = os.path.join("images", image_name)
        self.image = pygame.image.load(image_path)

        # Scaling the image to fit the cell size
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def draw(self, screen):
        """
        Drawing the figure on the screen.
        :param screen: The screen on which the figure is drawn.
        """
        x = self.position[1] * self.cell_size  # Calculate the x coordinate
        y = self.position[0] * self.cell_size  # Calculate the y coordinate
        screen.blit(self.image, (x, y))

    def get_valid_moves(self, board):
        """
        Returns a list of legal moves for the piece.
        :param board: A two-dimensional list representing the board.
        :return: A list of legal moves as (row, col) tuples.
        """
        raise NotImplementedError("The get_valid_moves method must be overridden in the child class.")
