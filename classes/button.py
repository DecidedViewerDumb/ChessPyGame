import pygame


class Button:
    def __init__(
            self,
            y,
            text,
            font,
            colour,
            hover_colour,
            text_colour,
            screen_width,
            padding_x=20,
            padding_y=10,
            visible=True
    ):
        """
        Initialize an auto-sized button.
        :param y: Vertical position
        :param text: Button text
        :param font: Font for text
        :param colour: Primary colour
        :param hover_colour: Hover colour
        :param text_colour: Text colour
        :param screen_width: Screen width to center
        :param padding_x: Horizontal padding
        :param padding_y: Vertical padding
        """
        self.text = text
        self.font = font
        self.colour = colour
        self.colour = hover_colour
        self.colour = text_colour
        self.hovered = False
        self.visible = visible

        # Calculate button sizes based on text
        text_width, text_height = self.font.size(self.text)
        self.width = text_width + 2 * padding_x
        self.height = text_height + 2 * padding_y

        # Centering horizontally
        self.x = (screen_width - self.width) // 2
        self.y = y

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """
        Draws the button on the screen (if it is visible).
        :param screen: The screen on which the button is drawn.
        """
        if self.visible:  # Draw only if the button is visible
            # Change button colour when hovered
            colour = self.hover_colour if self.hovered else self.colour
            pygame.draw.rect(screen, colour, self.rect, border_radius=5)

            # Rendering text
            text_surface = self.font.render(self.text, True, self.text_colour)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """
        Check if the mouse is over the button (if it is visible).
        :param mouse_pos: The position of the mouse cursor.
        """
        if self.visible:  # We check hover only if the button is visible
            self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        """
        Check if the button is pressed (if it is visible).
        :param mouse_pos: The position of the mouse cursor.
        :param mouse_pressed: The state of the mouse buttons.
        """
        if self.visible:  # We check for pressing only if the button is visible
            return self.hovered and mouse_pressed[0]
        return False

    def set_visible(self, visible):
        """
        Sets the visibility of the button.
        :param visible: Boolean value (True/False).
        """
        self.visible = visible
