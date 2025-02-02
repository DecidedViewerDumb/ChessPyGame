import pygame
import os


class Piece:
    def __init__(self, color, position, cell_size, image_name):
        """
        Базовый класс для всех фигур.
        :param color: Цвет фигуры ("black" или "white").
        :param position: Позиция фигуры на доске в виде кортежа (row, col).
        :param cell_size: Размер клетки доски.
        :param image_name: Имя файла изображения фигуры.
        """
        self.color = color
        self.position = position  # Позиция в виде (row, col)
        self.cell_size = cell_size

        # Загрузка изображения фигуры
        image_path = os.path.join("images", image_name)
        self.image = pygame.image.load(image_path)

        # Масштабирование изображения под размер клетки
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def draw(self, screen):
        """
        Отрисовка фигуры на экране.
        :param screen: Экран, на котором отрисовывается фигура.
        """
        x = self.position[1] * self.cell_size  # Вычисляем координату x
        y = self.position[0] * self.cell_size  # Вычисляем координату y
        screen.blit(self.image, (x, y))

    def get_valid_moves(self, board):
        """
        Возвращает список допустимых ходов для фигуры.
        :param board: Двумерный список, представляющий доску.
        :return: Список допустимых ходов в виде кортежей (row, col).
        """
        raise NotImplementedError("Метод get_valid_moves должен быть переопределен в дочернем классе.")
