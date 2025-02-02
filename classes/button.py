import pygame


class Button:
    def __init__(self, y, width, height, text, font, color, hover_color, text_color, screen_width, visible=True):
        """
        Инициализация кнопки.
        :param y: Позиция кнопки по вертикали (от верхнего края экрана).
        :param width: Ширина кнопки.
        :param height: Высота кнопки.
        :param text: Текст на кнопке.
        :param font: Шрифт для текста.
        :param color: Основной цвет кнопки.
        :param hover_color: Цвет кнопки при наведении.
        :param text_color: Цвет текста.
        :param screen_width: Ширина экрана (для центрирования кнопки).
        :param visible: Видимость кнопки (True/False).
        """
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.visible = visible  # Параметр видимости

        # Вычисляем позицию кнопки по горизонтали для центрирования
        self.x = (screen_width - width) // 2
        self.y = y

        # Создаем прямоугольник для кнопки
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, screen):
        """
        Отрисовка кнопки на экране (если она видима).
        :param screen: Экран, на котором отрисовывается кнопка.
        """
        if self.visible:  # Отрисовываем только если кнопка видима
            # Изменяем цвет кнопки, если наведена
            if self.hovered:
                pygame.draw.rect(screen, self.hover_color, self.rect)
            else:
                pygame.draw.rect(screen, self.color, self.rect)

            # Рендерим текст
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """
        Проверка, наведен ли курсор на кнопку (если она видима).
        :param mouse_pos: Позиция курсора мыши.
        """
        if self.visible:  # Проверяем наведение только если кнопка видима
            self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        """
        Проверка, нажата ли кнопка (если она видима).
        :param mouse_pos: Позиция курсора мыши.
        :param mouse_pressed: Состояние кнопок мыши.
        """
        if self.visible:  # Проверяем нажатие только если кнопка видима
            return self.hovered and mouse_pressed[0]
        return False

    def set_visible(self, visible):
        """
        Устанавливает видимость кнопки.
        :param visible: Булево значение (True/False).
        """
        self.visible = visible
