import pygame

class Button:
    def __init__(self, y, width, height, text, font, colour, hover_colour, text_colour, screen_width, visible=True):
        """
        Initialize the button.
        :param y: The vertical position of the button (from the top edge of the screen).
        :param width: The width of the button.
        :param height: The height of the button.
        :param text: The text on the button.
        :param font: The font for the text.
        :param hover_colour: The colour of the button when hovering.
        :param text_colour: The colour of the text.
        :param screen_width: The width of the screen (for centering the button).
        :param visible: The visibility of the button (True/False).
        """
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        self.hovered = False
        self.visible = visible  # Visibility parameter

        #Calculating the horizontal position of the button for centering
        self.x = (screen_width - width) // 2
        self.y = y

        # Creating a rectangle for the button
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def draw(self, screen):
        """
        Draws the button on the screen (if it is visible).
        :param screen: The screen on which the button is drawn.
        """
        if self.visible: # Draw only if the button is visible
            # Change the button colour when hovered
            if self.hovered:
                pygame.draw.rect(screen, self.hover_colour, self.rect)
            else:
                pygame.draw.rect(screen, self.colour, self.rect)

            # Rendering the text
            text_surface = self.font.render(self.text, True, self.text_colour)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """
        Check if the mouse is over the button (if it is visible).
        :param mouse_pos: The position of the mouse cursor.
        """
        if self.visible:  # Checking hover only if the button is visible
            self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        """
        Check if the button is pressed (if it is visible).
        :param mouse_pos: The position of the mouse cursor.
        :param mouse_pressed: The state of the mouse buttons.
        """
        if self.visible:  # Checking for pressing only if the button is visible
            return self.hovered and mouse_pressed[0]
        return False

    def set_visible(self, visible):
        """
        Sets the visibility of the button.
        :param visible: Boolean value (True/False).
        """
        self.visible = visible
