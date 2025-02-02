import pygame
from classes.button import Button


class Menu:
    def __init__(self, screen_width, screen_height):
        """
        Инициализация меню.
        :param screen_width: Ширина экрана.
        :param screen_height: Высота экрана.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)  # Создаем шрифт здесь
        self.buttons = self.create_buttons()

    def create_buttons(self):
        """
        Создает кнопки для меню.
        :return: Список кнопок.
        """
        buttons = [
            Button(200, 200, 50, "Игра против компьютера", self.font, (0, 128, 255), (0, 255, 128), (255, 255, 255), self.screen_width),
            Button(300, 200, 50, "Игра против человека", self.font, (0, 128, 255), (0, 255, 128), (255, 255, 255), self.screen_width),
            Button(400, 200, 50, "Выход", self.font, (0, 128, 255), (0, 255, 128), (255, 255, 255), self.screen_width),
        ]
        return buttons

    def draw(self, screen):
        """
        Отрисовка меню.
        :param screen: Экран, на котором отрисовывается меню.
        """
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        """
        Обрабатывает события в меню.
        :param event: Событие Pygame.
        :return: Результат обработки (например, выбор режима игры).
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    return button.text
        return None
