import pygame
from classes.button import Button

class Menu:
    def __init__(self, screen_width, screen_height):
        """
        Initializing the menu.
        :param screen_width: Screen width.
        :param screen_height: Screen height.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)  # Создаем шрифт здесь
        self.buttons = self.create_buttons()

    def create_buttons(self):
        """
        Creates buttons for the menu.
        :return: List of buttons.
        """
        buttons = [
            Button(200, 200, 50, "Play against the computer", self.font, (0, 128, 255), (0, 255, 128), (255, 255, 255), self.screen_width),
            Button(300, 200, 50, "Play against a person", self.font, (0, 128, 255), (0, 255, 128), (255, 255, 255), self.screen_width),
            Button(400, 200, 50, "Exit", self.font, (0, 128, 255), (0, 255, 128), (255, 255, 255), self.screen_width),
        ]
        return buttons

    def draw(self, screen):
        """
        Rendering the menu.
        :param screen: The screen on which the menu is rendered.
        """
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        """
        Handles events in the menu.
        :param event: Pygame event.
        :return: The result of the processing (e.g. selecting a game mode).
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    return button.text
        return None
