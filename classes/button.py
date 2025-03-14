import pygame


class Button:
    def __init__(
            self,
            y,
            text,
            font,
            color,
            hover_color,
            text_color,
            screen_width,
            padding_x=20,
            padding_y=10,
            visible=True
    ):
        """
        Инициализация кнопки с автоматическим размером.
        :param y: Позиция по вертикали
        :param text: Текст кнопки
        :param font: Шрифт для текста
        :param color: Основной цвет
        :param hover_color: Цвет при наведении
        :param text_color: Цвет текста
        :param screen_width: Ширина экрана для центрирования
        :param padding_x: Отступ по горизонтали
        :param padding_y: Отступ по вертикали
        """
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.visible = visible

        # Рассчитываем размеры кнопки на основе текста
        text_width, text_height = self.font.size(self.text)
        self.width = text_width + 2 * padding_x
        self.height = text_height + 2 * padding_y

        # Центрирование по горизонтали
        self.x = (screen_width - self.width) // 2
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        Отрисовка кнопки на экране (если она видима).
        :param screen: Экран, на котором отрисовывается кнопка.
        """
        if self.visible:  # Отрисовываем только если кнопка видима
            # Изменяем цвет кнопки, если наведена
            color = self.hover_color if self.hovered else self.color
            pygame.draw.rect(screen, color, self.rect, border_radius=5)

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
